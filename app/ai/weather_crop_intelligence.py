"""Weather-to-Crop Intelligence Engine for KhetRakshak AI.
Translates raw meteorological forecasts into crop-specific agronomic implications.

Formula:
Weather + Crop Type + Growth Stage + Soil Saturation + Location = Field-Level Consequence
"Weather tells you what is coming. Crop detection tells you what is happening.
 KhetRakshak tells you what it means for your farm."
"""

from typing import Dict, Any, List
from app.models import FarmProfile, EnvironmentalFactors

def interpret_weather_for_crop(
    profile: FarmProfile,
    env: EnvironmentalFactors
) -> Dict[str, Any]:
    """Generates the crop-specific impact analysis of current weather forecasts."""
    crop = profile.crop
    stage = profile.crop_stage
    forecast_rain = env.forecast_rainfall_48h_mm
    soil_moisture = env.soil_moisture_pct
    temp_max = env.temperature_max_c
    humidity = env.relative_humidity_pct
    wind_speed = env.wind_speed_kmh

    # 1. Irrigation Directive
    if forecast_rain >= 25.0 or soil_moisture >= 75.0:
        irrigation_status = "HALT"
        irrigation_directive = "⛔ STOP ALL IRRIGATION: Soil is saturated and incoming rain will cause root flooding."
        irrigation_directive_hindi = "⛔ तुरंत सभी सिंचाई बंद करें: खेत में पहले से नमी है और बारिश से जलभराव हो सकता है।"
    elif soil_moisture <= 35.0 and forecast_rain < 10.0:
        irrigation_status = "URGENT"
        irrigation_directive = "💧 CRITICAL IRRIGATION REQUIRED: Root zone moisture is depleting below field capacity."
        irrigation_directive_hindi = "💧 तुरंत हल्की सिंचाई करें: मिट्टी में नमी खतरनाक स्तर तक गिर चुकी है।"
    else:
        irrigation_status = "NORMAL"
        irrigation_directive = "ℹ️ NORMAL MOISTURE: Maintain standard scheduled watering as per crop stage."
        irrigation_directive_hindi = "ℹ️ नमी सामान्य: सामान्य अंतराल पर सिंचाई जारी रखें।"

    # 2. Spraying Window Directive
    if forecast_rain > 15.0 or wind_speed > 20.0:
        spray_status = "UNFAVORABLE"
        spray_advice = "❌ DO NOT SPRAY CHEMICALS: Rain will wash off active ingredients within 24h, wasting money."
        spray_advice_hindi = "❌ कीटनाशक/फफूंदनाशी का छिड़काव न करें: बारिश और तेज हवा से दवा धुल जाएगी।"
    elif humidity > 85.0 and temp_max > 26.0:
        spray_status = "PREPARE"
        spray_advice = "⚠️ HIGH DISEASE RISK COMING: High humidity favors fungal spores. Keep sprayers ready once leaves dry."
        spray_advice_hindi = "⚠️ बीमारी का खतरा बढ़ रहा है: अधिक उमस में फफूंद पनपती है। बारिश रुकते ही छिड़काव की तैयारी रखें।"
    else:
        spray_status = "FAVORABLE"
        spray_advice = "✅ SAFE SPRAY WINDOW: Calm winds and dry conditions allow effective foliar spray."
        spray_advice_hindi = "✅ छिड़काव के लिए अनुकूल समय: शांत हवा और सूखे मौसम में दवा का पूरा असर होगा।"

    # 3. Specific Agronomic Consequence Analysis
    consequence_title = f"What {forecast_rain:.0f}mm Rain Means for Your {stage} {crop}"
    consequence_title_hindi = f"आपकी {stage} {crop} पर {forecast_rain:.0f}मिमी बारिश का वास्तविक प्रभाव"

    points: List[Dict[str, str]] = []

    if crop == "Maize":
        if "flowering" in stage.lower() or "tassel" in stage.lower():
            points.append({
                "factor": "Pollen & Cob Development",
                "factor_hindi": "परागकण व भुट्टे का विकास",
                "impact": "SEVERE RISK",
                "explanation": "Flowering maize has zero tolerance for water stagnation. Submergence for >24h starves roots of oxygen and halts silking, causing up to 50% barren cobs.",
                "explanation_hindi": "मक्का में फूल आने के समय 24 घंटे से ज्यादा पानी रुकने से जड़ें सड़ने लगती हैं और भुट्टों में दाने नहीं बनते (50% तक नुकसान)।"
            })
            points.append({
                "factor": "Foliage Blight Incubation",
                "factor_hindi": "पर्ण अंगमारी फफूंद",
                "impact": "HIGH RISK",
                "explanation": f"Humidity of {humidity:.0f}% combined with warm 31°C temp triggers Maydis leaf blight spore germination.",
                "explanation_hindi": f"{humidity:.0f}% आर्द्रता और 31°C तापमान में पर्ण अंगमारी के फफूंद तेजी से फैलते हैं।"
            })
        else:
            points.append({
                "factor": "Root Zone Aeration",
                "factor_hindi": "जड़ों में वायु संचार",
                "impact": "MODERATE",
                "explanation": "Maize requires well-drained loam. Standing water over 48h turns leaves yellow from nitrogen leaching.",
                "explanation_hindi": "मक्के को जलभराव बिल्कुल पसंद नहीं है। 48 घंटे पानी रुकने से पत्तियां पीली पड़ जाती हैं।"
            })
    elif crop == "Paddy":
        if soil_moisture < 40.0:
            points.append({
                "factor": "Tiller Desiccation",
                "factor_hindi": "कल्लों का सूखना",
                "impact": "CRITICAL RISK",
                "explanation": "Lack of water during vegetative phase prevents tiller multiplication, reducing harvest yield.",
                "explanation_hindi": "कल्ले फूटने के समय पानी की कमी से बालियों की संख्या कम हो जाएगी।"
            })
        else:
            points.append({
                "factor": "Water Inundation Threshold",
                "factor_hindi": "जलभराव सहन सीमा",
                "impact": "MANAGEABLE",
                "explanation": "Paddy can tolerate 5-10cm standing water, but ensure submergence does not exceed 5 days continuously.",
                "explanation_hindi": "धान 5-10 सेमी पानी सहन कर सकता है, परंतु फसल 5 दिन से अधिक जलमग्न न रहने पाए।"
            })
    elif crop == "Potato":
        points.append({
            "factor": "Late Blight Rapid Epidemic",
            "factor_hindi": "पछेती झुलसा का प्रकोप",
            "impact": "EXTREME RISK",
            "explanation": "Cold humid conditions can destroy an entire potato foliage canopy within 72 hours via Phytophthora.",
            "explanation_hindi": "ठंडे और नमी वाले मौसम में लेट ब्लाइट 72 घंटे में पूरी फसल को झुलसा सकती है।"
        })
    else:
        points.append({
            "factor": "Field Soil Mechanics",
            "factor_hindi": "मिट्टी की स्थिति",
            "impact": "MODERATE",
            "explanation": f"Current weather pattern requires proactive vigilance on {crop} fields.",
            "explanation_hindi": f"वर्तमान मौसम में {crop} के खेत की निरंतर निगरानी आवश्यक है।"
        })

    return {
        "irrigation_status": irrigation_status,
        "irrigation_directive": irrigation_directive,
        "irrigation_directive_hindi": irrigation_directive_hindi,
        "spray_status": spray_status,
        "spray_advice": spray_advice,
        "spray_advice_hindi": spray_advice_hindi,
        "consequence_title": consequence_title,
        "consequence_title_hindi": consequence_title_hindi,
        "points": points,
        "district": profile.district,
        "crop": crop,
        "crop_stage": stage,
        "forecast_rain_mm": forecast_rain,
        "soil_moisture_pct": soil_moisture
    }
