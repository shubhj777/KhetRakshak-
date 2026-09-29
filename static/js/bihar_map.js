/**
 * KhetRakshak - Bihar Agricultural Risk GIS Map
 * Interactive Leaflet Map with District-level multi-risk visualization,
 * river basin overlays, and farm locator.
 */

let mapInstance = null;
let districtMarkersLayer = null;
let farmPinMarker = null;

function initBiharGISMap(districts) {
    const mapContainer = document.getElementById('bihar-map');
    if (!mapContainer) return;

    if (mapInstance) {
        mapInstance.remove();
        mapInstance = null;
    }

    // Centered over Bihar
    mapInstance = L.map('bihar-map', {
        center: [25.75, 85.7],
        zoom: 7.5,
        minZoom: 7,
        maxZoom: 12,
        scrollWheelZoom: false
    });

    // High quality OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | KhetRakshak GIS'
    }).addTo(mapInstance);

    districtMarkersLayer = L.layerGroup().addTo(mapInstance);

    // Plot all districts
    districts.forEach(d => {
        let markerColor = '#16a34a';
        let riskLabel = 'NORMAL';
        const floodRisk = d.historical_flood_risk;
        const droughtRisk = d.historical_drought_risk;

        if (floodRisk >= 85) {
            markerColor = '#dc2626'; // Red for severe flood risk
            riskLabel = 'HIGH FLOOD RISK';
        } else if (droughtRisk >= 80) {
            markerColor = '#d97706'; // Amber/Orange for severe drought risk
            riskLabel = 'HIGH DROUGHT RISK';
        } else if (floodRisk >= 65 || droughtRisk >= 60) {
            markerColor = '#ea580c';
            riskLabel = 'MODERATE RISK';
        }

        const circleMarker = L.circleMarker([d.lat, d.lng], {
            radius: floodRisk >= 85 || droughtRisk >= 80 ? 12 : 9,
            fillColor: markerColor,
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.85
        });

        // Popup HTML
        const popupContent = `
            <div class="text-xs space-y-1.5 min-w-[210px]">
                <div class="flex items-center justify-between border-b pb-1">
                    <span class="font-bold text-sm text-slate-800">${d.name} (${d.hindi_name})</span>
                    <span class="px-1.5 py-0.5 rounded text-[10px] font-bold text-white" style="background-color: ${markerColor}">
                        ${riskLabel}
                    </span>
                </div>
                <div><strong class="text-slate-500">Zone:</strong> ${d.zone}</div>
                <div><strong class="text-slate-500">River Basin:</strong> ${d.river_basin}</div>
                <div class="grid grid-cols-2 gap-1 py-1 bg-slate-50 p-1.5 rounded">
                    <div><strong>Flood:</strong> ${d.historical_flood_risk}/100</div>
                    <div><strong>Drought:</strong> ${d.historical_drought_risk}/100</div>
                    <div><strong>24h Rain:</strong> ${d.current_rainfall_24h_mm} mm</div>
                    <div><strong>Crops:</strong> ${d.major_crops[0]}</div>
                </div>
                <div class="p-1.5 bg-amber-50 border border-amber-200 rounded text-amber-900 text-[11px]">
                    <strong>Alert:</strong> ${d.active_alert}
                </div>
                <button onclick="window.selectDistrictFromMap('${d.name}')" class="w-full mt-1 px-2 py-1 bg-emerald-700 text-white rounded text-center text-xs font-semibold hover:bg-emerald-800">
                    📍 Focus My Farm Here
                </button>
            </div>
        `;

        circleMarker.bindPopup(popupContent);
        districtMarkersLayer.addLayer(circleMarker);
    });

    // Add Focus My Farm Button listener
    const btnFocus = document.getElementById('btn-focus-farm');
    if (btnFocus) {
        btnFocus.addEventListener('click', focusOnCurrentFarm);
    }

    // Default focus
    focusOnCurrentFarm();

    window.BiharMap = mapInstance;
}

function focusOnCurrentFarm() {
    if (!mapInstance || !window.AppState || !window.AppState.profile) return;
    const p = window.AppState.profile;
    const lat = p.latitude || 25.7771;
    const lng = p.longitude || 87.4753;

    mapInstance.flyTo([lat, lng], 9, { duration: 1.5 });

    if (farmPinMarker) {
        mapInstance.removeLayer(farmPinMarker);
    }

    // Custom Farm Icon
    const farmIcon = L.divIcon({
        className: 'custom-farm-pin',
        html: `<div class="w-8 h-8 rounded-full bg-emerald-600 border-2 border-white shadow-lg flex items-center justify-center text-white text-sm font-bold animate-bounce">🏡</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    farmPinMarker = L.marker([lat, lng], { icon: farmIcon }).addTo(mapInstance);
    farmPinMarker.bindPopup(`
        <div class="text-xs">
            <strong class="text-emerald-800 text-sm">📍 Your Monitored Farm</strong><br>
            <strong>Farmer:</strong> ${p.farmer_name}<br>
            <strong>District:</strong> ${p.district} (${p.village_block || ''})<br>
            <strong>Crop:</strong> ${p.crop} (${p.crop_stage})<br>
            <strong>Risk Status:</strong> <span class="text-red-600 font-bold">72/100 HIGH RISK</span>
        </div>
    `).openPopup();
}

window.selectDistrictFromMap = async function(districtName) {
    if (window.AppState && window.AppState.profile) {
        window.AppState.profile.district = districtName;
        // Save to backend
        await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(window.AppState.profile)
        });
        await fetchRiskEvaluation();
        await fetchWeatherToCrop();
        renderDashboard();
        focusOnCurrentFarm();
        showToast(`Farm location updated to ${districtName}`, 'success');
    }
};

window.initBiharGISMap = initBiharGISMap;
