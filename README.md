# 🌾 KhetRakshak

### Bihar’s Crop Risk Intelligence & Early-Warning Platform

> **Disclaimer:** KhetRakshak is an experimental working prototype and agricultural technology demonstration platform. It combines crop health heuristics, environmental risk assessment, weather-to-crop intelligence, GIS risk visualization, smart alerts, and bilingual advisory. It is **not** a certified medical/scientific crop-disease diagnosis system or an official disaster forecasting authority.

---

## 📖 Overview

Smallholder farmers across Bihar face overlapping, compounded agronomic hazards throughout the crop cycle:

* **Crop diseases & pest outbreaks** that proliferate rapidly in high-humidity riverine microclimates.
* **Excess rainfall & sudden downpours** causing severe water stagnation in poorly drained plains.
* **River inundation & flash floods** from the Kosi, Gandak, Bagmati, and Ganga basins in North Bihar.
* **Waterlogging & root asphyxiation**, particularly devastating during sensitive stages like flowering.
* **Prolonged dry spells, drought, & water stress** in South Bihar's rain-shadow districts.
* **Weather unpredictability & climate variability** that invalidate traditional calendar-based farming.
* **Information fragmentation & delayed guidance**, leaving farmers without actionable, stage-specific advice.

Raw meteorological alerts tell farmers *what the weather might do*, but rarely explain *what it means for their specific crop at its current growth stage*. **KhetRakshak** addresses this gap by unifying plant health observation, localized weather indicators, hydrological stress factors, and agronomic knowledge into a single, farmer-centric interface.

The platform operates on a 5-step operational framework:

$$\text{DETECT} \longrightarrow \text{PREDICT} \longrightarrow \text{UNDERSTAND} \longrightarrow \text{ADVISE} \longrightarrow \text{PROTECT}$$

* **DETECT:** Capture visible leaf symptoms and local field parameters.
* **PREDICT:** Evaluate short-range flood, drought, rain, and disease vulnerabilities.
* **UNDERSTAND:** Translate raw weather numbers into agronomic field consequences.
* **ADVISE:** Provide stage-appropriate, practical actions in Hindi and English.
* **PROTECT:** Alert farmers before critical thresholds trigger irreversible yield loss.

---

## ⚡ Core Features

The following features are implemented and verifiable in the codebase:

### 👨‍🌾 Farmer Profile & Personalization
* **Registration & Secure Login:** Farmer registration with mobile number, district, block, village, land area, primary and secondary crops, crop stage, irrigation source, and preferred language.
* **5 Instant Demo Accounts:** Pre-configured farmer profiles representing diverse agro-climatic zones across Bihar.
* **Dynamic Location Baseline:** Automatically aligns environmental risk parameters with the farmer's registered or selected district.
* **Measurement Units:** Supports standard land metrics (Acres, Bigha, Kattha).

### 📷 Crop Scanner (Computer Vision Heuristics)
* **Image Upload & File Processing:** Accepts crop foliage photos via camera capture, device upload, or preset sample images.
* **Automated Image Quality Inspection:**
  * **Blur Detection:** Discrete 2D Laplacian variance check (`laplacian_var < 55.0` flags blurry or out-of-focus captures).
  * **Illumination Assessment:** RGB luminance checks to reject underexposed/dark (`< 38.0`) or overexposed/glare-washed (`> 235.0`) photos.
  * **Strict Non-Crop Rejection:** Color-space spectral coverage filters verify agricultural foliage (chlorophyll green, chlorotic yellow, necrotic brown lesions). Non-crop photos (vehicles, faces, animals, buildings, indoor scenes) are refused (`status_code: NOT_CROP`).
* **Disease Analysis Workflow:** Identifies symptom patterns (e.g., Maydis Leaf Blight in maize, Bacterial Leaf Blight in paddy, Anthracnose in litchi, Late Blight in potato).
* **Transparent Confidence Scoring:** Displays confidence ratings and flags low-confidence or ambiguous scans rather than guessing.
* **Actionable Farm Guidance:** Provides non-chemical and chemical remediation steps alongside recommendations to verify with the local Krishi Vigyan Kendra (KVK).
* *Note: The current computer vision module uses rule-based image processing heuristics and feature-extraction models. It is model-ready for transfer learning integrations and should not be treated as a medically or scientifically validated diagnosis system.*

### 🌧️ Weather-to-Crop Intelligence
* **Contextual Agronomic Interpretation:** Translates forecast rainfall, temperature, relative humidity, and wind speed into specific crop stage impacts.
* **Irrigation Directives:** Generates clear directives (`STOP ALL IRRIGATION`, `CRITICAL IRRIGATION REQUIRED`, or `NORMAL MOISTURE`) based on 48-hour rainfall forecasts and soil moisture saturation.
* **Safe Spray Windows:** Analyzes rain probability and wind velocity to advise whether chemical or foliar sprays will adhere or wash away.
* **Stage-Specific Impact Explanations:** Explains biological consequences (e.g., how 24 hours of standing water during maize flowering halts silking and causes cob abortion).

### 🌊 Flood & Waterlogging Risk
* **Multi-Factor Hydrology Assessment:** Evaluates 48-hour forecast rainfall, existing soil moisture saturation percentage, river level gauge status (Normal, Near Warning, Above Danger Level), and historical basin vulnerability.
* **Crop Vulnerability Multipliers:** Applies growth-stage sensitivity factors (e.g., maize flowering has a higher flood sensitivity multiplier than mature paddy).

### ☀️ Drought & Water Stress
* **Soil & Rainfall Deficit Modeling:** Evaluates root-zone moisture deficits, 48-hour rainfall shortages, elevated evapotranspiration temperatures, and South Bihar drought vulnerability baselines.
* **Agronomic Mitigation:** Suggests protective strategies such as mulching, light evening irrigation, and potassium foliar sprays to minimize transpiration.

### 🗺️ Bihar GIS Risk Map
* **Full 38-District Coverage:** Interactive geographic visualization built with **Leaflet.js** and **OpenStreetMap**.
* **District Multi-Risk Indicators:** Color-coded district markers displaying flood vulnerability (red), drought stress (amber), moderate risk (orange), or normal status (green).
* **River Basin Context:** Annotates river basins including Kosi, Ganga, Burhi Gandak, Bagmati, Sone, and Falgu.
* **Interactive District Modal:** Clicking any district displays 24-hour rainfall, rainfall anomalies, flood/drought risk scores, primary crops, and active advisories.
* **Active Farm Pin:** Plots a distinct pulsating marker showing the logged-in farmer's geographical coordinates.

### 🔔 Smart Alerts
* **Severity-Graded System:** Categorizes alerts into `CRITICAL`, `WARNING`, and `INFO`.
* **Thematic Coverage:** Alerts spanning Flood/Waterlogging, Drought Stress, Disease Outbreaks, High Wind, and Spray Windows.
* **Bilingual Guidance:** Each alert includes plain-language root causes and recommended mitigation steps in both Hindi and English.

### 💬 Farmer Advisor (RAG-Grounded Chat)
* **Agronomic Knowledge Base:** Grounded in recommendations and advisories inspired by Bihar institutions including:
  * Bihar Agricultural University (BAU), Sabour
  * ICAR Research Complex for Eastern Region (ICAR-RCER), Patna
  * Krishi Vigyan Kendra (KVK) Network
  * Rajendra Prasad Central Agricultural University (RPCAU), Pusa
* **Context-Aware Responses:** Synthesizes the active farmer profile, crop growth stage, and current risk scores into tailored advice.
* **Citation Visibility:** Cites the verified source behind recommendations.

### 🔊 Voice Support (Speech-to-Text & TTS)
* **Web Speech Recognition:** Voice query input supporting Hindi (`hi-IN`) and English (`en-IN`).
* **Pre-Recorded Voice Prompts:** One-tap audio scenario chips for hands-free queries.
* **Speech Synthesis (TTS):** Spoken audio playback of advisor responses in Hindi or English.

### 📅 Farm Timeline
* **Historical Audit Trail:** Chronological log of crop scans, detected issues, confidence ratings, risk scores, and generated alerts stored in SQLite.

### 🌾 My Farm
* **Profile Management:** View and edit land size, soil type, irrigation source, crop stage, and location parameters.

### 🌐 Bilingual Interface (Hindi / English)
* **Instant Language Toggle:** Comprehensive UI switching between Hindi (`hi`) and English (`en`) with persistent client-side storage.

### 🌙 Dark / Light Mode
* **Persistent Theme Switching:** Theme toggle with smooth transition styling and persistent local preference.

### ⋮ Simplified Navigation
* **4-Tab Primary Bar:** Clean navigation across `Dashboard`, `Crop Scan`, `Risk`, and `Alerts`.
* **3-Dot "More" Dropdown Menu:** Quick access to extended modules including Flood Risk, Drought & Moisture, Weather-to-Crop, Ask Advisor, Voice AI, Bihar Risk Map, Farm Timeline, Profile, and Admin Metrics.

---

## 🔄 How KhetRakshak Works

```
                     ┌────────────────────────┐
                     │   Smallholder Farmer   │
                     └───────────┬────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │   Login / Demo Account │
                     └───────────┬────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │     Farmer Profile     │
                     │ (District, Crop, Stage)│
                     └───────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐      ┌────────▼────────┐      ┌────────▼────────┐
│  Crop Scanner  │      │ Weather-to-Crop │      │ Hydrological &  │
│(Image Quality, │      │ (Rainfall, Temp,│      │ GIS Risk Engine │
│Lesion Analysis)│      │  Spray Windows) │      │ (38 Districts)  │
└───────┬────────┘      └────────┬────────┘      └────────┬────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │  Composite Risk Engine │
                     │  (0-100 Score & Level) │
                     └───────────┬────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        │                                                 │
┌───────▼────────┐                               ┌────────▼────────┐
│  Smart Alerts  │                               │ Personalized AI │
│  (Bilingual,   │                               │    Advisory     │
│Severity-Based) │                               │  (Text & Voice) │
└───────┬────────┘                               └────────┬────────┘
        │                                                 │
        └────────────────────────┬────────────────────────┘
                                 │
                     ┌───────────▼────────────┐
                     │ Timely Farmer Decision │
                     │ (Drain, Spray, Irrigate)│
                     └────────────────────────┘
```

---

## 🛠️ Technology Stack

KhetRakshak is built using standard, lightweight open-source technologies:

### Backend
* **Python 3.10+ / 3.13:** Core backend runtime.
* **FastAPI (0.110+):** High-performance asynchronous REST API framework.
* **Pydantic (v2):** Data validation, schema definitions, and request/response models.
* **Uvicorn (0.28+):** ASGI production web server.
* **Python-Multipart:** Multipart form-data handling for image uploads.

### Computer Vision & Image Processing
* **Pillow (PIL 10.0+):** Image manipulation, luminance extraction, and color processing.
* **NumPy (1.24+):** Array operations, Laplacian variance convolution for blur detection, and multi-spectral foliage masking.

### Frontend
* **HTML5:** Semantic document structure.
* **Vanilla CSS (`/static/css/styles.css`):** Custom glassmorphism, responsive navigation, and dark mode tokens.
* **Tailwind CSS (CDN):** Utility styling and responsive layouts.
* **Vanilla JavaScript (ES6+):** Modular frontend logic:
  * `app.js`: Main state management, bilingual translation dictionary, and API bindings.
  * `scanner.js`: Camera handling, image preview, quality check rendering, and diagnosis UI.
  * `bihar_map.js`: Leaflet map initialization, district markers, and popup bindings.
  * `voice.js`: Web Speech API recognition, synthesis, and audio scenario handling.

### Mapping & GIS
* **Leaflet.js (1.9.4):** Interactive mobile-friendly map library.
* **OpenStreetMap (OSM):** Map tile provider.

### Data & Persistence
* **SQLite3 (`khetrakshak.db`):** Relational storage for farmer accounts, farm profiles, scan history, and alerts.
* **Pre-Seeded Agronomic Datasets:**
  * `bihar_districts.py`: Geographic and agro-climatic profiles for all 38 Bihar districts.
  * `crop_agronomy.py`: Agronomic rules, growth stages, disease catalogues, and water thresholds for 7 major crops (Maize, Paddy, Wheat, Potato, Mustard, Litchi, Sugarcane).
  * `sample_scenarios.py`: 5 realistic demo scenarios with pre-configured telemetry.

---

## 📁 Project Structure

```text
KhetRakshak/
├── app/
│   ├── ai/
│   │   ├── crop_vision.py                  # Image quality validation, blur/dark filters, non-crop rejection, lesion analysis
│   │   ├── rag_advisor.py                  # Knowledge retrieval & bilingual advisory generation
│   │   ├── risk_engine.py                  # Multi-hazard risk calculation & explainability engine
│   │   └── weather_crop_intelligence.py    # Forecast-to-crop impact & irrigation/spraying guidance
│   ├── data/
│   │   ├── bihar_districts.py              # Geospatial & climate metadata for 38 Bihar districts
│   │   ├── crop_agronomy.py                # Agronomic database (7 crops, stages, diseases, thresholds)
│   │   └── sample_scenarios.py             # 5 pre-configured Bihar evaluation scenarios
│   ├── models.py                           # Pydantic data schemas & request/response contracts
│   └── storage.py                          # SQLite database schema, migrations, and CRUD operations
├── scripts/
│   └── generate_sample_images.py           # Utility to generate synthetic leaf test images for development
├── static/
│   ├── css/
│   │   └── styles.css                      # Custom CSS styles, glassmorphism, and theme variables
│   ├── js/
│   │   ├── app.js                          # Core application logic, bilingual translations, UI rendering
│   │   ├── bihar_map.js                    # Leaflet.js Bihar district GIS map integration
│   │   ├── scanner.js                      # Image upload, validation feedback, and scan workflow
│   │   └── voice.js                        # Speech recognition & speech synthesis integration
│   └── sample_images/                      # Pre-generated sample images for scanner testing
│       ├── blurry_leaf_sample.jpg
│       ├── dark_leaf_sample.jpg
│       ├── healthy_maize.jpg
│       ├── maize_maydis_blight.jpg
│       ├── non_crop_sample.jpg
│       └── paddy_bacterial_blight.jpg
├── templates/
│   └── index.html                          # Single-page application template with all views & modals
├── khetrakshak.db                          # SQLite database file
├── main.py                                 # FastAPI application entry point and API route definitions
├── requirements.txt                        # Python dependencies
├── .gitignore                              # Git exclusion rules
└── README.md                               # Project documentation
```

---

## 🚀 Installation & Local Setup

### Prerequisites
* **Python:** Version 3.10 or higher (tested up to Python 3.13)
* **pip:** Python package installer
* **Git:** Version control system

### 1. Clone the Repository
```bash
git clone https://github.com/shubhj777/KhetRakshak-.git
cd KhetRakshak-
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 4. Run the Application
```bash
python3 -m uvicorn main:app --reload
```

The application will start on:
```
http://127.0.0.1:8000
```
Open this URL in any modern web browser (Google Chrome or Microsoft Edge recommended for full Web Speech API support).

---

## 👥 Demo Accounts & Evaluation Scenarios

KhetRakshak provides 5 pre-configured demo scenarios representing distinct agro-climatic zones and challenges across Bihar. These can be accessed directly from the **"Demo Accounts"** modal in the navigation bar:

| # | District | Farmer Name | Primary Crop | Growth Stage | Primary Threat & Scenario | Baseline Risk Score |
|---|---|---|---|---|---|---|
| **1** | **Purnia** (Kasba Block) | Ramesh Kumar Yadav | Maize | Flowering & Tasseling | Heavy rainfall forecast (88.5mm) + Kosi river near warning level + saturated soil. High risk of waterlogging and Maydis Leaf Blight. | **84 / 100** (High) |
| **2** | **Gaya** (Bodh Gaya Block) | Suresh Manjhi | Wheat | Vegetative (Jointing) | Severe rainfall deficit (-42%) in South Bihar + dry Falgu basin + low soil moisture (28%). High drought stress. | **98 / 100** (Severe) |
| **3** | **Bhagalpur** (Sabour Block) | Arun Kumar Singh | Katarni Paddy | Tillering | Ganga basin water surge + saturated silt loam. Waterlogging vigilance and Bacterial Leaf Blight risk. | **57 / 100** (Moderate) |
| **4** | **Muzaffarpur** (Mushahari Block) | Mukesh Chandra | Shahi Litchi | Fruit Development | High humidity (82%) along Burhi Gandak basin. Threat of Litchi fruit borer and anthracnose spot damage. | **41 / 100** (Moderate) |
| **5** | **Rohtas** (Nokha Block) | Dharmendra Rai | Paddy / Wheat | Tillering & Growth | Granary of Bihar + Sone canal command area. Adequate controlled irrigation and stable moisture baseline. | **27 / 100** (Safe / Normal) |

> **How to Access:** Click the **"Demo Accounts"** button in the header (or select it from the 3-dot "More" menu) and click on any scenario card. The entire application—profile, active district, environmental sensors, scan results, alerts, and GIS map pin—will instantly reload with that scenario's parameters.

---

## 📡 API Overview

All API endpoints are implemented in [`main.py`](file:///Users/shubhj_777/Desktop/KhetRakshak/main.py):

| Group | Method | Endpoint | Purpose |
|---|---|---|---|
| **Authentication** | `POST` | `/api/auth/register` | Register a new farmer account with district, crop, and farm details. |
| | `POST` | `/api/auth/login` | Authenticate an existing farmer via mobile number and password. |
| | `GET` | `/api/auth/demo-accounts` | Retrieve the list of 5 pre-configured Bihar demo accounts. |
| | `POST` | `/api/auth/demo-login/{demo_id}` | Switch session to a specific demo account and load its preset telemetry. |
| **Profile** | `GET` | `/api/profile` | Retrieve the active farm profile and crop parameters. |
| | `POST` | `/api/profile` | Update farm details (district, crop, land area, irrigation, stage). |
| **Crop & Vision** | `GET` | `/api/crop-catalog` | Get the agronomic catalog of supported Bihar crops, stages, and diseases. |
| | `POST` | `/api/scan-crop` | Upload an image file for quality checks and disease analysis (multipart/form-data). |
| | `POST` | `/api/scan-crop-json` | Submit base64-encoded image or sample key for analysis (JSON). |
| **Risk & Intelligence** | `GET` | `/api/risk-evaluation` | Compute multi-hazard risk score, sub-indices, and explainability reasons. |
| | `GET` | `/api/weather-to-crop` | Generate crop-stage-specific weather interpretation, irrigation & spray advice. |
| | `GET` | `/api/districts-gis` | Retrieve geographic coordinates and risk metadata for all 38 Bihar districts. |
| | `GET` | `/api/scenarios` | List available demo evaluation scenarios. |
| | `POST` | `/api/load-scenario/{scenario_id}` | Load a specific preset scenario into the active session. |
| **Advisory & Voice** | `POST` | `/api/ask-advisor` | Submit a text question to the RAG advisory engine with institutional citations. |
| | `POST` | `/api/voice-query` | Process a speech transcript and return bilingual text and audio response metadata. |
| **Operations** | `GET` | `/api/alerts` | Fetch active smart alerts filtered by severity and category. |
| | `GET` | `/api/timeline` | Retrieve chronological scan and advisory history from SQLite. |
| | `GET` | `/api/admin/metrics` | Retrieve administrative surveillance metrics and district alert counts. |

---

## ⚠️ Data & Prototype Limitations

KhetRakshak is designed to demonstrate an end-to-end user experience and system architecture. Users and evaluators should note the following technical boundaries:

* **Prototype Status:** This system is an engineering prototype developed for demonstration and conceptual evaluation. It is not currently certified for production field deployment.
* **Sample & Simulated Environmental Telemetry:** In the absence of live API feeds from government departments or IoT sensor hardware, environmental metrics (rainfall forecasts, river levels, soil moisture) use realistic simulated values and preset scenario data.
* **Non-Replacement for Certified Advice:** Recommendations generated by the advisory and scanner modules are informational. Farmers should consult certified Krishi Vigyan Kendra (KVK) scientists or agricultural officers before applying chemical fungicides or pesticides.
* **Deterministic Risk Scoring:** The multi-risk engine uses an agronomic heuristic scoring formula based on published extension literature. Scores are intended for risk prioritization, not probabilistic guarantees.
* **Evaluation Scenarios:** The pre-configured scenarios demonstrate edge cases (severe flood risk vs. extreme drought). Actual field conditions will vary by micro-location.

---

## 🗺️ Bihar-Specific Agro-Climatic Design

Bihar exhibits a stark agro-climatic duality divided by the Ganges River. KhetRakshak is tailored specifically to address these regional dynamics:

### North Bihar (Flood-Prone Alluvial Plains)
* **River Basins:** Kosi, Burhi Gandak, Gandak, Bagmati, Kamla-Balan, Mahananda.
* **Characteristics:** Silt-rich alluvial soils (Khadar), shallow water tables, and high annual monsoon rainfall.
* **Primary Hazards:** Perennial river inundation, flash flooding from Nepal catchment runoff, waterlogging in saucer-shaped depressions (*chaurs*), and fungal leaf blights during humid spells.
* **KhetRakshak Adaptation:** The risk engine assigns a 60% combined weight to flood and excess rainfall factors, highlighting water evacuation strategies and fungal prophylaxis.

### South Bihar (Drought-Vulnerable Plains & Plateaus)
* **River Basins:** Sone, Punpun, Falgu, Kiul, Badua.
* **Characteristics:** Older alluvium (Bangar) and red gravelly soils, deeper water tables, and lower monsoon precipitation.
* **Primary Hazards:** Monsoon failure, erratic rainfall distribution, terminal drought during reproductive crop stages, and declining groundwater levels.
* **KhetRakshak Adaptation:** The risk engine shifts primary weighting (65%) to rainfall deficits, soil moisture exhaustion, and evapotranspiration stress, recommending moisture-conservation practices (Alternate Wetting and Drying, mulching, foliar potassium).

> *Note: Risk indicators are heuristic representations of published agro-climatic tendencies and do not constitute official disaster declarations.*

---

## 🛡️ Responsible AI & Image Analysis Safeguards

Agricultural computer vision systems deployed directly to farmers must adhere to strict safety safeguards to prevent incorrect chemical recommendations:

1. **Non-Crop Image Rejection:**
   * Images that do not exhibit characteristic spectral foliage distributions (chlorophyll green, chlorotic yellow, or necrotic brown lesion pigmentation) are rejected with a clear message (`NOT_CROP`).
   * Prevents accidental diagnosis of photographs containing vehicles, household objects, documents, or faces.
2. **Quality Verification:**
   * **Blur Filtering:** Uses discrete 2D Laplacian variance convolution to detect blurred or shaking camera captures.
   * **Illumination Filtering:** Calculates RGB luminance to reject underexposed (dark night/shadow) or overexposed (sun-glare washed) leaf photos.
3. **Transparent Uncertainty Disclosure:**
   * Low-confidence classifications (`< 65%`) are explicitly labeled with warning indicators rather than presenting a speculative diagnosis.
   * The UI highlights that automated computer vision should be corroborated by local agricultural extension officers before investing in chemical treatments.
4. **Future Model Integration:**
   * The codebase provides a modular abstraction (`CropVisionModel` in [`crop_vision.py`](file:///Users/shubhj_777/Desktop/KhetRakshak/app/ai/crop_vision.py)) structured so that PyTorch, ONNX, or TensorFlow Lite models trained on comprehensive agricultural datasets (e.g., PlantVillage, ICAR pest repositories) can be plugged in directly.

---

## 🔮 Future Scope

The following enhancements represent planned directions for future production iterations:

* **Live Environmental Integrations:**
  * Integration with India Meteorological Department (IMD) open weather APIs.
  * Real-time river telemetry from the Central Water Commission (CWC) and Bihar Water Resources Department (FMIS).
* **Remote Sensing & Satellite Imagery:**
  * Sentinel-2 and Landsat multispectral index tracking (NDVI for vegetation vigor, NDWI for surface water ponding).
* **Deep Learning Computer Vision:**
  * Fine-tuned convolutional vision backbones (e.g., EfficientNet, MobileNetV4) trained on regional crop disease datasets.
* **IoT Field Sensor Telemetry:**
  * In-situ soil moisture, electrical conductivity (EC), and canopy temperature sensors.
* **Regional Language Expansion:**
  * Addition of local Bihar languages and dialects (Bhojpuri, Maithili, Magahi, Angika) in voice and text interfaces.
* **Low-Connectivity Distribution:**
  * SMS alerts and automated Interactive Voice Response (IVR) telephone updates for basic feature phones without internet connectivity.
* **Granular GIS Hydrology:**
  * High-resolution elevation digital elevation models (DEM) for village- and plot-level drainage flow mapping.
* **Verified Human-in-the-Loop Support:**
  * Escalation pathway connecting flagged scans directly to certified KVK agronomists for review.

---

## 📸 Screenshots

Screenshots of the KhetRakshak interface, crop scanner, Bihar GIS risk map, and mobile responsive views can be placed here:

* *Dashboard & Composite Risk Gauge*
* *Crop Scanner & Image Quality Validation*
* *Leaflet 38-District Bihar GIS Risk Map*
* *Weather-to-Crop Agronomic Intelligence*
* *Bilingual AI Farmer Advisor & Voice Interface*

---

## 💻 Local Development Notes

### Running with Live Reload
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Generating Test Sample Images
To generate synthetic test images for blur, dark lighting, non-crop objects, and disease patterns:
```bash
python3 scripts/generate_sample_images.py
```
This script populates [`static/sample_images/`](file:///Users/shubhj_777/Desktop/KhetRakshak/static/sample_images) with test fixtures used by the scanner module.

### Inspecting the Database
The SQLite database can be inspected with standard tools:
```bash
sqlite3 khetrakshak.db ".tables"
sqlite3 khetrakshak.db "SELECT id, farmer_name, district, primary_crop FROM farmers;"
```

---

## 🧪 Testing & Validation

The codebase has been verified across the following functional areas:

* **Backend Startup & Health:** FastAPI starts cleanly with zero module import or circular dependency errors.
* **API Endpoints:** All documented REST routes respond with valid HTTP status codes and Pydantic-validated JSON payloads.
* **Crop Scanner Pipeline:**
  * Valid crop leaf images are processed through quality checks and produce structured disease outputs.
  * Blurry, dark, and non-crop test images trigger appropriate rejection status codes (`BLURRY`, `TOO_DARK`, `NOT_CROP`).
* **Bilingual Localization:** Client-side translation strings update UI text elements across all tabs in both Hindi and English.
* **Theme Switching:** Dark mode and light mode toggles update root document styling without layout distortion.
* **GIS Map Initialization:** Leaflet.js renders all 38 Bihar districts with responsive tooltips and color-coded risk markers.
* **Demo Scenarios:** All 5 pre-configured scenarios load their complete profiles, risk scores, and telemetry upon selection.
* **Database Operations:** Farmer registration, profile updates, and scan timeline entries persist across server restarts in `khetrakshak.db`.

---

## 💡 Project Philosophy

> **"Farmers should receive understandable, timely, and actionable information rather than disconnected technical data."**

Agricultural early-warning systems often fail smallholders by providing raw, generic meteorological data (*"45mm rain expected"*) or isolated diagnoses (*"your plant has blight"*) without contextualizing what that means for the specific crop, at its current growth stage, in that specific river basin.

KhetRakshak connects these dots:

$$\textbf{Detect} \longrightarrow \textbf{Predict} \longrightarrow \textbf{Understand} \longrightarrow \textbf{Advise} \longrightarrow \textbf{Protect}$$

By centering the farmer's operational decisions—*Should I spray today? Should I run the pump? Should I clear drainage furrows?*—KhetRakshak transforms multi-source agricultural data into practical risk protection.

---

## 📄 License

License: Not specified yet.

---

## 👥 Contributors

Contributors: KhetRakshak development team
