/**
 * KhetRakshak - Core Client Application State, Router, Auth & Geolocation
 * Bihar's Crop Risk Intelligence & Early-Warning Platform
 */

const AppState = {
    language: 'hi', // default to Hindi as per Bihar Farmer Persona, toggleable to English
    currentTab: 'dashboard',
    theme: 'light',
    currentUser: null,
    profile: null,
    riskData: null,
    weatherImpact: null,
    alerts: [],
    timeline: [],
    adminMetrics: null,
    districtsGis: [],
    selectedDistrict: 'Purnia',
    demoAccounts: []
};

// 38 Districts of Bihar with agro-climatic coordinates for GPS matching
const BIHAR_38_DISTRICTS = [
    { name: "Purnia", hindi_name: "पूर्णिया", lat: 25.7771, lng: 87.4753, zone: "Zone II" },
    { name: "Katihar", hindi_name: "कटिहार", lat: 25.5414, lng: 87.5714, zone: "Zone II" },
    { name: "Bhagalpur", hindi_name: "भागलपुर", lat: 25.2425, lng: 86.9842, zone: "Zone III A" },
    { name: "Darbhanga", hindi_name: "दरभंगा", lat: 26.1542, lng: 85.8918, zone: "Zone I" },
    { name: "Saharsa", hindi_name: "सहरसा", lat: 25.8835, lng: 86.6006, zone: "Zone II" },
    { name: "Gaya", hindi_name: "गया", lat: 24.7914, lng: 85.0002, zone: "Zone III B" },
    { name: "Muzaffarpur", hindi_name: "मुजफ्फरपुर", lat: 26.1209, lng: 85.3647, zone: "Zone I" },
    { name: "Patna", hindi_name: "पटना", lat: 25.5941, lng: 85.1376, zone: "Zone III B" },
    { name: "Rohtas", hindi_name: "रोहतास (सासाराम)", lat: 24.9515, lng: 84.0163, zone: "Zone III B" },
    { name: "Samastipur", hindi_name: "समस्तीपुर", lat: 25.8629, lng: 85.7811, zone: "Zone I" },
    { name: "Begusarai", hindi_name: "बेगूसराय", lat: 25.4182, lng: 86.1272, zone: "Zone I" },
    { name: "Madhubani", hindi_name: "मधुबनी", lat: 26.3547, lng: 86.0718, zone: "Zone I" },
    { name: "Nalanda", hindi_name: "नालंदा (बिहारशरीफ)", lat: 25.2016, lng: 85.5247, zone: "Zone III B" },
    { name: "Nawada", hindi_name: "नवादा", lat: 24.8856, lng: 85.5435, zone: "Zone III B" },
    { name: "Aurangabad", hindi_name: "औरंगाबाद", lat: 24.7538, lng: 84.3742, zone: "Zone III B" },
    { name: "Bhojpur", hindi_name: "भोजपुर (आरा)", lat: 25.5560, lng: 84.6603, zone: "Zone III B" },
    { name: "Buxar", hindi_name: "बक्सर", lat: 25.5647, lng: 83.9777, zone: "Zone III B" },
    { name: "Kaimur", hindi_name: "कैमूर (भभुआ)", lat: 25.0427, lng: 83.5855, zone: "Zone III B" },
    { name: "Jehanabad", hindi_name: "जहानाबाद", lat: 25.2132, lng: 84.9867, zone: "Zone III B" },
    { name: "Arwal", hindi_name: "अरवल", lat: 25.2444, lng: 84.6738, zone: "Zone III B" },
    { name: "Saran", hindi_name: "सारण (छपरा)", lat: 25.7838, lng: 84.7460, zone: "Zone I" },
    { name: "Siwan", hindi_name: "सीवान", lat: 26.2223, lng: 84.3567, zone: "Zone I" },
    { name: "Gopalganj", hindi_name: "गोपालगंज", lat: 26.4673, lng: 84.4449, zone: "Zone I" },
    { name: "Vaishali", hindi_name: "वैशाली (हाजीपुर)", lat: 25.6858, lng: 85.2155, zone: "Zone I" },
    { name: "Sitamarhi", hindi_name: "सीतामढ़ी", lat: 26.5937, lng: 85.4893, zone: "Zone I" },
    { name: "Sheohar", hindi_name: "शिवहर", lat: 26.5204, lng: 85.2954, zone: "Zone I" },
    { name: "East Champaran", hindi_name: "पूर्वी चंपारण (मोतिहारी)", lat: 26.6469, lng: 84.9089, zone: "Zone I" },
    { name: "West Champaran", hindi_name: "पश्चिम चंपारण (बेतिया)", lat: 26.8024, lng: 84.5029, zone: "Zone I" },
    { name: "Supaul", hindi_name: "सुपौल", lat: 26.1260, lng: 86.6053, zone: "Zone II" },
    { name: "Madhepura", hindi_name: "मधेपुरा", lat: 25.9264, lng: 86.7909, zone: "Zone II" },
    { name: "Araria", hindi_name: "अररिया", lat: 26.1497, lng: 87.4986, zone: "Zone II" },
    { name: "Kishanganj", hindi_name: "किशनगंज", lat: 26.0964, lng: 87.9435, zone: "Zone II" },
    { name: "Munger", hindi_name: "मुंगेर", lat: 25.3757, lng: 86.4744, zone: "Zone III A" },
    { name: "Lakhisarai", hindi_name: "लखीसराय", lat: 25.1764, lng: 86.0945, zone: "Zone III A" },
    { name: "Sheikhpura", hindi_name: "शेखपुरा", lat: 25.1388, lng: 85.8576, zone: "Zone III B" },
    { name: "Jamui", hindi_name: "जमुई", lat: 24.9281, lng: 86.2232, zone: "Zone III A" },
    { name: "Khagaria", hindi_name: "खगड़िया", lat: 25.5034, lng: 86.4828, zone: "Zone II" },
    { name: "Banka", hindi_name: "बांका", lat: 24.8864, lng: 86.9238, zone: "Zone III A" }
];

// Bilingual Localized Strings
const I18N = {
    hi: {
        appName: 'खेतरक्षक',
        tagline: 'बिहार का फसल सुरक्षा एवं पूर्व-चेतावनी मंच',
        philosophy: '“मौसम बताता है क्या आ रहा है। फसल स्कैनर बताता है क्या हो रहा है। खेतरक्षक बताता है कि आपके खेत पर इसका क्या असर होगा।”',
        btnDemoAccounts: 'डेमो खाते',
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
        scanNow: 'फसल स्वास्थ्य जांच करें',
        exploreMap: 'बिहार जोखिम मानचित्र देखें',
        tabDashboard: 'डैशबोर्ड',
        tabScanner: 'फसल जांच',
        tabRisk: 'जोखिम',
        tabAlerts: 'अलर्ट',
        tabMore: 'अन्य',
        tabFlood: 'बाढ़ जोखिम',
        tabDrought: 'सूखा तनाव',
        tabWeather: 'मौसम-फसल',
        tabAdvisor: 'सलाहकार',
        tabVoice: 'आवाज AI',
        tabMap: 'बिहार मानचित्र',
        tabTimeline: 'समय-सारणी',
        tabProfile: 'मेरा खेत',
        tabAdmin: 'प्रशासन',
        tabAbout: 'परिचय',
        btnChangeLocation: 'स्थान बदलें',
        btnChangeLocShort: 'स्थान',
        btnLogout: 'लॉगआउट',
        lblDemoSelect: 'डेमो परिदृश्य:',
        authModalTitle: 'खेतरक्षक किसान पोर्टल (Farmer Portal)',
        disclaimerNotice: 'सूचना: खेतरक्षक एक निर्णय-सहायक प्रणाली है। आपदा प्रबंधन विभाग (बिहार सरकार) के आधिकारिक निर्देश सर्वोपरि हैं।'
    },
    en: {
        appName: 'KhetRakshak',
        tagline: "Bihar's Crop Risk Intelligence & Early-Warning Platform",
        philosophy: '“Weather tells you what is coming. Crop detection tells you what is happening. KhetRakshak tells you what it means for your farm.”',
        btnDemoAccounts: 'Demo Accounts',
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
        scanNow: 'Analyze Crop Health',
        exploreMap: 'Explore Bihar Risk Map',
        tabDashboard: 'Dashboard',
        tabScanner: 'Crop Scan',
        tabRisk: 'Risk',
        tabAlerts: 'Alerts',
        tabMore: 'More',
        tabFlood: 'Flood Risk',
        tabDrought: 'Drought & Water Stress',
        tabWeather: 'Weather-to-Crop',
        tabAdvisor: 'Ask Advisor',
        tabVoice: 'Voice AI',
        tabMap: 'Bihar Risk Map',
        tabTimeline: 'Farm Timeline',
        tabProfile: 'My Farm',
        tabAdmin: 'Admin Surveillance',
        tabAbout: 'About KhetRakshak',
        btnChangeLocation: 'Change Location',
        btnChangeLocShort: 'Location',
        btnLogout: 'Logout',
        lblDemoSelect: 'Demo Scenario:',
        authModalTitle: 'KhetRakshak Farmer Portal',
        disclaimerNotice: 'Notice: KhetRakshak is an agronomic decision-support platform. Official Bihar Disaster Management Department (DMD) alerts take legal precedence.'
    }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    setupTabNavigation();
    setupLanguageToggle();
    setupMoreMenu();
    setupAuthListeners();
    populateDistrictSelects();
    
    // Check saved session or load initial data
    await initSession();
    await loadInitialData();
});

// Theme Management (Light / Dark Mode)
function initTheme() {
    const savedTheme = localStorage.getItem('kr_theme') || 
        (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    setTheme(savedTheme);

    const themeBtn = document.getElementById('btn-theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleTheme);
    }
}

function setTheme(theme) {
    AppState.theme = theme;
    const root = document.documentElement;
    const themeIcon = document.getElementById('theme-icon');
    
    if (theme === 'dark') {
        root.classList.add('dark');
        if (themeIcon) themeIcon.textContent = '☀️';
    } else {
        root.classList.remove('dark');
        if (themeIcon) themeIcon.textContent = '🌙';
    }
    localStorage.setItem('kr_theme', theme);
}

function toggleTheme() {
    setTheme(AppState.theme === 'dark' ? 'light' : 'dark');
    showToast(AppState.theme === 'dark' ? 'Dark Mode Activated' : 'Light Mode Activated', 'info');
}

// Session & Authentication
async function initSession() {
    try {
        const savedUser = localStorage.getItem('khetrakshak_user');
        if (savedUser) {
            AppState.currentUser = JSON.parse(savedUser);
            renderAuthStatus();
        } else {
            // Default active demo user session
            AppState.currentUser = {
                id: 1,
                farmer_name: "Ramesh Kumar Yadav",
                mobile_number: "9800011111",
                district: "Purnia",
                block: "Kasba",
                village: "Madhavpur",
                primary_crop: "Maize"
            };
            renderAuthStatus();
        }
        await fetchDemoAccounts();
    } catch (e) {
        console.error("Session init error:", e);
    }
}

function renderAuthStatus() {
    const authBtnLabel = document.getElementById('auth-btn-label');
    const authBtnIcon = document.getElementById('auth-btn-icon');
    const authBtn = document.getElementById('btn-open-auth-modal');

    if (AppState.currentUser) {
        if (authBtnLabel) authBtnLabel.textContent = AppState.currentUser.farmer_name.split(' ')[0];
        if (authBtnIcon) authBtnIcon.textContent = '🧑🌾';
        if (authBtn) {
            authBtn.title = `Logged in as: ${AppState.currentUser.farmer_name}`;
            authBtn.className = "px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-800 hover:bg-emerald-900 text-white shadow-sm flex items-center gap-1.5 transition-all border border-emerald-600";
        }
    } else {
        if (authBtnLabel) authBtnLabel.textContent = AppState.language === 'hi' ? 'लॉगिन' : 'Login';
        if (authBtnIcon) authBtnIcon.textContent = '🔑';
        if (authBtn) {
            authBtn.title = "Click to Login or Register";
            authBtn.className = "px-3.5 py-1.5 rounded-lg text-xs font-bold bg-emerald-700 hover:bg-emerald-800 text-white shadow-sm flex items-center gap-1.5 transition-all";
        }
    }
}

async function fetchDemoAccounts() {
    try {
        const res = await fetch('/api/auth/demo-accounts');
        AppState.demoAccounts = await res.json();
        renderDemoAccountsList();
    } catch (e) {
        console.error("Failed to fetch demo accounts:", e);
    }
}

function renderDemoAccountsList() {
    const listAuth = document.getElementById('auth-demo-accounts-list');
    const listModal = document.getElementById('modal-demo-list');

    const html = AppState.demoAccounts.map(acc => `
        <div onclick="window.selectDemoAccount(${acc.id})" class="p-3 bg-slate-50 dark:bg-slate-800/80 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 border border-slate-200 dark:border-slate-700 hover:border-emerald-500 rounded-xl cursor-pointer transition-all">
            <div class="flex items-center justify-between">
                <span class="font-bold text-sm text-slate-900 dark:text-slate-100">${acc.farmer_name}</span>
                <span class="text-xs px-2 py-0.5 rounded-full font-bold bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200">
                    📍 ${acc.district}
                </span>
            </div>
            <div class="text-xs text-slate-600 dark:text-slate-300 mt-1 flex items-center gap-2">
                <span>🌾 ${acc.primary_crop} (${acc.land_area} Acres)</span>
                <span>•</span>
                <span>🌱 ${acc.crop_stage}</span>
            </div>
            <div class="text-[11px] text-slate-500 mt-0.5">
                📞 ${acc.mobile_number} | ${acc.village}, ${acc.block}
            </div>
        </div>
    `).join('');

    if (listAuth) listAuth.innerHTML = html;
    if (listModal) listModal.innerHTML = html;
}

window.selectDemoAccount = async function(demoId) {
    try {
        showToast("Loading Demo Account...", "info");
        const res = await fetch(`/api/auth/demo-login/${demoId}`, { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
            AppState.currentUser = data.user;
            AppState.profile = data.profile;
            localStorage.setItem('khetrakshak_user', JSON.stringify(data.user));
            
            closeAuthModal();
            closeDemoModal();
            renderAuthStatus();
            
            // Reload all telemetry & risk
            await Promise.all([
                fetchRiskEvaluation(),
                fetchWeatherToCrop(),
                fetchAlerts(),
                fetchTimeline()
            ]);
            
            renderDashboard();
            renderProfileUI();
            updateLocationNavbarLabel(data.profile.district);
            
            showToast(`Loaded: ${data.user.farmer_name} (${data.profile.district})`, "success");
            switchTab('dashboard');
        }
    } catch (err) {
        console.error("Demo login error:", err);
        showToast("Failed to load demo account", "error");
    }
};

window.submitLogin = async function() {
    const mobile = document.getElementById('login-mobile').value.trim();
    const password = document.getElementById('login-password').value.trim();

    if (!mobile || mobile.length < 10) {
        showToast("कृपया 10 अंकों का मान्य मोबाइल नंबर दर्ज करें", "error");
        return;
    }

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mobile_number: mobile, password: password || "123456" })
        });
        const data = await res.json();
        if (res.ok && data.status === 'success') {
            AppState.currentUser = data.user;
            AppState.profile = data.profile;
            localStorage.setItem('khetrakshak_user', JSON.stringify(data.user));
            closeAuthModal();
            renderAuthStatus();
            await fetchRiskEvaluation();
            renderDashboard();
            showToast(`नमस्ते, ${data.user.farmer_name}!`, "success");
        } else {
            showToast(data.detail || "लॉगिन असफल रहा। कृपया जांचें।", "error");
        }
    } catch (e) {
        console.error("Login failed:", e);
        showToast("सर्वर से संपर्क नहीं हो सका।", "error");
    }
};

window.submitRegister = async function() {
    const name = document.getElementById('reg-name').value.trim();
    const mobile = document.getElementById('reg-mobile').value.trim();
    const password = document.getElementById('reg-password').value.trim();
    const district = document.getElementById('reg-district').value;
    const block = document.getElementById('reg-block').value.trim();
    const village = document.getElementById('reg-village').value.trim();
    const crop = document.getElementById('reg-crop').value;
    const area = parseFloat(document.getElementById('reg-area').value) || 2.5;
    const stage = document.getElementById('reg-stage').value;

    if (!name || !mobile || mobile.length < 10) {
        showToast("कृपया नाम एवं 10 अंकों का मोबाइल नंबर भरें।", "error");
        return;
    }

    try {
        const res = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                farmer_name: name,
                mobile_number: mobile,
                password: password || "123456",
                district: district,
                block: block,
                village: village,
                primary_crop: crop,
                land_area: area,
                crop_stage: stage
            })
        });
        const data = await res.json();
        if (res.ok && data.status === 'success') {
            AppState.currentUser = data.user;
            AppState.profile = data.profile;
            localStorage.setItem('khetrakshak_user', JSON.stringify(data.user));
            closeAuthModal();
            renderAuthStatus();
            await fetchRiskEvaluation();
            renderDashboard();
            showToast(`पंजीकरण सफल! स्वागत है, ${data.user.farmer_name}`, "success");
            switchTab('dashboard');
        } else {
            showToast(data.detail || "पंजीकरण में त्रुटि आई।", "error");
        }
    } catch (e) {
        console.error("Register error:", e);
        showToast("पंजीकरण नहीं हो सका।", "error");
    }
};

window.logout = function() {
    localStorage.removeItem('khetrakshak_user');
    AppState.currentUser = null;
    renderAuthStatus();
    showToast("सफलतापूर्वक लॉगआउट हुए।", "info");
    // Switch to first demo account
    window.selectDemoAccount(1);
};

// Modals Controls
function setupAuthListeners() {
    const authBtn = document.getElementById('btn-open-auth-modal');
    if (authBtn) {
        authBtn.addEventListener('click', openAuthModal);
    }

    const demoBtn = document.getElementById('btn-open-demo-modal');
    if (demoBtn) {
        demoBtn.addEventListener('click', openDemoModal);
    }

    const locBtn = document.getElementById('btn-open-location-modal');
    if (locBtn) {
        locBtn.addEventListener('click', openLocationModal);
    }
}

window.openAuthModal = function() {
    const modal = document.getElementById('modal-auth');
    if (modal) modal.classList.add('active');
};

window.closeAuthModal = function() {
    const modal = document.getElementById('modal-auth');
    if (modal) modal.classList.remove('active');
};

window.switchAuthTab = function(tab) {
    const tabs = ['login', 'register', 'demo'];
    tabs.forEach(t => {
        const btn = document.getElementById(`auth-tab-btn-${t}`);
        const panel = document.getElementById(`auth-panel-${t}`);
        if (t === tab) {
            if (btn) btn.className = "flex-1 py-2.5 text-center text-emerald-700 border-b-2 border-emerald-600 font-extrabold";
            if (panel) panel.classList.remove('hidden');
        } else {
            if (btn) btn.className = "flex-1 py-2.5 text-center text-slate-500 hover:text-slate-800";
            if (panel) panel.classList.add('hidden');
        }
    });
};

window.openLocationModal = function() {
    const modal = document.getElementById('modal-location');
    if (modal) modal.classList.add('active');
};

window.closeLocationModal = function() {
    const modal = document.getElementById('modal-location');
    if (modal) modal.classList.remove('active');
};

window.openDemoModal = function() {
    const modal = document.getElementById('modal-demo-accounts');
    if (modal) modal.classList.add('active');
};

window.closeDemoModal = function() {
    const modal = document.getElementById('modal-demo-accounts');
    if (modal) modal.classList.remove('active');
};

window.toggleMobileMoreModal = function() {
    const modal = document.getElementById('modal-mobile-more');
    if (modal) modal.classList.toggle('active');
};

window.closeMobileMoreModal = function() {
    const modal = document.getElementById('modal-mobile-more');
    if (modal) modal.classList.remove('active');
};

// 3-Dot More Menu
function setupMoreMenu() {
    const btnMore = document.getElementById('btn-more-menu');
    const dropdown = document.getElementById('more-menu-dropdown');
    
    if (btnMore && dropdown) {
        btnMore.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('hidden');
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target) && e.target !== btnMore) {
                dropdown.classList.add('hidden');
            }
        });
    }

    // Secondary Tab Clicks in More Menu
    document.querySelectorAll('.more-menu-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
            if (dropdown) dropdown.classList.add('hidden');
        });
    });

    const moreDemo = document.getElementById('more-btn-demo');
    if (moreDemo) {
        moreDemo.addEventListener('click', () => {
            if (dropdown) dropdown.classList.add('hidden');
            openDemoModal();
        });
    }

    const moreLoc = document.getElementById('more-btn-location');
    if (moreLoc) {
        moreLoc.addEventListener('click', () => {
            if (dropdown) dropdown.classList.add('hidden');
            openLocationModal();
        });
    }

    const moreLogout = document.getElementById('more-btn-logout');
    if (moreLogout) {
        moreLogout.addEventListener('click', () => {
            if (dropdown) dropdown.classList.add('hidden');
            window.logout();
        });
    }
}

// 38 Districts Population
function populateDistrictSelects() {
    const selects = ['reg-district', 'loc-select-district', 'prof-district'];
    const optionsHtml = BIHAR_38_DISTRICTS.map(d => 
        `<option value="${d.name}">${d.name} (${d.hindi_name}) - ${d.zone}</option>`
    ).join('');

    selects.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = optionsHtml;
    });
}

// Geolocation with Haversine distance matching
function calculateDistanceKm(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

window.detectLocationFromGPS = function() {
    const statusMsg = document.getElementById('gps-status-msg');
    if (!navigator.geolocation) {
        showToast("आपका ब्राउज़र GPS लोकेशन को सपोर्ट नहीं करता।", "error");
        return;
    }

    if (statusMsg) {
        statusMsg.classList.remove('hidden');
        statusMsg.textContent = "उपग्रह से स्थान खोजा जा रहा है (Searching GPS coordinates)...";
    }

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;

            // Find closest Bihar district
            let closestDistrict = null;
            let minDistance = Infinity;

            BIHAR_38_DISTRICTS.forEach(d => {
                const dist = calculateDistanceKm(userLat, userLng, d.lat, d.lng);
                if (dist < minDistance) {
                    minDistance = dist;
                    closestDistrict = d;
                }
            });

            if (closestDistrict && minDistance <= 200) {
                // Inside or near Bihar
                if (statusMsg) {
                    statusMsg.textContent = `✓ स्थान मिला: ${closestDistrict.name} (${closestDistrict.hindi_name}) - ${Math.round(minDistance)} किमी दूरी`;
                }

                // Update location selector dropdown
                const locSelect = document.getElementById('loc-select-district');
                if (locSelect) locSelect.value = closestDistrict.name;

                // Apply update
                await applyDistrictLocation(closestDistrict.name, userLat, userLng, "GPS");
                closeLocationModal();
                showToast(`स्थान स्वतः पहचाना गया: ${closestDistrict.hindi_name} (GPS)`, "success");
            } else {
                if (statusMsg) {
                    statusMsg.textContent = `आपकी वर्तमान स्थिति (${userLat.toFixed(2)}, ${userLng.toFixed(2)}) बिहार से बाहर है। कृपया नीचे सूची से जिला चुनें।`;
                }
                showToast("वर्तमान लोकेशन बिहार से बाहर है। कृपया मैन्युअल जिला चुनें।", "info");
            }
        },
        (error) => {
            console.warn("Geolocation denied or failed:", error);
            if (statusMsg) {
                statusMsg.textContent = "लोकेशन अनुमति अस्वीकृत या उपलब्ध नहीं। कृपया नीचे दिए गए फॉर्म से जिला चुनें।";
            }
            showToast("GPS अनुमति नहीं मिली। कृपया मैन्युअल जिला चुनें।", "info");
        },
        { timeout: 10000, enableHighAccuracy: true }
    );
};

window.saveManualLocation = async function() {
    const district = document.getElementById('loc-select-district').value;
    const block = document.getElementById('loc-input-block').value.trim();
    const village = document.getElementById('loc-input-village').value.trim();

    const dObj = BIHAR_38_DISTRICTS.find(d => d.name === district) || BIHAR_38_DISTRICTS[0];
    await applyDistrictLocation(district, dObj.lat, dObj.lng, "Manual", block, village);
    closeLocationModal();
    showToast(`स्थान अपडेट हुआ: ${district}`, "success");
};

async function applyDistrictLocation(district, lat, lng, source = "Manual", block = "", village = "") {
    AppState.selectedDistrict = district;
    updateLocationNavbarLabel(district, source);

    if (AppState.profile) {
        AppState.profile.district = district;
        if (lat) AppState.profile.latitude = lat;
        if (lng) AppState.profile.longitude = lng;
        if (block) AppState.profile.block = block;
        if (village) AppState.profile.village = village;

        // Sync with backend
        try {
            await fetch('/api/profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(AppState.profile)
            });
            await fetchRiskEvaluation();
            await fetchWeatherToCrop();
            renderDashboard();
            renderProfileUI();
        } catch (e) {
            console.error("Failed to sync location profile:", e);
        }
    }
}

function updateLocationNavbarLabel(district, source = "") {
    const navLoc = document.getElementById('nav-location-label');
    if (navLoc) {
        navLoc.textContent = `${district}, Bihar${source === "GPS" ? " (GPS)" : ""}`;
    }
}

// Initial Data Loading
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

// Navigation Tabs & Routing
function setupTabNavigation() {
    const tabs = document.querySelectorAll('.nav-tab-btn, .mobile-tab-btn');
    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    const scenarioSelector = document.getElementById('demo-scenario-select');
    if (scenarioSelector) {
        scenarioSelector.addEventListener('change', async (e) => {
            if (e.target.value) {
                await loadScenario(e.target.value);
            }
        });
    }
}

function switchTab(tabId) {
    if (tabId === 'risk') {
        // Scroll smoothly to Risk section inside Dashboard
        switchTab('dashboard');
        setTimeout(() => {
            const riskCircle = document.getElementById('score-circle');
            if (riskCircle) riskCircle.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 150);
        return;
    }

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

    // Special handler for Bihar Map redraw
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

    const langBtnText = document.getElementById('lang-btn-text');
    if (langBtnText) {
        langBtnText.textContent = lang === 'hi' ? 'English' : 'हिंदी';
    }

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            el.textContent = t[key];
        }
    });

    renderAuthStatus();
    renderDashboard();
    renderAlertsUI();
    renderTimelineUI();
}

// API Calls
async function fetchProfile() {
    const res = await fetch('/api/profile');
    AppState.profile = await res.json();
    renderProfileUI();
    if (AppState.profile && AppState.profile.district) {
        updateLocationNavbarLabel(AppState.profile.district);
    }
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
            updateLocationNavbarLabel(data.profile.district);
            
            showToast(`Scenario Loaded: ${data.scenario.title}`, "success");
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
        farmerNameEl.textContent = `${p.farmer_name} (${p.village ? p.village + ', ' : ''}${p.block ? p.block + ', ' : ''}${p.district}, Bihar)`;
    }

    const farmMetaEl = document.getElementById('dash-farm-meta');
    if (farmMetaEl) {
        farmMetaEl.textContent = `${p.crop} • ${p.crop_stage} • ${p.farm_size_acres || p.land_area} ${p.land_area_unit || 'Acres'} • ${p.soil_type}`;
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
            <li class="flex items-start gap-2 text-sm text-slate-700 dark:text-slate-300">
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
            <li class="flex items-start gap-2 text-sm text-slate-800 dark:text-slate-200 font-medium bg-emerald-50 dark:bg-emerald-950/40 p-2.5 rounded-lg border border-emerald-100 dark:border-emerald-800">
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">✓</span>
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
    if (sizeInput) sizeInput.value = p.farm_size_acres || p.land_area;
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
                        <h4 class="font-bold text-slate-800 dark:text-slate-100">${lang === 'hi' ? a.title_hindi : a.title}</h4>
                        <span class="text-xs text-slate-500">${a.timestamp} • ${a.district}</span>
                    </div>
                </div>
                <span class="px-2 py-0.5 rounded text-xs font-semibold ${a.severity === 'CRITICAL' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'}">
                    ${a.severity}
                </span>
            </div>
            <p class="text-sm text-slate-700 dark:text-slate-300 mt-2"><strong>Reason:</strong> ${lang === 'hi' ? a.reason_hindi : a.reason}</p>
            <div class="mt-2 text-xs font-medium text-emerald-800 dark:text-emerald-300 bg-emerald-100/60 dark:bg-emerald-900/40 p-2 rounded">
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
        <div class="relative pl-6 pb-6 border-l-2 ${idx === 0 ? 'border-emerald-500' : 'border-slate-200 dark:border-slate-700'}">
            <div class="absolute -left-2 top-0 w-4 h-4 rounded-full ${idx === 0 ? 'bg-emerald-500 ring-4 ring-emerald-100' : 'bg-slate-300 dark:bg-slate-600'}"></div>
            <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-700 shadow-xs">
                <div class="flex items-center justify-between text-xs text-slate-500">
                    <span>${item.timestamp}</span>
                    <span class="font-semibold text-slate-700 dark:text-slate-300">${item.crop} (${item.crop_stage})</span>
                </div>
                <div class="font-bold text-slate-800 dark:text-slate-100 text-sm mt-1">
                    ${lang === 'hi' ? item.hindi_issue : item.possible_issue}
                    <span class="text-xs font-normal text-slate-500">(${Math.round(item.confidence * 100)}% conf)</span>
                </div>
                <div class="text-xs text-slate-600 dark:text-slate-400 mt-1">${item.notes}</div>
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
            <tr class="border-b border-slate-100 dark:border-slate-800 text-sm">
                <td class="py-2.5 font-medium text-slate-800 dark:text-slate-200">${r.river}</td>
                <td class="py-2.5 text-slate-600 dark:text-slate-400">${r.status}</td>
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

// Toast Notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `kr-toast ${
        type === 'success' ? 'bg-emerald-800 text-white' :
        type === 'error' ? 'bg-red-800 text-white' :
        'bg-slate-900 text-white'
    }`;
    toast.innerHTML = `<span>${type === 'success' ? '✓' : type === 'error' ? '⚠️' : 'ℹ️'}</span> <span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

// Global Exports
window.AppState = AppState;
window.showToast = showToast;
window.loadScenario = loadScenario;
window.switchTab = switchTab;
