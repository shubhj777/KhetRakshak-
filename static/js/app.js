/**
 * KhetRakshak AI - Core Client Application State & Router
 * Bihar's AI-Powered Crop Risk Intelligence & Early-Warning Platform
 */

const AppState = {
    language: 'hi', // default to Hindi as per Bihar Farmer Persona, toggleable to English
    currentTab: 'dashboard',
    profile: null,
    riskData: null,
    weatherImpact: null,
    alerts: [],
    timeline: [],
    adminMetrics: null,
    districtsGis: [],
    selectedDistrict: 'Purnia'
};

// Bilingual Localized Strings
const I18N = {
    hi: {
        appName: 'खेतरक्षक AI',
        tagline: 'बिहार का AI-संचालित फसल जोखिम और पूर्व-चेतावनी मंच',
        philosophy: 'मौसम बताता है क्या आ रहा है। फसल स्कैनर बताता है क्या हो रहा है। खेतरक्षक बताता है कि आपके खेत पर इसका क्या असर होगा।',
        btnDemo: '⚡ IDEATEX डेमो परिदृश्य (पूर्णिया मक्का)',
        welcomeFarmer: 'नमस्ते, किसान भाई 👋',
        highCropRisk: 'उच्च फसल जोखिम (HIGH CROP RISK)',
        moderateRisk: 'मध्यम फसल जोखिम',
        lowRisk: 'सुरक्षित / निम्न जोखिम',
        scoreLabel: 'खेतरक्षक स्कोर',
        breakdownTitle: 'पर्यावरणीय एवं जैविक जोखिम विश्लेषण',
        floodRisk: 'बाढ़ व जलजमाव जोखिम',
        diseaseRisk: 'पत्ती रोग (ब्लाइट) जोखिम',
        droughtRisk: 'सूखा व नमी की कमी',
        excessRain: 'अत्यधिक बारिश का दबाव',
        pestRisk: 'कीट प्रकोप का खतरा',
        whyHigh: 'यह उच्च जोखिम क्यों है?',
        whatToDo: 'खेत में तुरंत क्या करें?',
        weatherMeaningTitle: 'आपके खेत पर इस मौसम का वास्तविक असर',
        scanNow: 'फसल स्वास्थ्य स्कैन करें',
        exploreMap: 'बिहार जोखिम मानचित्र देखें',
        tabDashboard: 'डैशबोर्ड',
        tabScanner: 'फसल स्कैनर',
        tabFlood: 'बाढ़ जोखिम',
        tabDrought: 'सूखा व नमी',
        tabWeather: 'मौसम-फसल AI',
        tabAdvisor: 'सलाहकार',
        tabVoice: 'आवाज AI',
        tabMap: 'बिहार मानचित्र',
        tabAlerts: 'अलर्ट',
        tabTimeline: 'टाइमलाइन',
        tabProfile: 'मेरा खेत',
        tabAdmin: 'प्रशासन डैशबोर्ड',
        tabAbout: 'परिचय / Impact',
        disclaimerNotice: 'सूचना: खेतरक्षक AI एक निर्णय-सहायक प्रणाली है। आपदा प्रबंधन विभाग (बिहार सरकार) के आधिकारिक निर्देश सर्वोपरि हैं।'
    },
    en: {
        appName: 'KhetRakshak AI',
        tagline: "Bihar's AI-Powered Crop Risk Intelligence Platform",
        philosophy: 'Weather tells you what is coming. Crop detection tells you what is happening. KhetRakshak tells you what it means for your farm.',
        btnDemo: '⚡ Load IDEATEX Demo (Purnia Maize)',
        welcomeFarmer: 'Namaste, Farmer 👋',
        highCropRisk: 'HIGH CROP RISK',
        moderateRisk: 'MODERATE CROP RISK',
        lowRisk: 'LOW / SAFE CROP RISK',
        scoreLabel: 'KhetRakshak Score',
        breakdownTitle: 'Environmental & Biological Risk Breakdown',
        floodRisk: 'Flood & Waterlogging Risk',
        diseaseRisk: 'Crop Disease Risk',
        droughtRisk: 'Drought & Moisture Deficit',
        excessRain: 'Excess Rainfall Surge',
        pestRisk: 'Pest Outbreak Risk',
        whyHigh: 'Why is this considered High Risk?',
        whatToDo: 'Actionable Field Directives',
        weatherMeaningTitle: 'What This Weather Means for Your Farm',
        scanNow: 'Analyze My Crop',
        exploreMap: 'Explore Bihar Risk Map',
        tabDashboard: 'Dashboard',
        tabScanner: 'Crop Scanner',
        tabFlood: 'Flood Risk',
        tabDrought: 'Drought & Water Stress',
        tabWeather: 'Weather-to-Crop',
        tabAdvisor: 'Ask Advisor',
        tabVoice: 'Voice AI',
        tabMap: 'Bihar Risk Map',
        tabAlerts: 'Smart Alerts',
        tabTimeline: 'Farm Timeline',
        tabProfile: 'My Farm',
        tabAdmin: 'Admin Surveillance',
        tabAbout: 'About / Impact',
        disclaimerNotice: 'Notice: KhetRakshak AI is an agronomic decision-support platform. Official Bihar Disaster Management Department (DMD) alerts take legal precedence.'
    }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
    setupTabNavigation();
    setupLanguageToggle();
    setupScenarioButtons();
    
    // Load initial data
    await loadInitialData();
});

async function loadInitialData() {
    try {
        await Promise.all([
            fetchProfile(),
            fetchRiskEvaluation(),
            fetchWeatherToCrop(),
            fetchAlerts(),
            fetchTimeline(),
            fetchDistrictsGis(),
            fetchAdminMetrics()
        ]);
        renderDashboard();
    } catch (e) {
        console.error("Error loading initial data:", e);
    }
}

// Navigation Tabs
function setupTabNavigation() {
    const tabs = document.querySelectorAll('.nav-tab-btn, .mobile-tab-btn');
    tabs.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

function switchTab(tabId) {
    AppState.currentTab = tabId;

    // Update active nav styling
    document.querySelectorAll('.nav-tab-btn, .mobile-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-tab') === tabId) {
            btn.classList.add('active', 'text-emerald-700', 'font-bold');
            btn.classList.remove('text-slate-600');
        } else {
            btn.classList.remove('active', 'text-emerald-700', 'font-bold');
            btn.classList.add('text-slate-600');
        }
    });

    // Toggle section visibility
    document.querySelectorAll('.app-section').forEach(sec => {
        if (sec.id === `section-${tabId}`) {
            sec.classList.remove('hidden');
            sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            sec.classList.add('hidden');
        }
    });

    // Special handlers per tab
    if (tabId === 'map' && window.BiharMap) {
        setTimeout(() => window.BiharMap.invalidateSize(), 200);
    }
}

// Language Switcher
function setupLanguageToggle() {
    const langBtn = document.getElementById('btn-lang-toggle');
    if (langBtn) {
        langBtn.addEventListener('click', () => {
            AppState.language = AppState.language === 'hi' ? 'en' : 'hi';
            updateLanguageUI();
        });
    }
}

function updateLanguageUI() {
    const lang = AppState.language;
    const t = I18N[lang];

    // Toggle button label
    const langBtnText = document.getElementById('lang-btn-text');
    if (langBtnText) {
        langBtnText.textContent = lang === 'hi' ? 'English' : 'हिंदी';
    }

    // Apply translations across UI
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            el.textContent = t[key];
        }
    });

    // Re-render dashboard dynamic text
    renderDashboard();
}

// API Calls
async function fetchProfile() {
    const res = await fetch('/api/profile');
    AppState.profile = await res.json();
    renderProfileUI();
}

async function fetchRiskEvaluation() {
    const res = await fetch('/api/risk-evaluation');
    const data = await res.json();
    AppState.riskData = data.risk;
    AppState.profile = data.profile;
    AppState.currentEnv = data.environmental;
    AppState.latestScan = data.scan_result;
}

async function fetchWeatherToCrop() {
    const res = await fetch('/api/weather-to-crop');
    AppState.weatherImpact = await res.json();
}

async function fetchAlerts() {
    const res = await fetch('/api/alerts');
    AppState.alerts = await res.json();
    renderAlertsUI();
}

async function fetchTimeline() {
    const res = await fetch('/api/timeline');
    AppState.timeline = await res.json();
    renderTimelineUI();
}

async function fetchDistrictsGis() {
    const res = await fetch('/api/districts-gis');
    AppState.districtsGis = await res.json();
    if (window.initBiharGISMap) {
        window.initBiharGISMap(AppState.districtsGis);
    }
}

async function fetchAdminMetrics() {
    const res = await fetch('/api/admin/metrics');
    AppState.adminMetrics = await res.json();
    renderAdminUI();
}

// Scenario loader setup
function setupScenarioButtons() {
    const btnIdeatex = document.getElementById('btn-load-ideatex-demo');
    if (btnIdeatex) {
        btnIdeatex.addEventListener('click', async () => {
            await loadScenario('ideatex_purnia_maize');
        });
    }

    const scenarioSelector = document.getElementById('demo-scenario-select');
    if (scenarioSelector) {
        scenarioSelector.addEventListener('change', async (e) => {
            if (e.target.value) {
                await loadScenario(e.target.value);
            }
        });
    }
}

async function loadScenario(scenarioId) {
    try {
        showToast("Loading Scenario...", "info");
        const res = await fetch(`/api/load-scenario/${scenarioId}`, { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
            AppState.profile = data.profile;
            AppState.riskData = data.risk_result;
            AppState.currentEnv = data.environmental;
            AppState.latestScan = data.scan_result;
            
            await fetchWeatherToCrop();
            await fetchTimeline();
            
            renderDashboard();
            renderProfileUI();
            
            showToast(`Scenario Loaded: ${data.scenario.title}`, "success");
            
            // Switch to dashboard view
            switchTab('dashboard');
        }
    } catch (err) {
        console.error("Failed to load scenario:", err);
        showToast("Failed to load scenario", "error");
    }
}

// Render Dashboard Data
function renderDashboard() {
    if (!AppState.riskData || !AppState.profile) return;

    const r = AppState.riskData;
    const p = AppState.profile;
    const lang = AppState.language;

    // Farmer Profile Header
    const farmerNameEl = document.getElementById('dash-farmer-name');
    if (farmerNameEl) {
        farmerNameEl.textContent = `${p.farmer_name} (${p.district}, ${p.village_block || 'Bihar'})`;
    }

    const farmMetaEl = document.getElementById('dash-farm-meta');
    if (farmMetaEl) {
        farmMetaEl.textContent = `${p.crop} • ${p.crop_stage} • ${p.farm_size_acres} Acres • ${p.soil_type}`;
    }

    // Overall Score Gauge
    const scoreValEl = document.getElementById('score-value');
    if (scoreValEl) {
        scoreValEl.textContent = r.overall_khetrakshak_score;
    }

    const scoreCircleEl = document.getElementById('score-circle');
    if (scoreCircleEl) {
        const score = r.overall_khetrakshak_score;
        let color = '#16a34a';
        if (score >= 70) color = '#dc2626';
        else if (score >= 45) color = '#d97706';
        scoreCircleEl.style.background = `conic-gradient(${color} 0% ${score}%, #e2e8f0 ${score}% 100%)`;
    }

    const riskLevelBadge = document.getElementById('risk-level-badge');
    if (riskLevelBadge) {
        riskLevelBadge.textContent = lang === 'hi' ? r.risk_level_hindi : `${r.risk_level} CROP RISK`;
        riskLevelBadge.className = `px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
            r.overall_khetrakshak_score >= 70 ? 'bg-red-100 text-red-700 border border-red-200' :
            r.overall_khetrakshak_score >= 45 ? 'bg-amber-100 text-amber-800 border border-amber-200' :
            'bg-green-100 text-green-700 border border-green-200'
        }`;
    }

    // Risk Breakdown Bars
    const bd = r.breakdown;
    setBarValue('bar-flood', 'val-flood', bd.flood_risk);
    setBarValue('bar-disease', 'val-disease', bd.disease_risk);
    setBarValue('bar-drought', 'val-drought', bd.drought_risk);
    setBarValue('bar-rain', 'val-rain', bd.excess_rain_risk);
    setBarValue('bar-pest', 'val-pest', bd.pest_risk);

    // Why is this high risk? (Explainability)
    const whyList = document.getElementById('dash-why-reasons');
    if (whyList) {
        const reasons = lang === 'hi' ? r.why_reasons_hindi : r.why_reasons;
        whyList.innerHTML = reasons.map(rsn => `
            <li class="flex items-start gap-2 text-sm text-slate-700">
                <span class="text-amber-500 font-bold">⚠️</span>
                <span>${rsn}</span>
            </li>
        `).join('');
    }

    // What should I do? (Actionable)
    const actionList = document.getElementById('dash-actions');
    if (actionList) {
        const actions = lang === 'hi' ? r.actionable_recommendations_hindi : r.actionable_recommendations;
        actionList.innerHTML = actions.map(act => `
            <li class="flex items-start gap-2 text-sm text-slate-800 font-medium bg-emerald-50 p-2.5 rounded-lg border border-emerald-100">
                <span class="text-emerald-600 font-bold">✓</span>
                <span>${act}</span>
            </li>
        `).join('');
    }

    // Weather to Crop prominent card
    const weatherMeaningEl = document.getElementById('dash-weather-meaning');
    if (weatherMeaningEl) {
        weatherMeaningEl.textContent = lang === 'hi' ? r.weather_to_crop_meaning_hindi : r.weather_to_crop_meaning;
    }
}

function setBarValue(barId, valId, val) {
    const bar = document.getElementById(barId);
    const label = document.getElementById(valId);
    if (bar) {
        bar.style.width = `${val}%`;
        bar.className = `h-2 rounded-full transition-all duration-500 ${
            val >= 70 ? 'bg-red-500' : val >= 45 ? 'bg-amber-500' : 'bg-emerald-500'
        }`;
    }
    if (label) {
        label.textContent = `${val}/100`;
    }
}

// Profile UI
function renderProfileUI() {
    if (!AppState.profile) return;
    const p = AppState.profile;

    const nameInput = document.getElementById('prof-farmer-name');
    const districtSelect = document.getElementById('prof-district');
    const cropSelect = document.getElementById('prof-crop');
    const stageSelect = document.getElementById('prof-stage');
    const sizeInput = document.getElementById('prof-size');

    if (nameInput) nameInput.value = p.farmer_name;
    if (districtSelect) districtSelect.value = p.district;
    if (cropSelect) cropSelect.value = p.crop;
    if (stageSelect) stageSelect.value = p.crop_stage;
    if (sizeInput) sizeInput.value = p.farm_size_acres;
}

// Alerts UI
function renderAlertsUI() {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    const lang = AppState.language;

    alertsContainer.innerHTML = AppState.alerts.map(a => `
        <div class="kr-card p-4 border-l-4 ${a.severity === 'CRITICAL' ? 'border-l-red-500 bg-red-50/30' : 'border-l-amber-500 bg-amber-50/20'}">
            <div class="flex items-start justify-between">
                <div class="flex items-center gap-2">
                    <span class="text-2xl">${a.icon}</span>
                    <div>
                        <h4 class="font-bold text-slate-800">${lang === 'hi' ? a.title_hindi : a.title}</h4>
                        <span class="text-xs text-slate-500">${a.timestamp} • ${a.district}</span>
                    </div>
                </div>
                <span class="px-2 py-0.5 rounded text-xs font-semibold ${a.severity === 'CRITICAL' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'}">
                    ${a.severity}
                </span>
            </div>
            <p class="text-sm text-slate-700 mt-2"><strong>Reason:</strong> ${lang === 'hi' ? a.reason_hindi : a.reason}</p>
            <div class="mt-2 text-xs font-medium text-emerald-800 bg-emerald-100/60 p-2 rounded">
                <strong>Recommended Action:</strong> ${lang === 'hi' ? a.recommended_action_hindi : a.recommended_action}
            </div>
        </div>
    `).join('');
}

// Timeline UI
function renderTimelineUI() {
    const timelineContainer = document.getElementById('timeline-container');
    if (!timelineContainer) return;
    const lang = AppState.language;

    timelineContainer.innerHTML = AppState.timeline.map((item, idx) => `
        <div class="relative pl-6 pb-6 border-l-2 ${idx === 0 ? 'border-emerald-500' : 'border-slate-200'}">
            <div class="absolute -left-2 top-0 w-4 h-4 rounded-full ${idx === 0 ? 'bg-emerald-500 ring-4 ring-emerald-100' : 'bg-slate-300'}"></div>
            <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-xs">
                <div class="flex items-center justify-between text-xs text-slate-500">
                    <span>${item.timestamp}</span>
                    <span class="font-semibold text-slate-700">${item.crop} (${item.crop_stage})</span>
                </div>
                <div class="font-bold text-slate-800 text-sm mt-1">
                    ${lang === 'hi' ? item.hindi_issue : item.possible_issue}
                    <span class="text-xs font-normal text-slate-500">(${Math.round(item.confidence * 100)}% conf)</span>
                </div>
                <div class="text-xs text-slate-600 mt-1">${item.notes}</div>
            </div>
        </div>
    `).join('');
}

// Admin Metrics UI
function renderAdminUI() {
    if (!AppState.adminMetrics) return;
    const m = AppState.adminMetrics;

    const elFarms = document.getElementById('admin-monitored-farms');
    const elDistricts = document.getElementById('admin-high-risk-districts');
    const elFlood = document.getElementById('admin-flood-alerts');
    const elDisease = document.getElementById('admin-disease-alerts');

    if (elFarms) elFarms.textContent = m.monitored_farms.toLocaleString();
    if (elDistricts) elDistricts.textContent = m.high_risk_districts_count;
    if (elFlood) elFlood.textContent = m.active_flood_alerts_farms.toLocaleString();
    if (elDisease) elDisease.textContent = m.disease_outbreak_alerts.toLocaleString();

    // River basins table
    const tableBody = document.getElementById('admin-rivers-tbody');
    if (tableBody) {
        tableBody.innerHTML = m.river_basins_alert.map(r => `
            <tr class="border-b border-slate-100 text-sm">
                <td class="py-2.5 font-medium text-slate-800">${r.river}</td>
                <td class="py-2.5 text-slate-600">${r.status}</td>
                <td class="py-2.5">
                    <span class="px-2 py-0.5 rounded text-xs font-bold ${
                        r.risk === 'SEVERE' ? 'bg-red-100 text-red-700' :
                        r.risk === 'HIGH' ? 'bg-orange-100 text-orange-700' :
                        r.risk === 'DROUGHT' ? 'bg-amber-100 text-amber-700' :
                        'bg-blue-100 text-blue-700'
                    }">${r.risk}</span>
                </td>
            </tr>
        `).join('');
    }
}

// Utility Toast Notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-20 right-6 z-50 px-4 py-2.5 rounded-xl shadow-lg text-sm font-medium transition-all transform duration-300 flex items-center gap-2 ${
        type === 'success' ? 'bg-emerald-800 text-white' :
        type === 'error' ? 'bg-red-800 text-white' :
        'bg-slate-800 text-white'
    }`;
    toast.innerHTML = `<span>🔔</span> <span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

window.AppState = AppState;
window.showToast = showToast;
window.loadScenario = loadScenario;
window.switchTab = switchTab;
