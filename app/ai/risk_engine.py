"""Central Risk Intelligence Engine for KhetRakshak AI.
Aggregates crop physiology, growth stage sensitivity, localized GIS hydrology,
river gauges, soil moisture, and weather forecasts into explainable risk indicators.

Follows the paradigm:
DETECT -> PREDICT -> UNDERSTAND -> ADVISE -> PROTECT
"""

from typing import Dict, Any, List, Optional, Tuple
from app.models import (
    FarmProfile,
    EnvironmentalFactors,
    DiseaseDetectionResult,
    RiskEngineResult,
    RiskBreakdown
)
from app.data.bihar_districts import BIHAR_DISTRICTS
from app.data.crop_agronomy import CROPS_AGRONOMY

def calculate_flood_and_waterlogging_risk(
    profile: FarmProfile,
    env: EnvironmentalFactors,
    stage_multiplier: float
) -> int:
    """Calculates waterlogging & flood inundation risk (0-100)."""
    # 1. Rainfall forecast component (0-35 pts)
    # Heavy rainfall (>65mm) in 48h creates severe ponding
    rf_pts = min(35.0, (env.forecast_rainfall_48h_mm / 100.0) * 35.0)
    if env.forecast_rainfall_48h_mm > 75.0:
        rf_pts = max(30.0, rf_pts)

    # 2. Existing soil moisture saturation (0-25 pts)
    # Soils saturated > 80% cannot absorb incremental rainfall
    sm_pts = (env.soil_moisture_pct / 100.0) * 25.0

    # 3. River gauge telemetry & basin flood history (0-25 pts)
    river_pts = 5.0
    if env.river_level_status == "Above Danger Level":
        river_pts = 25.0
    elif env.river_level_status == "Near Warning Level":
        river_pts = 20.0
    elif env.historical_flood_vulnerability == "High" or env.historical_flood_vulnerability == "Severe":
        river_pts = 16.0
    elif env.historical_flood_vulnerability == "Medium":
        river_pts = 10.0

    # 4. Crop stage vulnerability multiplier
    # e.g. Maize flowering root asphyxiation vulnerability
    base_score = rf_pts + sm_pts + river_pts
    adjusted_score = base_score * (0.85 + (stage_multiplier - 1.0) * 0.4)
    
    return int(min(100, max(5, round(adjusted_score))))

def calculate_drought_and_water_stress_risk(
    profile: FarmProfile,
    env: EnvironmentalFactors,
    normal_monsoon_mm: float
) -> int:
    """Calculates moisture deficit and drought stress (0-100)."""
    # Low soil moisture (< 40%) drives stress
    soil_deficit_pts = max(0.0, (50.0 - env.soil_moisture_pct) * 1.3)
    
    # Rainfall deficit in 24h & 48h forecast
    rain_pts = max(0.0, (30.0 - env.forecast_rainfall_48h_mm) * 1.1)
    
    # High heat / evapotranspiration
    heat_pts = max(0.0, (env.temperature_max_c - 30.0) * 2.0)
    
    # Historical drought baseline for South Bihar
    drought_base = 25.0 if env.historical_drought_vulnerability == "High" else 5.0
    
    raw = soil_deficit_pts + rain_pts + heat_pts + drought_base
    return int(min(100, max(5, round(raw))))

def calculate_excess_rain_risk(env: EnvironmentalFactors) -> int:
    """Evaluates excess rainfall surge threat over the next 48 hours."""
    combined_rain = env.current_rainfall_mm * 0.4 + env.forecast_rainfall_48h_mm * 0.8
    score = (combined_rain / 120.0) * 100.0
    return int(min(100, max(5, round(score))))

def calculate_disease_and_pest_risk(
    crop: str,
    env: EnvironmentalFactors,
    scan_result: Optional[DiseaseDetectionResult]
) -> Tuple[int, int]:
    """Combines Computer Vision lesion severity with micro-climate humidity & temperature."""
    # Base disease risk from weather (humid warm conditions favor fungal / bacterial sporulation)
    weather_disease_pts = 20
    if env.relative_humidity_pct > 80.0 and env.temperature_max_c > 26.0:
        weather_disease_pts += 25
    if env.forecast_rainfall_48h_mm > 50.0:
        weather_disease_pts += 15

    # Direct visual disease scan component
    if scan_result and not scan_result.is_low_confidence:
        if scan_result.severity == "Severe":
            scan_pts = 40
        elif scan_result.severity in ["Moderate", "High"]:
            scan_pts = 25
        else:
            scan_pts = 5
    else:
        scan_pts = 10

    total_disease = min(100, weather_disease_pts + scan_pts)

    # Pest risk (e.g. armyworm in dry-wet cycle or aphids in cloudy weather)
    pest_risk = 35
    if env.relative_humidity_pct > 75 and env.temperature_max_c < 30:
        pest_risk += 15
    if scan_result and "Pest" in scan_result.pathogen_type:
        pest_risk = max(pest_risk, 65)

    return total_disease, pest_risk

def evaluate_crop_risk(
    profile: FarmProfile,
    env: EnvironmentalFactors,
    scan_result: Optional[DiseaseDetectionResult] = None
) -> RiskEngineResult:
    """Executes the complete multi-dimensional KhetRakshak Risk Engine."""
    
    # 1. Lookup crop agronomic stage sensitivity
    crop_data = CROPS_AGRONOMY.get(profile.crop, CROPS_AGRONOMY["Maize"])
    stages = crop_data.get("stages", [])
    
    stage_multiplier = 1.2
    for s in stages:
        if profile.crop_stage.lower() in s["name"].lower() or s["name"].lower() in profile.crop_stage.lower():
            stage_multiplier = s.get("flood_risk_multiplier", 1.2)
            break

    # 2. Lookup district normal rainfall
    district_data = BIHAR_DISTRICTS.get(profile.district, BIHAR_DISTRICTS["Purnia"])
    normal_monsoon = district_data.get("normal_rainfall_monsoon_mm", 1100.0)

    # 3. Calculate sub-indices
    flood_risk = calculate_flood_and_waterlogging_risk(profile, env, stage_multiplier)
    water_stress = calculate_drought_and_water_stress_risk(profile, env, normal_monsoon)
    drought_risk = water_stress  # In this agronomic model, drought reflects prolonged water stress
    excess_rain_risk = calculate_excess_rain_risk(env)
    disease_risk, pest_risk = calculate_disease_and_pest_risk(profile.crop, env, scan_result)

    # 4. Synthesize Aggregate KhetRakshak Score (0-100)
    # The score dynamically weights the dominant environmental hazard for this district
    is_flood_zone = district_data.get("zone_type") in ["FLOOD_PRONE", "MIXED_RIVERINE"]
    
    if is_flood_zone:
        # North Bihar weighting: Flood & Excess Rain are heavy drivers
        overall = (
            flood_risk * 0.35 +
            excess_rain_risk * 0.25 +
            disease_risk * 0.22 +
            pest_risk * 0.10 +
            water_stress * 0.08
        )
    else:
        # South Bihar weighting: Water Stress & Drought are dominant
        overall = (
            water_stress * 0.40 +
            drought_risk * 0.25 +
            disease_risk * 0.20 +
            pest_risk * 0.10 +
            flood_risk * 0.05
        )

    overall_score = int(min(100, max(5, round(overall))))

    # 5. Classify Risk Level
    if overall_score >= 70:
        risk_level = "HIGH"
        risk_level_hindi = "उच्च जोखिम (High Risk)"
    elif overall_score >= 45:
        risk_level = "MODERATE"
        risk_level_hindi = "मध्यम जोखिम (Moderate Risk)"
    elif overall_score >= 25:
        risk_level = "LOW-MODERATE"
        risk_level_hindi = "हल्का जोखिम (Low-Moderate)"
    else:
        risk_level = "LOW"
        risk_level_hindi = "निम्न जोखिम (Low Risk)"

    # 6. Generate Explainability: Why is it high risk? (No technical overload)
    why_reasons: List[str] = []
    why_reasons_hindi: List[str] = []

    if flood_risk >= 70:
        why_reasons.append(f"Heavy rainfall forecast ({env.forecast_rainfall_48h_mm:.1f} mm) in saturated catchment.")
        why_reasons_hindi.append(f"जलग्रहण क्षेत्र में भारी बारिश ({env.forecast_rainfall_48h_mm:.1f} मिमी) का अनुमान।")
        
        why_reasons.append(f"Soil moisture is extremely high ({env.soil_moisture_pct:.0f}%), limiting infiltration.")
        why_reasons_hindi.append(f"खेत की मिट्टी में नमी अत्यधिक ({env.soil_moisture_pct:.0f}%) है, जिससे पानी तुरंत सोखना मुश्किल है।")
        
        why_reasons.append(f"River {env.river_name} is '{env.river_level_status}'.")
        why_reasons_hindi.append(f"{env.river_name} नदी का जलस्तर '{env.river_level_status}' की स्थिति में है।")
    elif drought_risk >= 65:
        why_reasons.append(f"Severe rainfall deficit over recent weeks in {profile.district}.")
        why_reasons_hindi.append(f"{profile.district} में हाल के हफ्तों में सामान्य से बहुत कम वर्षा हुई है।")
        
        why_reasons.append(f"Soil moisture critically low ({env.soil_moisture_pct:.0f}%).")
        why_reasons_hindi.append(f"खेत की मिट्टी में नमी गंभीर रूप से कम ({env.soil_moisture_pct:.0f}%) है।")

    if disease_risk >= 50:
        why_reasons.append(f"High relative humidity ({env.relative_humidity_pct:.0f}%) creates ideal fungal & bacterial conditions.")
        why_reasons_hindi.append(f"उच्च आर्द्रता ({env.relative_humidity_pct:.0f}%) के कारण फफूंद व जीवाणु रोग फैलने का अनुकूल वातावरण है।")

    # 7. Actionable, low-cognitive load recommendations
    actions: List[str] = []
    actions_hindi: List[str] = []

    if flood_risk >= 65:
        actions.append("Avoid any scheduled irrigation immediately.")
        actions_hindi.append("तुरंत किसी भी प्रकार की सिंचाई रोक दें।")
        
        actions.append(f"Open perimeter drainage furrows to protect {profile.crop} root zone.")
        actions_hindi.append(f"{profile.crop} की जड़ों को सड़ने से बचाने के लिए खेत की मेड़ों के किनारे निकास नाली खोलें।")
        
        actions.append("Follow official Flood Management Information System (FMIS) Bihar advisories.")
        actions_hindi.append("बिहार सरकार के बाढ़ प्रबंधन सूचना प्रणाली (FMIS) के आधिकारिक निर्देशों का पालन करें।")
    elif drought_risk >= 65:
        actions.append("Apply micro-irrigation (Drip or Alternate Furrow) in evening hours.")
        actions_hindi.append("शाम के समय ड्रिप या एकांतर नाली विधि से हल्की सिंचाई करें।")
        
        actions.append("Spread straw or dry weed mulch to conserve ground moisture.")
        actions_hindi.append("खेत में नमी रोकने के लिए पुआल या सूखी घास की पलवार (मल्चिंग) बिछाएं।")

    if scan_result and scan_result.severity in ["Moderate", "High", "Severe"]:
        actions.append(f"Monitor crop for {scan_result.possible_issue}. Prepare approved spray once rain subsides.")
        actions_hindi.append(f"{scan_result.hindi_issue} के लक्षणों की निगरानी करें। बारिश रुकते ही अनुशंसित घोल का छिड़काव करें।")

    # 8. Weather-to-Crop Specific Meaning (The Crucial Differentiator)
    if profile.crop == "Maize" and "flowering" in profile.crop_stage.lower():
        meaning = (
            f"Heavy rainfall expected ({env.forecast_rainfall_48h_mm:.1f} mm) during Maize Flowering stage. "
            "Pollen washing and root anoxia can decrease cob grain set by up to 50% if submerged >24 hours."
        )
        meaning_hindi = (
            f"मक्का में मंजर/फूल आने की अवस्था में {env.forecast_rainfall_48h_mm:.1f} मिमी बारिश का पूर्वानुमान है। "
            "24 घंटे से अधिक जलजमाव होने से परागकण धुल सकते हैं और दानों की संख्या आधी रह सकती है।"
        )
    elif profile.crop == "Paddy":
        meaning = (
            f"Current weather provides adequate water for Paddy {profile.crop_stage}, but check drainage outlets "
            "to prevent continuous submergence over 4 days."
        )
        meaning_hindi = (
            f"धान की {profile.crop_stage} अवस्था के लिए वर्षा सहायक है, लेकिन 4 दिन से अधिक जलभराव से बचाव हेतु जलनिकास खुला रखें।"
        )
    else:
        meaning = (
            f"Weather forecast indicates {env.forecast_rainfall_48h_mm:.1f} mm precipitation. "
            f"Adjust nutrient and fungicide timing for {profile.crop}."
        )
        meaning_hindi = (
            f"मौसम पूर्वानुमान {env.forecast_rainfall_48h_mm:.1f} मिमी वर्षा दर्शा रहा है। {profile.crop} में कीटनाशक छिड़काव का समय तदनुसार तय करें।"
        )

    # Primary Threat
    if flood_risk >= 70:
        primary_threat = "Severe Waterlogging & Flash Inundation"
        primary_threat_hindi = "गंभीर जलजमाव व आकस्मिक बाढ़ का खतरा"
    elif drought_risk >= 65:
        primary_threat = "Severe Moisture Stress & Drought Deficit"
        primary_threat_hindi = "गंभीर नमी संकट व सूखे का खतरा"
    elif disease_risk >= 60:
        primary_threat = "High Crop Foliage Disease Spread"
        primary_threat_hindi = "पत्ती रोग के तेजी से फैलने का खतरा"
    else:
        primary_threat = "Moderate Seasonal Weather Fluctuation"
        primary_threat_hindi = "मौसमी उतार-चढ़ाव"

    breakdown = RiskBreakdown(
        flood_risk=flood_risk,
        disease_risk=disease_risk,
        drought_risk=drought_risk,
        excess_rain_risk=excess_rain_risk,
        pest_risk=pest_risk,
        water_stress_risk=water_stress
    )

    return RiskEngineResult(
        overall_khetrakshak_score=overall_score,
        risk_level=risk_level,
        risk_level_hindi=risk_level_hindi,
        breakdown=breakdown,
        primary_threat=primary_threat,
        primary_threat_hindi=primary_threat_hindi,
        why_reasons=why_reasons,
        why_reasons_hindi=why_reasons_hindi,
        weather_to_crop_meaning=meaning,
        weather_to_crop_meaning_hindi=meaning_hindi,
        actionable_recommendations=actions,
        actionable_recommendations_hindi=actions_hindi,
        official_disaster_note="Notice: KhetRakshak AI is an agronomic decision-support platform. Official Bihar Disaster Management Department (DMD) alerts take legal precedence.",
        is_simulated=True
    )
