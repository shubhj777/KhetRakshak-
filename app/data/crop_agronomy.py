"""Agronomic knowledge base for Bihar crops, growth stages, waterlogging vulnerability,
drought vulnerability, and disease profiles.
"""

from typing import Dict, Any, List

CROPS_AGRONOMY: Dict[str, Dict[str, Any]] = {
    "Maize": {
        "hindi_name": "मक्का (Makka)",
        "scientific_name": "Zea mays",
        "primary_season": "Kharif & Rabi (North Bihar / Seemanchal is known as Maize Granary)",
        "water_sensitivity": "HIGHLY SENSITIVE to waterlogging, especially at Flowering/Tasseling stage",
        "stages": [
            {
                "name": "Germination & Seedling",
                "hindi_name": "अंकुरण व प्रारंभिक अवस्था (0-15 दिन)",
                "waterlogging_tolerance_days": 1,
                "drought_tolerance": "MODERATE",
                "water_stress_impact": "Stunted shoot and poor root establishment",
                "flood_risk_multiplier": 1.4
            },
            {
                "name": "Vegetative (Knee-high)",
                "hindi_name": "वानस्पतिक अवस्था / घुटने तक (15-40 दिन)",
                "waterlogging_tolerance_days": 2,
                "drought_tolerance": "MODERATE",
                "water_stress_impact": "Reduced leaf canopy and delayed tassel emergence",
                "flood_risk_multiplier": 1.2
            },
            {
                "name": "Flowering & Tasseling",
                "hindi_name": "फूल आने व मंजर अवस्था (40-65 दिन)",
                "waterlogging_tolerance_days": 0.5,  # Extremely sensitive
                "drought_tolerance": "CRITICAL",
                "water_stress_impact": "Anthesis-silking interval (ASI) widening, pollen sterility, severe cob abortion",
                "flood_risk_multiplier": 1.8  # Critical vulnerability!
            },
            {
                "name": "Grain Filling / Milking",
                "hindi_name": "दाने भरने की अवस्था (65-90 दिन)",
                "waterlogging_tolerance_days": 1.5,
                "drought_tolerance": "HIGH",
                "water_stress_impact": "Shriveled grains, low test-weight",
                "flood_risk_multiplier": 1.3
            },
            {
                "name": "Maturity & Harvesting",
                "hindi_name": "परिपक्वता व कटाई (90-110 दिन)",
                "waterlogging_tolerance_days": 3,
                "drought_tolerance": "HIGH",
                "water_stress_impact": "Pre-harvest cob rotting if standing water persists",
                "flood_risk_multiplier": 1.5
            }
        ],
        "diseases": {
            "Maydis Leaf Blight": {
                "hindi_name": "मेडीस लीफ ब्लाइट (पर्ण अंगमारी)",
                "pathogen": "Bipolaris maydis (Fungus)",
                "symptoms": [
                    "Small oval to rectangular water-soaked lesions on leaves",
                    "Lesions elongate between veins into straw-colored necrotic areas",
                    "Dark brown or purple borders on mature spots"
                ],
                "symptoms_hindi": [
                    "पत्तियों पर छोटे अंडाकार पानी से भीगे भूरे धब्बे",
                    "धब्बे नसों के बीच लंबे भूरे-पीले रूप में फैलते हैं",
                    "पुराने धब्बों के किनारे गहरे कत्थई रंग के हो जाते हैं"
                ],
                "favorable_weather": "High humidity (>85%), warm temps (26-32°C), continuous rainfall",
                "immediate_action": "Drain standing water immediately. Apply Mancozeb 75% WP @ 2.5g/liter or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1ml/liter.",
                "immediate_action_hindi": "खेत से तुरंत अतिरिक्त पानी निकालें। मैंकोजेब 75% WP (2.5 ग्राम/लीटर) या एज़ोक्सीस्ट्रोबिन + डिफेनोकोनाज़ोल (1 मिली/लीटर) का छिड़काव करें।",
                "organic_remedy": "Neem oil spray (5ml/L) + Trichoderma viride soil application"
            },
            "Turcicum Leaf Blight": {
                "hindi_name": "टर्सिकम पर्ण अंगमारी",
                "pathogen": "Exserohilum turcicum (Fungus)",
                "symptoms": [
                    "Large, elliptical or cigar-shaped grayish-green lesions (2.5 - 15 cm)",
                    "Leaves appear scorched or burned during severe infestation"
                ],
                "symptoms_hindi": [
                    "पत्तियों पर सिगार के आकार के लंबे भूरे-धूसर धब्बे",
                    "गंभीर स्थिति में पत्तियां जली हुई प्रतीत होती हैं"
                ],
                "favorable_weather": "Moderate temperatures (20-25°C) with persistent fog or dew",
                "immediate_action": "Spray Propiconazole 25% EC @ 1ml/L at early lesion onset.",
                "immediate_action_hindi": "प्रारंभिक लक्षण दिखने पर प्रोपिकोनाज़ोल 25% EC (1 मिली/लीटर) का छिड़काव करें।"
            },
            "Fall Armyworm": {
                "hindi_name": "फॉल आर्मीवर्म (सैनिक कीट)",
                "pathogen": "Spodoptera frugiperda (Pest)",
                "symptoms": [
                    "Ragged shot-hole feeding on leaves in central whorl",
                    "Heavy sawdust-like larval fecal frass in the plant whorl"
                ],
                "symptoms_hindi": [
                    "पौधे के गोफ (केंद्रीय भंवर) में पत्तियों पर बड़े कटे-फटे छेद",
                    "गोफ में लकड़ी के बुरादे जैसी विष्ठा"
                ],
                "favorable_weather": "Warm dry spells followed by rain",
                "immediate_action": "Whol application of Chlorantraniliprole 18.5% SC @ 0.4ml/L or Emamectin Benzoate 5% SG @ 0.5g/L.",
                "immediate_action_hindi": "गोफ में क्लोरेंट्रानिलिप्रोल (0.4 मिली/लीटर) या एमामेक्टिन बेंजोएट (0.5 ग्राम/लीटर) का घोल डालें।"
            },
            "Healthy Maize": {
                "hindi_name": "स्वस्थ मक्का फसल",
                "pathogen": "None",
                "symptoms": ["Uniform green leaf pigmentation, erect leaves, healthy tassel, no visible lesions"],
                "symptoms_hindi": ["एकसमान हरी पत्तियां, कोई धब्बे या कीट के लक्षण नहीं"],
                "favorable_weather": "Optimum sunny weather with balanced moisture",
                "immediate_action": "Maintain optimal root aeration and continue standard fertigation.",
                "immediate_action_hindi": "खेत में उचित नमी बनाए रखें और सामान्य उर्वरक प्रबंधन जारी रखें।"
            }
        }
    },
    "Paddy": {
        "hindi_name": "धान (Dhan)",
        "scientific_name": "Oryza sativa",
        "primary_season": "Kharif (Aman, Aus, Boro in Bihar)",
        "water_sensitivity": "Needs water, but submerged deep flooding for >7 days damages non-submergence varieties",
        "stages": [
            {"name": "Nursery / Seedling", "hindi_name": "नर्सरी अवस्था (0-25 दिन)", "waterlogging_tolerance_days": 3, "drought_tolerance": "CRITICAL", "water_stress_impact": "Seedling desiccation, poor tillering", "flood_risk_multiplier": 1.3},
            {"name": "Tillering", "hindi_name": "कल्ले फूटने की अवस्था (25-50 दिन)", "waterlogging_tolerance_days": 6, "drought_tolerance": "MODERATE", "water_stress_impact": "Reduced effective panicle-bearing tillers", "flood_risk_multiplier": 1.1},
            {"name": "Panicle Initiation & Booting", "hindi_name": "गाभा व बाली निकलने की अवस्था (50-75 दिन)", "waterlogging_tolerance_days": 4, "drought_tolerance": "CRITICAL", "water_stress_impact": "Spikelet sterility, incomplete heading", "flood_risk_multiplier": 1.5},
            {"name": "Flowering & Grain Filling", "hindi_name": "फूल आने व दूधिया अवस्था (75-100 दिन)", "waterlogging_tolerance_days": 3, "drought_tolerance": "HIGH", "water_stress_impact": "Chaffy grains, low grain weight", "flood_risk_multiplier": 1.4},
            {"name": "Maturity", "hindi_name": "कटाई अवस्था (100-120 दिन)", "waterlogging_tolerance_days": 5, "drought_tolerance": "HIGH", "water_stress_impact": "Grain shattering or viviparous sprouting in flood", "flood_risk_multiplier": 1.6}
        ],
        "diseases": {
            "Bacterial Leaf Blight": {
                "hindi_name": "जीवाणु झुलसा (बैक्टीरियल ब्लाइट)",
                "pathogen": "Xanthomonas oryzae pv. oryzae (Bacteria)",
                "symptoms": ["Wavy water-soaked stripes along leaf margins turning yellow-white", "Milky bacterial ooze beads on young leaves in humid mornings"],
                "symptoms_hindi": ["पत्तियों के किनारों से लहरदार पीले-सफेद धारियां", "सुबह के समय पत्तियों पर दूधिया जीवाणु बूंदें"],
                "favorable_weather": "Heavy rain, typhoons/strong winds, temperatures 25-34°C, excess nitrogen",
                "immediate_action": "Drain water for 3-4 days. Withhold urea top-dressing. Spray Streptocycline @ 6g + Copper Oxychloride @ 500g in 200L water per acre.",
                "immediate_action_hindi": "खेत का पानी 3-4 दिन निकाल दें। यूरिया न डालें। स्ट्रेप्टोसाइक्लिन 6 ग्राम + कॉपर ऑक्सीक्लोराइड 500 ग्राम प्रति एकड़ छिड़कें।",
                "organic_remedy": "Cow dung filtrate (20%) spray or Pseudomonas fluorescens @ 5g/L"
            },
            "Rice Blast": {
                "hindi_name": "धान का झोंका रोग (ब्लास्ट)",
                "pathogen": "Magnaporthe oryzae (Fungus)",
                "symptoms": ["Diamond or spindle-shaped lesions with grayish centers and brown borders", "Neck rot breaking panicles"],
                "symptoms_hindi": ["नाव या आंख के आकार के धब्बे जिनका केंद्र राख रंग का और किनारे कत्थई होते हैं", "गर्दन तोड़ लक्षण"],
                "favorable_weather": "Night temp 20-24°C with relative humidity >90%, intermittent showers",
                "immediate_action": "Spray Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L.",
                "immediate_action_hindi": "ट्राइसाइक्लाजोल 75% WP (0.6 ग्राम/लीटर) या आइसोप्रोपाइल 40% EC का छिड़काव करें।"
            },
            "Brown Spot": {
                "hindi_name": "भूरा धब्बा रोग (ब्राउन स्पॉट)",
                "pathogen": "Bipolaris oryzae (Fungus)",
                "symptoms": ["Small circular to oval sesame-seed shaped brown spots with yellow halo", "Prevalent in low fertility soils with water deficit"],
                "symptoms_hindi": ["तिल के दाने जैसे गोल-अंडाकार भूरे धब्बे जिनके चारों ओर पीला छल्ला होता है", "कम उर्वरक व सूखे वाले खेतों में अधिक"],
                "favorable_weather": "Drought stress followed by high humidity",
                "immediate_action": "Apply balanced potassium fertilizer. Spray Propiconazole 25% EC @ 1ml/L.",
                "immediate_action_hindi": "खेत में पोटाश की कमी पूरी करें। प्रोपिकोनाज़ोल 25% EC (1 मिली/लीटर) छिड़कें।"
            },
            "Healthy Paddy": {
                "hindi_name": "स्वस्थ धान फसल",
                "pathogen": "None",
                "symptoms": ["Clean vibrant green blades, healthy tillers, no lesions"],
                "symptoms_hindi": ["स्वस्थ हरी पत्तियां, मजबूत कल्ले, कोई रोग लक्षण नहीं"],
                "favorable_weather": "Adequate sunshine with controlled 3-5 cm water layer",
                "immediate_action": "Maintain optimal standing water depth of 2-4 cm.",
                "immediate_action_hindi": "खेत में 2-4 सेमी पानी का स्तर बनाए रखें।"
            }
        }
    },
    "Wheat": {
        "hindi_name": "गेहूं (Gehun)",
        "scientific_name": "Triticum aestivum",
        "primary_season": "Rabi (Major crop across Central & South Bihar plains)",
        "water_sensitivity": "Needs 4-6 timed irrigations (CRI, Tillering, Booting, Milking), sensitive to terminal heat",
        "stages": [
            {"name": "Crown Root Initiation (CRI)", "hindi_name": "शिखर जड़ अवस्था / सीआरआई (20-25 दिन)", "waterlogging_tolerance_days": 1, "drought_tolerance": "CRITICAL", "water_stress_impact": "Critical stage: 30% yield loss if dry", "flood_risk_multiplier": 1.4},
            {"name": "Tillering & Jointing", "hindi_name": "कल्ले व गांठ बनने की अवस्था (40-60 दिन)", "waterlogging_tolerance_days": 2, "drought_tolerance": "MODERATE", "water_stress_impact": "Fewer productive spikes", "flood_risk_multiplier": 1.2},
            {"name": "Flowering & Anthesis", "hindi_name": "फूल आने की अवस्था (70-85 दिन)", "waterlogging_tolerance_days": 2, "drought_tolerance": "CRITICAL", "water_stress_impact": "Pollen desiccation from westerly dry winds (Loo)", "flood_risk_multiplier": 1.3},
            {"name": "Grain Filling / Milking", "hindi_name": "दाने भरने की अवस्था (85-105 दिन)", "waterlogging_tolerance_days": 3, "drought_tolerance": "HIGH", "water_stress_impact": "Terminal heat forced maturity, shriveled grains", "flood_risk_multiplier": 1.2},
            {"name": "Maturity", "hindi_name": "परिपक्वता (105-125 दिन)", "waterlogging_tolerance_days": 3, "drought_tolerance": "HIGH", "water_stress_impact": "Pre-harvest rain causes lodging & sprouting", "flood_risk_multiplier": 1.5}
        ],
        "diseases": {
            "Yellow Rust": {
                "hindi_name": "पीला रतुआ (येलो रस्ट)",
                "pathogen": "Puccinia striiformis (Fungus)",
                "symptoms": ["Bright yellow linear stripes of powdery pustules arranged in rows on leaf surface", "Rubbing leaf leaves yellow powder on fingers"],
                "symptoms_hindi": ["पत्तियों पर कतारबद्ध चमकदार पीले चूर्ण के फफोले", "पत्ती छूने पर उंगली पर पीला पाउडर लगना"],
                "favorable_weather": "Cool humid weather (10-18°C), prolonged winter dew/fog",
                "immediate_action": "Spray Tebuconazole 25.9% EC @ 1ml/L or Propiconazole 25% EC @ 1ml/L immediately.",
                "immediate_action_hindi": "टेबुकोनाज़ोल या प्रोपिकोनाज़ोल (1 मिली/लीटर) का तुरंत छिड़काव करें।"
            },
            "Spot Blotch": {
                "hindi_name": "पर्ण झुलसा (स्पॉट ब्लॉच)",
                "pathogen": "Bipolaris sorokiniana (Fungus)",
                "symptoms": ["Brown oval spots with yellow halo, drying from leaf tip backwards", "Severe in Eastern Gangetic Plains"],
                "symptoms_hindi": ["पत्तियों के सिरे से सूखना, पीले घेरे वाले भूरे धब्बे"],
                "favorable_weather": "High temperatures during late grain filling",
                "immediate_action": "Spray Mancozeb @ 2.5g/L or Azoxystrobin @ 1ml/L.",
                "immediate_action_hindi": "मैंकोजेब (2.5 ग्राम/लीटर) का छिड़काव करें।"
            },
            "Healthy Wheat": {
                "hindi_name": "स्वस्थ गेहूं फसल",
                "pathogen": "None",
                "symptoms": ["Sturdy green stems, clean upright leaves, dense tillers"],
                "symptoms_hindi": ["स्वस्थ हरे तने, मजबूत कल्ले, रोगमुक्त पत्तियां"],
                "favorable_weather": "Sunny cool winter days (15-22°C)",
                "immediate_action": "Apply timely irrigation at critical stages.",
                "immediate_action_hindi": "क्रांतिक अवस्थाओं पर समय से हल्की सिंचाई करें।"
            }
        }
    },
    "Potato": {
        "hindi_name": "आलू (Aloo)",
        "scientific_name": "Solanum tuberosum",
        "primary_season": "Rabi (Major crop in Nalanda, Patna, Vaishali, Samastipur)",
        "water_sensitivity": "HIGHLY SENSITIVE to water stagnation (tuber rot) and winter late blight",
        "stages": [
            {"name": "Sprouting & Emergence", "hindi_name": "जमाव अवस्था (0-20 दिन)", "waterlogging_tolerance_days": 0.5, "drought_tolerance": "MODERATE", "water_stress_impact": "Rotting of mother seed tubers if waterlogged", "flood_risk_multiplier": 1.6},
            {"name": "Tuber Initiation", "hindi_name": "कंद बनने की अवस्था (30-45 दिन)", "waterlogging_tolerance_days": 1, "drought_tolerance": "CRITICAL", "water_stress_impact": "Fewer tubers set, misshapen tubers", "flood_risk_multiplier": 1.5},
            {"name": "Tuber Bulking", "hindi_name": "कंद फुलाव अवस्था (45-75 दिन)", "waterlogging_tolerance_days": 1, "drought_tolerance": "HIGH", "water_stress_impact": "Cracking and reduced size", "flood_risk_multiplier": 1.4},
            {"name": "Maturity", "hindi_name": "खुदाई अवस्था (75-90 दिन)", "waterlogging_tolerance_days": 2, "drought_tolerance": "HIGH", "water_stress_impact": "Soft rot in soil if wet", "flood_risk_multiplier": 1.7}
        ],
        "diseases": {
            "Late Blight": {
                "hindi_name": "पछेती झुलसा (लेट ब्लाइट)",
                "pathogen": "Phytophthora infestans (Oomycete)",
                "symptoms": ["Water-soaked dark lesions at leaf tips and margins spreading rapidly", "White cottony fungal mildew growth on lower leaf surface in morning mist", "Rapid collapse of entire canopy within 48-72 hours"],
                "symptoms_hindi": ["पत्तियों के सिरों पर तेजी से फैलने वाले काले-भूरे भीगे धब्बे", "सुबह की धुंध में पत्ती की निचली सतह पर सफेद फफूंद", "2 से 3 दिनों में पूरा पौधा झुलस कर नष्ट होना"],
                "favorable_weather": "Overcast humid weather (RH >90%), temperature 12-20°C, continuous fog/drizzle",
                "immediate_action": "Prophylactic spray of Mancozeb 75% WP @ 2.5g/L. If disease appears, spray Cymoxanil 8% + Mancozeb 64% WP @ 3g/L or Dimethomorph 50% WP @ 1g/L.",
                "immediate_action_hindi": "सुरक्षात्मक छिड़काव: मैंकोजेब (2.5 ग्राम/लीटर)। लक्षण दिखने पर साइमोक्सानिल + मैंकोजेब (3 ग्राम/लीटर) तुरंत छिड़कें।",
                "organic_remedy": "Bordeaux mixture 1% or Copper Hydroxide spray"
            },
            "Early Blight": {
                "hindi_name": "अगेती झुलसा (अर्ली ब्लाइट)",
                "pathogen": "Alternaria solani (Fungus)",
                "symptoms": ["Concentric target-board rings on older bottom leaves", "Leaves turn yellow and drop prematurely"],
                "symptoms_hindi": ["पुरानी निचली पत्तियों पर चक्राकार (टारगेट बोर्ड) छल्लेदार धब्बे"],
                "favorable_weather": "Alternating wet and dry periods, warm temperatures (24-30°C)",
                "immediate_action": "Spray Chlorothalonil 75% WP @ 2g/L or Mancozeb @ 2.5g/L.",
                "immediate_action_hindi": "क्लोरोथैलोनिल 75% WP (2 ग्राम/लीटर) या मैंकोजेब का छिड़काव करें।"
            },
            "Healthy Potato": {
                "hindi_name": "स्वस्थ आलू फसल",
                "pathogen": "None",
                "symptoms": ["Lush green bushy foliage, strong stems, no water-soaked edges"],
                "symptoms_hindi": ["घना हरा पौधा, मजबूत तने, रोगमुक्त पत्तियां"],
                "favorable_weather": "Bright sunny days, cool crisp nights",
                "immediate_action": "Ensure earthing up (mitti chadhana) is completed and avoid flooding furrows.",
                "immediate_action_hindi": "मेड़ों पर मिट्टी चढ़ाना सुनिश्चित करें और नालियों में पानी न रुकने दें।"
            }
        }
    },
    "Mustard": {
        "hindi_name": "सरसों / राई (Sarson)",
        "scientific_name": "Brassica juncea",
        "primary_season": "Rabi (Major cash crop across all Bihar zones)",
        "water_sensitivity": "MODERATE; sensitive to aphid attacks in humid cloudy weather",
        "stages": [
            {"name": "Vegetative", "hindi_name": "वानस्पतिक अवस्था", "waterlogging_tolerance_days": 1.5, "drought_tolerance": "MODERATE", "water_stress_impact": "Slow rosetting", "flood_risk_multiplier": 1.3},
            {"name": "Flowering", "hindi_name": "फूल आने की अवस्था", "waterlogging_tolerance_days": 1, "drought_tolerance": "CRITICAL", "water_stress_impact": "Flower drop, poor pod set", "flood_risk_multiplier": 1.4},
            {"name": "Pod Formation (Siliqua)", "hindi_name": "फलियां बनने की अवस्था", "waterlogging_tolerance_days": 2, "drought_tolerance": "HIGH", "water_stress_impact": "Immature seed drying", "flood_risk_multiplier": 1.3}
        ],
        "diseases": {
            "White Rust": {
                "hindi_name": "सफेद रतुआ (व्हाइट रस्ट)",
                "pathogen": "Albugo candida (Oomycete)",
                "symptoms": ["Creamy white chalky pustules on lower leaf surface", "Staghead malformation of inflorescence"],
                "symptoms_hindi": ["पत्तियों की निचली सतह पर सफेद चूने जैसे फफोले", "फूलों का विकृत होकर हिरण के सींग जैसा होना"],
                "favorable_weather": "Moist cold weather with high morning humidity",
                "immediate_action": "Spray Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2g/L.",
                "immediate_action_hindi": "मेटालेक्सिल + मैंकोजेब (2 ग्राम/लीटर) का छिड़काव करें।"
            },
            "Mustard Aphid": {
                "hindi_name": "माहू / चेपा कीट",
                "pathogen": "Lipaphis erysimi (Insect Pest)",
                "symptoms": ["Thousands of tiny greenish-black insects sucking sap from flowering buds and tender pods", "Sticky honeydew causing black sooty mold"],
                "symptoms_hindi": ["फूलों और फलियों पर चिपके हजारों छोटे हरे-काले कीट", "चिपचिपा पदार्थ और काली फफूंद"],
                "favorable_weather": "Cloudy humid weather with little sunshine in January-February",
                "immediate_action": "Spray Dimethoate 30% EC @ 1.7ml/L or Imidacloprid 17.8% SL @ 0.3ml/L.",
                "immediate_action_hindi": "डाइमेथोएट (1.7 मिली/लीटर) या इमिडाक्लोप्रिड (0.3 मिली/लीटर) का छिड़काव करें।"
            },
            "Healthy Mustard": {
                "hindi_name": "स्वस्थ सरसों फसल",
                "pathogen": "None",
                "symptoms": ["Vibrant yellow blooms, clean dark green leaves, straight healthy pods"],
                "symptoms_hindi": ["पीले फूल, स्वस्थ फलियां, कीटमुक्त पौधे"],
                "favorable_weather": "Clear sunny skies",
                "immediate_action": "Maintain weed-free plot and light moisture.",
                "immediate_action_hindi": "खेत में खरपतवार न होने दें और हल्की नमी रखें।"
            }
        }
    },
    "Litchi": {
        "hindi_name": "शाही लीची (Shahi Litchi)",
        "scientific_name": "Litchi chinensis",
        "primary_season": "Spring-Summer (Muzaffarpur, Vaishali, East Champaran belt)",
        "water_sensitivity": "Needs micro-irrigation during fruit bulking to prevent peel cracking, sensitive to fruit borer",
        "stages": [
            {"name": "Flowering & Panicle", "hindi_name": "मंजर व फूल अवस्था", "waterlogging_tolerance_days": 2, "drought_tolerance": "MODERATE", "water_stress_impact": "Flower drop", "flood_risk_multiplier": 1.2},
            {"name": "Fruit Development", "hindi_name": "फल विकास अवस्था", "waterlogging_tolerance_days": 2, "drought_tolerance": "CRITICAL", "water_stress_impact": "Fruit cracking and drop", "flood_risk_multiplier": 1.4},
            {"name": "Harvesting", "hindi_name": "तुड़ाई अवस्था", "waterlogging_tolerance_days": 3, "drought_tolerance": "HIGH", "water_stress_impact": "Post-harvest rot", "flood_risk_multiplier": 1.3}
        ],
        "diseases": {
            "Fruit Borer & Anthracnose": {
                "hindi_name": "फल बेधक एवं एन्थ्रेक्नोज़ रोग",
                "pathogen": "Conopomorpha sinensis (Insect) & Colletotrichum (Fungus)",
                "symptoms": ["Bore holes near fruit stalk, brown water-soaked necrotic patches on fruit skin"],
                "symptoms_hindi": ["फल के डंठल के पास छेद, लीची के छिलके पर कत्थई-भूरे धब्बे"],
                "favorable_weather": "Warm humid conditions (28-34°C, RH >80%) with intermittent showers",
                "immediate_action": "Spray Chlorantraniliprole 18.5% SC @ 0.4ml/L or Neem Oil (5ml/L) + Carbendazim @ 1g/L as per NRCL Muzaffarpur guidance.",
                "immediate_action_hindi": "क्लोरेंट्रानिलिप्रोल (0.4 मिली/लीटर) या नीम तेल (5 मिली/लीटर) का छिड़काव करें।",
                "organic_remedy": "Bagging fruit clusters with non-woven polypropylene bags"
            },
            "Healthy Litchi": {
                "hindi_name": "स्वस्थ लीची बागान",
                "pathogen": "None",
                "symptoms": ["Glossy healthy green foliage, clean pinkish-red developing fruit clusters"],
                "symptoms_hindi": ["चमकदार हरी पत्तियां, बेदाग फल"],
                "favorable_weather": "Sunny morning with mild afternoon humidity",
                "immediate_action": "Maintain mulching around tree basin and light drip watering.",
                "immediate_action_hindi": "पेड़ों की थालों में मल्चिंग करें और ड्रिप से हल्की नमी बनाए रखें।"
            }
        }
    },
    "Sugarcane": {
        "hindi_name": "गन्ना (Ganna)",
        "scientific_name": "Saccharum officinarum",
        "primary_season": "Perennial (North-West Bihar / Champaran & Gopalganj belt)",
        "water_sensitivity": "Needs ample water but prolonged water stagnation causes Red Rot",
        "stages": [
            {"name": "Formative Phase", "hindi_name": "शुरुआती बढ़वार अवस्था", "waterlogging_tolerance_days": 4, "drought_tolerance": "MODERATE", "water_stress_impact": "Slow tillering", "flood_risk_multiplier": 1.2},
            {"name": "Grand Growth Phase", "hindi_name": "तीव्र बढ़वार अवस्था", "waterlogging_tolerance_days": 7, "drought_tolerance": "MODERATE", "water_stress_impact": "Short internodes", "flood_risk_multiplier": 1.1},
            {"name": "Ripening & Maturity", "hindi_name": "पकने की अवस्था", "waterlogging_tolerance_days": 5, "drought_tolerance": "HIGH", "water_stress_impact": "Inversion of sucrose if waterlogged", "flood_risk_multiplier": 1.3}
        ],
        "diseases": {
            "Red Rot": {
                "hindi_name": "लाल सड़न रोग (रेड रॉट)",
                "pathogen": "Colletotrichum falcatum (Fungus)",
                "symptoms": ["Third and fourth leaves wither from tip, cane splits reveal red internal pith with white cross bands"],
                "symptoms_hindi": ["ऊपरी पत्तियां सूखना, गन्ने को चीरने पर भीतर लाल गूदा और सफेद आड़े धब्बे"],
                "favorable_weather": "Continuous water stagnation in poorly drained soil",
                "immediate_action": "Drain water immediately. Uproot and burn infected stools. Disinfect soil with Carbendazim.",
                "immediate_action_hindi": "जलभराव तुरंत निकालें। संक्रमित पौधे उखाड़कर नष्ट करें।"
            },
            "Healthy Sugarcane": {
                "hindi_name": "स्वस्थ गन्ना फसल",
                "pathogen": "None",
                "symptoms": ["Thick erect stalks, dark green lanceolate leaves, clean nodes"],
                "symptoms_hindi": ["मजबूत गन्ने के तने, गहरी हरी पत्तियां"],
                "favorable_weather": "Warm tropical sunshine with well-drained fertile loam",
                "immediate_action": "Earth up cane rows and maintain field irrigation drains.",
                "immediate_action_hindi": "गन्ने की पंक्तियों पर मिट्टी चढ़ाएं।"
            }
        }
    }
}
