"""KhetRakshak AI (खेतरक्षक AI)
Bihar's AI-Powered Crop Risk Intelligence & Early-Warning Platform.
Developed for IDEATEX Bootcamp — Ideas x AI x Impact
Startup Cell x AI Club, IIIT Bhagalpur
"""

import os
import io
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models import (
    FarmProfile,
    EnvironmentalFactors,
    AdvisorQueryRequest,
    AdvisorQueryResponse,
    DiseaseDetectionResult,
    RiskEngineResult
)
from app.data.bihar_districts import BIHAR_DISTRICTS
from app.data.crop_agronomy import CROPS_AGRONOMY
from app.data.sample_scenarios import PRESET_SCENARIOS
from app.ai.crop_vision import check_image_quality, analyze_crop_disease
from app.ai.risk_engine import evaluate_crop_risk
from app.ai.weather_crop_intelligence import interpret_weather_for_crop
from app.ai.rag_advisor import answer_farmer_query
from app.storage import (
    init_db,
    get_profile,
    update_profile,
    get_scan_timeline,
    add_scan_history,
    get_alerts,
    get_admin_metrics
)

app = FastAPI(
    title="KhetRakshak AI",
    description="Bihar's AI-Powered Crop Risk Intelligence & Early-Warning Platform",
    version="1.0.0"
)

# Enable CORS for maximum flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# In-memory session state for active environmental parameters (defaults to Purnia scenario)
active_environmental = EnvironmentalFactors(
    district="Purnia",
    current_rainfall_mm=68.0,
    forecast_rainfall_48h_mm=88.5,
    river_name="Kosi / Saura River",
    river_level_status="Near Warning Level",
    soil_moisture_pct=84.0,
    historical_flood_vulnerability="High",
    historical_drought_vulnerability="Low",
    temperature_max_c=31.5,
    temperature_min_c=24.2,
    relative_humidity_pct=89.0,
    wind_speed_kmh=22.0
)

# Latest scan result cache
latest_scan_result: Optional[DiseaseDetectionResult] = None

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>KhetRakshak AI Starting...</h1>")

@app.get("/api/profile", response_model=FarmProfile)
async def read_profile():
    return get_profile()

@app.post("/api/profile", response_model=FarmProfile)
async def write_profile(profile: FarmProfile):
    updated = update_profile(profile)
    # Update active environmental baseline if district changed
    d_data = BIHAR_DISTRICTS.get(profile.district)
    if d_data:
        active_environmental.district = profile.district
        active_environmental.historical_flood_vulnerability = "High" if d_data["historical_flood_risk"] > 60 else "Low"
        active_environmental.historical_drought_vulnerability = "High" if d_data["historical_drought_risk"] > 60 else "Low"
        active_environmental.current_rainfall_mm = d_data["current_rainfall_24h_mm"]
        active_environmental.river_name = d_data["river_basin"]
    return updated

@app.get("/api/scenarios")
async def list_scenarios():
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "description": s["description"],
            "district": s["district"],
            "crop": s["crop"],
            "crop_stage": s["crop_stage"]
        }
        for s in PRESET_SCENARIOS.values()
    ]

@app.post("/api/load-scenario/{scenario_id}")
async def load_preset_scenario(scenario_id: str):
    global active_environmental, latest_scan_result
    scenario = PRESET_SCENARIOS.get(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Update profile
    prof = FarmProfile(
        farmer_name=scenario["farmer_name"],
        district=scenario["district"],
        village_block=scenario["village_block"],
        crop=scenario["crop"],
        crop_stage=scenario["crop_stage"],
        farm_size_acres=scenario["farm_size_acres"],
        irrigation_type=scenario["irrigation_type"],
        soil_type=scenario["soil_type"]
    )
    update_profile(prof)

    # Update environmental parameters
    env_data = scenario["environmental"]
    active_environmental = EnvironmentalFactors(
        district=scenario["district"],
        current_rainfall_mm=env_data["current_rainfall_mm"],
        forecast_rainfall_48h_mm=env_data["forecast_rainfall_48h_mm"],
        river_name=env_data["river_name"],
        river_level_status=env_data["river_level_status"],
        soil_moisture_pct=env_data["soil_moisture_pct"],
        historical_flood_vulnerability=env_data["historical_flood_vulnerability"],
        historical_drought_vulnerability=env_data["historical_drought_vulnerability"],
        temperature_max_c=env_data["temperature_max_c"],
        temperature_min_c=env_data["temperature_min_c"],
        relative_humidity_pct=env_data["relative_humidity_pct"],
        wind_speed_kmh=env_data["wind_speed_kmh"]
    )

    # Pre-load simulated disease scan
    target_dis = scenario["target_disease"]
    crop_info = CROPS_AGRONOMY.get(scenario["crop"], CROPS_AGRONOMY["Maize"])
    disease_entry = crop_info["diseases"].get(target_dis, list(crop_info["diseases"].values())[0])

    latest_scan_result = DiseaseDetectionResult(
        crop=scenario["crop"],
        possible_issue=target_dis,
        hindi_issue=disease_entry.get("hindi_name", target_dis),
        pathogen_type=disease_entry.get("pathogen", "Fungus"),
        confidence=scenario.get("simulated_disease_confidence", 0.89),
        confidence_display=f"{int(scenario.get('simulated_disease_confidence', 0.89) * 100)}%",
        severity="Moderate",
        severity_hindi="मध्यम",
        is_demo=True,
        is_low_confidence=False,
        confidence_threshold=0.65,
        symptoms=disease_entry.get("symptoms", []),
        symptoms_hindi=disease_entry.get("symptoms_hindi", []),
        immediate_action=disease_entry.get("immediate_action", "Drain standing water immediately."),
        immediate_action_hindi=disease_entry.get("immediate_action_hindi", "खेत से तुरंत अतिरिक्त पानी निकालें।"),
        expert_verification_needed=True,
        disclaimer="Demo scenario preset for IDEATEX demonstration."
    )

    # Compute risk
    risk = evaluate_crop_risk(prof, active_environmental, latest_scan_result)

    return {
        "status": "success",
        "scenario": scenario,
        "profile": prof,
        "environmental": active_environmental,
        "scan_result": latest_scan_result,
        "risk_result": risk
    }

class ScanCropJsonRequest(BaseModel):
    image_base64: Optional[str] = None
    sample_key: Optional[str] = None
    crop: str = "Maize"
    crop_stage: str = "Flowering"
    simulate_low_confidence: bool = False

@app.post("/api/scan-crop-json")
async def scan_crop_json(payload: ScanCropJsonRequest):
    global latest_scan_result
    import base64
    image_bytes = None
    
    if payload.image_base64:
        data = payload.image_base64
        if "," in data:
            data = data.split(",", 1)[1]
        try:
            image_bytes = base64.b64decode(data)
        except Exception:
            pass

    if not image_bytes and payload.sample_key:
        sample_path = os.path.join(STATIC_DIR, "sample_images", f"{payload.sample_key}.jpg")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()

    if not image_bytes:
        sample_path = os.path.join(STATIC_DIR, "sample_images", "maize_maydis_blight.jpg")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()
        else:
            raise HTTPException(status_code=400, detail="No image provided")

    quality, _ = check_image_quality(image_bytes)
    result = analyze_crop_disease(
        image_bytes=image_bytes,
        crop=payload.crop,
        crop_stage=payload.crop_stage,
        simulate_low_confidence=payload.simulate_low_confidence
    )
    latest_scan_result = result

    add_scan_history({
        "crop": payload.crop,
        "crop_stage": payload.crop_stage,
        "possible_issue": result.possible_issue,
        "hindi_issue": result.hindi_issue,
        "confidence": result.confidence,
        "severity": result.severity,
        "overall_score": 72 if result.severity != "None" else 28,
        "risk_level": "HIGH" if result.severity != "None" else "LOW",
        "notes": result.immediate_action
    })

    return {
        "quality": quality,
        "diagnosis": result
    }

@app.post("/api/scan-crop")
async def scan_crop_image(
    file: Optional[UploadFile] = File(None),
    sample_key: Optional[str] = Form(None),
    crop: str = Form("Maize"),
    crop_stage: str = Form("Flowering"),
    simulate_low_confidence: bool = Form(False)
):
    global latest_scan_result
    image_bytes = None

    if file and file.filename:
        image_bytes = await file.read()
    elif sample_key:
        sample_path = os.path.join(STATIC_DIR, "sample_images", f"{sample_key}.jpg")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()

    if not image_bytes:
        # Fallback to default sample
        sample_path = os.path.join(STATIC_DIR, "sample_images", "maize_maydis_blight.jpg")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()
        else:
            raise HTTPException(status_code=400, detail="No image provided")

    # Step 1: Image Quality Inspection
    quality, _ = check_image_quality(image_bytes)

    # Step 2: Disease Diagnosis (respecting low-confidence handling)
    result = analyze_crop_disease(
        image_bytes=image_bytes,
        crop=crop,
        crop_stage=crop_stage,
        simulate_low_confidence=simulate_low_confidence
    )
    latest_scan_result = result

    # Log into history timeline
    add_scan_history({
        "crop": crop,
        "crop_stage": crop_stage,
        "possible_issue": result.possible_issue,
        "hindi_issue": result.hindi_issue,
        "confidence": result.confidence,
        "severity": result.severity,
        "overall_score": 72 if result.severity != "None" else 28,
        "risk_level": "HIGH" if result.severity != "None" else "LOW",
        "notes": result.immediate_action
    })

    return {
        "quality": quality,
        "diagnosis": result
    }

@app.get("/api/risk-evaluation")
async def get_current_risk():
    prof = get_profile()
    risk = evaluate_crop_risk(prof, active_environmental, latest_scan_result)
    return {
        "profile": prof,
        "environmental": active_environmental,
        "scan_result": latest_scan_result,
        "risk": risk
    }

@app.get("/api/weather-to-crop")
async def get_weather_to_crop():
    prof = get_profile()
    intelligence = interpret_weather_for_crop(prof, active_environmental)
    return intelligence

@app.post("/api/ask-advisor", response_model=AdvisorQueryResponse)
async def ask_advisor(request: AdvisorQueryRequest):
    if not request.farm_profile:
        request.farm_profile = get_profile()
    response = answer_farmer_query(request)
    return response

@app.post("/api/voice-query")
async def process_voice_query(data: Dict[str, Any]):
    transcript = data.get("transcript", "").strip()
    language = data.get("language", "hi")
    
    if not transcript:
        return JSONResponse({"status": "error", "message": "No voice transcript received"}, status_code=400)

    prof = get_profile()
    advisor_req = AdvisorQueryRequest(
        query=transcript,
        language=language,
        farm_profile=prof
    )
    res = answer_farmer_query(advisor_req)

    return {
        "status": "success",
        "transcript": transcript,
        "language": language,
        "intent": res.intent_detected,
        "response_text": res.response_text,
        "response_hindi": res.response_hindi,
        "audio_spoken_text": res.response_hindi if language == "hi" else res.response_text,
        "sources": res.verified_sources,
        "actions": res.recommended_actions
    }

@app.get("/api/districts-gis")
async def get_districts_gis():
    return list(BIHAR_DISTRICTS.values())

@app.get("/api/alerts")
async def get_active_alerts():
    return get_alerts()

@app.get("/api/timeline")
async def get_timeline():
    return get_scan_timeline()

@app.get("/api/admin/metrics")
async def get_admin_dashboard():
    return get_admin_metrics()

@app.get("/api/crop-catalog")
async def get_crop_catalog():
    return CROPS_AGRONOMY
