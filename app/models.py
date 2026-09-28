"""Data models and schemas for KhetRakshak AI.
Bihar's AI-Powered Crop Risk Intelligence Platform.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class FarmProfile(BaseModel):
    farmer_name: str = Field(default="Demo Farmer", description="Farmer Name")
    district: str = Field(default="Purnia", description="District in Bihar")
    village_block: Optional[str] = Field(default="Kasba Block", description="Block or Village")
    crop: str = Field(default="Maize", description="Primary Crop (Maize, Paddy, Wheat, Mustard, etc.)")
    crop_stage: str = Field(default="Flowering", description="Current crop stage (Germination, Vegetative, Flowering, Grain Filling, Maturity)")
    farm_size_acres: float = Field(default=2.5, description="Farm size in acres")
    irrigation_type: str = Field(default="Borewell / Tube-well", description="Irrigation source")
    soil_type: str = Field(default="Alluvial Loam (Khadar)", description="Soil type")
    latitude: Optional[float] = Field(default=25.7771, description="Farm latitude")
    longitude: Optional[float] = Field(default=87.4753, description="Farm longitude")

class ImageQualityResult(BaseModel):
    is_valid: bool
    blur_score: float
    is_blurry: bool
    brightness: float
    is_dark: bool
    is_overexposed: bool
    green_coverage_pct: float
    is_crop_detected: bool
    status_code: str  # 'PASS', 'BLURRY', 'TOO_DARK', 'OVEREXPOSED', 'NOT_CROP'
    message: str
    message_hindi: str
    suggestion: str

class DiseaseDetectionResult(BaseModel):
    crop: str
    possible_issue: str
    hindi_issue: str
    pathogen_type: str  # Fungal, Bacterial, Viral, Pest, Deficiency, Healthy
    confidence: float
    confidence_display: str
    severity: str  # Low, Moderate, Severe, None
    severity_hindi: str
    is_demo: bool = True
    is_low_confidence: bool
    confidence_threshold: float = 0.65
    symptoms: List[str]
    symptoms_hindi: List[str]
    immediate_action: str
    immediate_action_hindi: str
    expert_verification_needed: bool
    disclaimer: str = "Demo prediction based on computer vision feature analysis. Always verify with local Krishi Vigyan Kendra (KVK) before chemical application."

class EnvironmentalFactors(BaseModel):
    district: str
    current_rainfall_mm: float
    forecast_rainfall_48h_mm: float
    river_name: str
    river_level_status: str  # Normal, Near Warning, Above Danger Level, Receding
    soil_moisture_pct: float
    historical_flood_vulnerability: str  # High, Medium, Low
    historical_drought_vulnerability: str  # High, Medium, Low
    temperature_max_c: float
    temperature_min_c: float
    relative_humidity_pct: float
    wind_speed_kmh: float

class RiskBreakdown(BaseModel):
    flood_risk: int = Field(ge=0, le=100)
    disease_risk: int = Field(ge=0, le=100)
    drought_risk: int = Field(ge=0, le=100)
    excess_rain_risk: int = Field(ge=0, le=100)
    pest_risk: int = Field(ge=0, le=100)
    water_stress_risk: int = Field(ge=0, le=100)

class RiskEngineResult(BaseModel):
    overall_khetrakshak_score: int = Field(ge=0, le=100)
    risk_level: str  # 'LOW', 'MODERATE', 'HIGH', 'SEVERE'
    risk_level_hindi: str
    breakdown: RiskBreakdown
    primary_threat: str
    primary_threat_hindi: str
    why_reasons: List[str]
    why_reasons_hindi: List[str]
    weather_to_crop_meaning: str
    weather_to_crop_meaning_hindi: str
    actionable_recommendations: List[str]
    actionable_recommendations_hindi: List[str]
    official_disaster_note: str
    is_simulated: bool = True
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%d %b %Y, %I:%M %p"))

class SmartAlert(BaseModel):
    id: str
    title: str
    title_hindi: str
    category: str  # 'FLOOD', 'DISEASE', 'DROUGHT', 'WEATHER', 'ADVISORY'
    severity: str  # 'CRITICAL', 'WARNING', 'INFO'
    icon: str
    reason: str
    reason_hindi: str
    recommended_action: str
    recommended_action_hindi: str
    district: str
    crop: str
    timestamp: str

class AdvisorMessage(BaseModel):
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: Optional[str] = None

class AdvisorQueryRequest(BaseModel):
    query: str
    language: str = "hi"  # 'hi' or 'en'
    farm_profile: Optional[FarmProfile] = None
    latest_scan_result: Optional[Dict[str, Any]] = None
    current_risk_result: Optional[Dict[str, Any]] = None

class AdvisorQueryResponse(BaseModel):
    response_text: str
    response_hindi: str
    intent_detected: str
    verified_sources: List[str]
    recommended_actions: List[str]
    audio_hint: Optional[str] = None

class DistrictGISInfo(BaseModel):
    id: str
    name: str
    hindi_name: str
    zone: str  # 'North Bihar - Flood Prone', 'South Bihar - Drought Prone', 'Central Bihar'
    river_basin: str
    lat: float
    lng: float
    flood_risk_score: int
    drought_risk_score: int
    overall_crop_risk: int
    current_rainfall_24h_mm: float
    rainfall_anomaly_pct: float
    major_crops: List[str]
    active_alert_level: str  # 'NORMAL', 'ALERT', 'WARNING', 'SEVERE'
    active_alert_message: str
    active_alert_message_hindi: str
