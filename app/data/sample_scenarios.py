"""Predefined demo scenarios for KhetRakshak AI.
Includes the official IDEATEX Bootcamp primary scenario (Purnia Maize Flowering)
and comparative regional scenarios (Gaya Drought, Darbhanga Flood).
"""

from typing import Dict, Any

PRESET_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "ideatex_purnia_maize": {
        "id": "ideatex_purnia_maize",
        "title": "IDEATEX Primary Demo: Purnia Maize (Flowering) + Heavy Rain",
        "description": "Demonstrates the core differentiator: Weather forecast + critical crop stage + flood-prone location + crop leaf symptoms = High Crop Risk.",
        "farmer_name": "Ramesh Kumar Yadav",
        "district": "Purnia",
        "village_block": "Kasba Block, Purnia",
        "crop": "Maize",
        "crop_stage": "Flowering & Tasseling",
        "farm_size_acres": 3.0,
        "irrigation_type": "Borewell / Tube-well",
        "soil_type": "Sandy Loam Alluvium",
        "environmental": {
            "current_rainfall_mm": 68.0,
            "forecast_rainfall_48h_mm": 88.5,
            "river_name": "Kosi / Saura River",
            "river_level_status": "Near Warning Level",
            "soil_moisture_pct": 84.0,
            "historical_flood_vulnerability": "High",
            "historical_drought_vulnerability": "Low",
            "temperature_max_c": 31.5,
            "temperature_min_c": 24.2,
            "relative_humidity_pct": 89.0,
            "wind_speed_kmh": 22.0
        },
        "target_disease": "Maydis Leaf Blight",
        "simulated_disease_confidence": 0.89,
        "sample_query": "मेरे खेत में बहुत बारिश होने वाली है और मक्के में फूल आ रहे हैं, मुझे क्या करना चाहिए?",
        "sample_query_en": "Heavy rain is expected in my area and maize is at flowering stage. What should I do?",
        "sample_audio_response": "पूर्णि‍या में अगले 48 घंटों में भारी बारिश (88 मिमी) की संभावना है। चूंकि आपकी मक्का की फसल फूल आने की अवस्था में है, किसी भी प्रकार की सिंचाई तुरंत रोक दें। जलजमाव से परागकण नष्ट हो सकते हैं, इसलिए खेत के चारों ओर जल निकासी की नाली तैयार रखें। पत्ती पर पर्ण अंगमारी के लक्षण दिखे हैं, बारिश रुकने पर मैंकोजेब का छिड़काव करें।"
    },
    "gaya_drought_paddy": {
        "id": "gaya_drought_paddy",
        "title": "South Bihar Drought: Gaya Paddy (Tillering) + Severe Water Stress",
        "description": "Demonstrates South Bihar contrast: Deficit rainfall (-42%), low groundwater, water stress index high.",
        "farmer_name": "Suresh Manjhi",
        "district": "Gaya",
        "village_block": "Bodh Gaya Block",
        "crop": "Paddy",
        "crop_stage": "Tillering",
        "farm_size_acres": 2.0,
        "irrigation_type": "Check Dam / Tube-well",
        "soil_type": "Old Alluvium / Red Sandy Silt",
        "environmental": {
            "current_rainfall_mm": 2.0,
            "forecast_rainfall_48h_mm": 4.5,
            "river_name": "Falgu River (Dry bed)",
            "river_level_status": "Normal / Low Flow",
            "soil_moisture_pct": 28.0,
            "historical_flood_vulnerability": "Low",
            "historical_drought_vulnerability": "High",
            "temperature_max_c": 38.0,
            "temperature_min_c": 27.0,
            "relative_humidity_pct": 42.0,
            "wind_speed_kmh": 14.0
        },
        "target_disease": "Brown Spot",
        "simulated_disease_confidence": 0.82,
        "sample_query": "गया में बारिश नहीं हो रही है, धान के कल्ले सूख रहे हैं। क्या उपाय करें?",
        "sample_query_en": "No rainfall in Gaya, paddy tillers are drying up. What should I do?",
        "sample_audio_response": "गया में पिछले 3 हफ्तों से बारिश की भारी कमी है। धान में कल्ले फूटने के समय नमी अत्यंत आवश्यक है। खेत में दरारें न पड़ने दें, संभव हो तो एकांतर गीला-सूखा (AWD) सिंचाई विधि अपनाएं। पोटाश का छिड़काव करें ताकि फसल सूखे को सहन कर सके।"
    },
    "darbhanga_kamla_flood": {
        "id": "darbhanga_kamla_flood",
        "title": "North Bihar Flood: Darbhanga (Kamla Balan Overflow) + Bacterial Blight",
        "description": "River above danger mark, extreme flood inundation, bacterial leaf blight threat.",
        "farmer_name": "Maheshwar Jha",
        "district": "Darbhanga",
        "village_block": "Biraul Block",
        "crop": "Paddy",
        "crop_stage": "Panicle Initiation & Booting",
        "farm_size_acres": 4.5,
        "irrigation_type": "Canal / River lift",
        "soil_type": "Heavy Clay Loam / Chaur",
        "environmental": {
            "current_rainfall_mm": 82.0,
            "forecast_rainfall_48h_mm": 95.0,
            "river_name": "Kamla Balan River",
            "river_level_status": "Above Danger Level",
            "soil_moisture_pct": 96.0,
            "historical_flood_vulnerability": "Severe",
            "historical_drought_vulnerability": "Low",
            "temperature_max_c": 29.0,
            "temperature_min_c": 23.5,
            "relative_humidity_pct": 94.0,
            "wind_speed_kmh": 26.0
        },
        "target_disease": "Bacterial Leaf Blight",
        "simulated_disease_confidence": 0.91,
        "sample_query": "कमला बलान नदी का पानी बढ़ गया है और धान में झुलसा लग रहा है।",
        "sample_query_en": "Kamla Balan river level is rising and paddy has blight symptoms.",
        "sample_audio_response": "दरभंगा में कमला बलान नदी खतरे के निशान से ऊपर है। निचले खेतों में जल निकासी तुरंत खोलें। अतिरिक्त यूरिया बिल्कुल न डालें क्योंकि इससे जीवाणु झुलसा और तेजी से फैलता है। मौसम खुलते ही स्ट्रेप्टोसाइक्लिन और कॉपर ऑक्सीक्लोराइड का छिड़काव करें।"
    }
}
