/**
 * KhetRakshak AI - Crop Health Scanner Module
 * Handles Camera/Upload, Computer Vision Quality Assessment,
 * Disease Diagnosis, and Responsible AI Low-Confidence Safeguards.
 */

let selectedFile = null;
let currentSampleKey = 'maize_maydis_blight';
let liveCameraStream = null;

document.addEventListener('DOMContentLoaded', () => {
    setupScannerListeners();
});

function setupScannerListeners() {
    const fileInput = document.getElementById('scanner-file-input');
    const dropZone = document.getElementById('scanner-dropzone');
    const btnScan = document.getElementById('btn-analyze-scan');
    const btnLowConf = document.getElementById('btn-test-low-confidence');
    const btnCameraToggle = document.getElementById('btn-camera-toggle');

    // Sample Image Chips
    document.querySelectorAll('.sample-image-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.sample-image-chip').forEach(c => c.classList.remove('ring-2', 'ring-emerald-500', 'bg-emerald-50'));
            chip.classList.add('ring-2', 'ring-emerald-500', 'bg-emerald-50');
            
            currentSampleKey = chip.getAttribute('data-sample');
            selectedFile = null;
            
            // Update preview image
            const previewImg = document.getElementById('scanner-preview-img');
            if (previewImg) {
                previewImg.src = `/static/sample_images/${currentSampleKey}.jpg`;
                previewImg.classList.remove('hidden');
                document.getElementById('scanner-placeholder').classList.add('hidden');
            }

            // Sync crop selector if sample matches
            const cropSelect = document.getElementById('scanner-crop-select');
            if (cropSelect) {
                if (currentSampleKey.includes('maize')) cropSelect.value = 'Maize';
                else if (currentSampleKey.includes('paddy')) cropSelect.value = 'Paddy';
            }
        });
    });

    // File Input change
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleUploadedFile(e.target.files[0]);
            }
        });
    }

    // Drag and Drop
    if (dropZone) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-emerald-500', 'bg-emerald-50/50');
        });
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-emerald-500', 'bg-emerald-50/50');
        });
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-emerald-500', 'bg-emerald-50/50');
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleUploadedFile(e.dataTransfer.files[0]);
            }
        });
    }

    // Camera Toggle
    if (btnCameraToggle) {
        btnCameraToggle.addEventListener('click', toggleCameraStream);
    }

    // Scan Buttons
    if (btnScan) {
        btnScan.addEventListener('click', () => executeScan(false));
    }

    if (btnLowConf) {
        btnLowConf.addEventListener('click', () => executeScan(true));
    }
}

function handleUploadedFile(file) {
    selectedFile = file;
    currentSampleKey = null;

    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImg = document.getElementById('scanner-preview-img');
        const placeholder = document.getElementById('scanner-placeholder');
        if (previewImg) {
            previewImg.src = e.target.result;
            previewImg.classList.remove('hidden');
        }
        if (placeholder) {
            placeholder.classList.add('hidden');
        }
    };
    reader.readAsDataURL(file);
}

async function toggleCameraStream() {
    const video = document.getElementById('scanner-camera-video');
    const previewImg = document.getElementById('scanner-preview-img');
    const placeholder = document.getElementById('scanner-placeholder');
    const btnToggle = document.getElementById('btn-camera-toggle');

    if (liveCameraStream) {
        // Stop stream
        liveCameraStream.getTracks().forEach(t => t.stop());
        liveCameraStream = null;
        video.classList.add('hidden');
        btnToggle.textContent = '📷 Open Camera';
        return;
    }

    try {
        liveCameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        video.srcObject = liveCameraStream;
        video.classList.remove('hidden');
        if (previewImg) previewImg.classList.add('hidden');
        if (placeholder) placeholder.classList.add('hidden');
        btnToggle.textContent = '⏹️ Capture Photo';
    } catch (err) {
        console.warn("Camera access denied or unavailable:", err);
        showToast("Camera not accessible on this device. Using field sample images.", "info");
    }
}

async function executeScan(simulateLowConfidence = false) {
    const btnScan = document.getElementById('btn-analyze-scan');
    const cropSelect = document.getElementById('scanner-crop-select');
    const stageSelect = document.getElementById('scanner-stage-select');
    const resultsContainer = document.getElementById('scan-results-container');

    const crop = cropSelect ? cropSelect.value : 'Maize';
    const stage = stageSelect ? stageSelect.value : 'Flowering';

    if (btnScan) {
        btnScan.disabled = true;
        btnScan.innerHTML = `<span class="animate-spin inline-block mr-2">⚙️</span> Analyzing Foliage...`;
    }

    try {
        let responseData;

        // If camera stream is live, capture frame to canvas
        const video = document.getElementById('scanner-camera-video');
        if (liveCameraStream && video && !video.classList.contains('hidden')) {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const dataUrl = canvas.toDataURL('image/jpeg', 0.85);

            const res = await fetch('/api/scan-crop-json', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_base64: dataUrl,
                    crop: crop,
                    crop_stage: stage,
                    simulate_low_confidence: simulateLowConfidence
                })
            });
            responseData = await res.json();
        } else if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('crop', crop);
            formData.append('crop_stage', stage);
            formData.append('simulate_low_confidence', simulateLowConfidence);

            const res = await fetch('/api/scan-crop', {
                method: 'POST',
                body: formData
            });
            responseData = await res.json();
        } else {
            // Using preset sample image
            const res = await fetch('/api/scan-crop-json', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sample_key: currentSampleKey || 'maize_maydis_blight',
                    crop: crop,
                    crop_stage: stage,
                    simulate_low_confidence: simulateLowConfidence
                })
            });
            responseData = await res.json();
        }

        renderScanResults(responseData.quality, responseData.diagnosis);
        if (resultsContainer) {
            resultsContainer.classList.remove('hidden');
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Re-fetch risk evaluation and timeline
        if (window.AppState) {
            await Promise.all([
                fetchRiskEvaluation(),
                fetchTimeline()
            ]);
            renderDashboard();
        }
    } catch (err) {
        console.error("Scan analysis failed:", err);
        showToast("Scan analysis encountered an issue", "error");
    } finally {
        if (btnScan) {
            btnScan.disabled = false;
            btnScan.innerHTML = `🔍 Run AI Diagnostic Scan`;
        }
    }
}

function renderScanResults(quality, diagnosis) {
    const lang = window.AppState ? window.AppState.language : 'hi';

    // 1. Step 1 Quality Card
    const qualityBadge = document.getElementById('scan-quality-badge');
    const qualityMsg = document.getElementById('scan-quality-msg');
    const qualityMetrics = document.getElementById('scan-quality-metrics');

    if (qualityBadge) {
        qualityBadge.className = `px-3 py-1 rounded-full text-xs font-bold ${
            quality.is_valid ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-red-100 text-red-800 border border-red-300'
        }`;
        qualityBadge.textContent = quality.is_valid ? '✓ QUALITY VERIFIED' : `⚠️ QUALITY REJECTED: ${quality.status_code}`;
    }

    if (qualityMsg) {
        qualityMsg.textContent = lang === 'hi' ? quality.message_hindi : quality.message;
    }

    if (qualityMetrics) {
        qualityMetrics.innerHTML = `
            <div class="grid grid-cols-3 gap-2 text-xs text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-200 mt-2">
                <div><strong>Sharpness:</strong> ${quality.blur_score} (${quality.is_blurry ? 'Blurry' : 'Sharp'})</div>
                <div><strong>Brightness:</strong> ${quality.brightness} (${quality.is_dark ? 'Too Dark' : quality.is_overexposed ? 'Overexposed' : 'Good'})</div>
                <div><strong>Foliage Green:</strong> ${quality.green_coverage_pct}%</div>
            </div>
        `;
    }

    // 2. Step 2 Disease Card
    const diseaseContainer = document.getElementById('scan-disease-card');
    if (!diseaseContainer) return;

    if (!quality.is_valid) {
        if (quality.status_code === 'NOT_CROP') {
            diseaseContainer.innerHTML = `
                <div class="p-4 bg-rose-50 dark:bg-rose-950/40 border-2 border-rose-300 dark:border-rose-800 rounded-xl text-rose-900 dark:text-rose-200 text-sm">
                    <div class="font-bold flex items-center gap-2 text-base text-rose-800 dark:text-rose-300">
                        <span>🚫</span>
                        <span>${lang === 'hi' ? 'गैर-कृषि वस्तु अस्वीकृत (Non-Agricultural Image Rejected)' : 'Non-Agricultural Object Rejected'}</span>
                    </div>
                    <p class="mt-2 font-medium leading-relaxed">
                        ${lang === 'hi' 
                            ? 'कृपया फसल की पत्ती या पौधे की स्पष्ट तस्वीर अपलोड करें। वाहन, चेहरे, दस्तावेज या गैर-कृषि तस्वीरों का निदान नहीं किया जा सकता।' 
                            : 'Please upload a clear photograph of a crop leaf or plant. Images of animals, vehicles, humans, documents, or indoor scenes cannot be diagnosed.'}
                    </p>
                    <div class="mt-3 p-2.5 bg-white dark:bg-slate-900 rounded-lg border border-rose-200 dark:border-rose-800 text-xs text-slate-600 dark:text-slate-400">
                        <strong>🛡️ ${lang === 'hi' ? 'जिम्मेदार एआई नियम:' : 'Responsible AI Guardrail:'}</strong> ${lang === 'hi' ? 'खेतरक्षक किसी भी गैर-कृषि फोटो पर मनगढ़ंत रोग या कीटनाशक का सुझाव नहीं देता।' : 'KhetRakshak strictly refuses to hallucinate crop diseases or pesticides on unrelated photographs.'}
                    </div>
                    <div class="mt-3 flex gap-2">
                        <button onclick="document.getElementById('scanner-file-input').click()" class="px-3.5 py-1.5 bg-rose-700 hover:bg-rose-800 text-white rounded-lg text-xs font-semibold">
                            ${lang === 'hi' ? 'फसल की फोटो अपलोड करें' : 'Upload Crop Leaf Photo'}
                        </button>
                    </div>
                </div>
            `;
        } else {
            diseaseContainer.innerHTML = `
                <div class="p-4 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 rounded-xl text-amber-900 dark:text-amber-200 text-sm">
                    <div class="font-bold flex items-center gap-2">
                        <span>🛑</span>
                        <span>${lang === 'hi' ? 'गुणवत्ता जांच असफल - निदान स्थगित' : 'Quality Check Failed - Diagnosis Withheld'}</span>
                    </div>
                    <p class="mt-1">${lang === 'hi' ? quality.message_hindi : quality.message}</p>
                    <div class="mt-3 flex gap-2">
                        <button onclick="document.getElementById('scanner-file-input').click()" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold">
                            ${lang === 'hi' ? 'साफ फोटो दोबारा लें' : 'Take Another Photo'}
                        </button>
                    </div>
                </div>
            `;
        }
        return;
    }

    // Low confidence handling
    if (diagnosis.is_low_confidence) {
        diseaseContainer.innerHTML = `
            <div class="p-4 bg-orange-50 border-2 border-orange-300 rounded-xl text-orange-900 text-sm">
                <div class="font-bold text-base flex items-center gap-2 text-orange-800">
                    <span>⚠️</span>
                    <span>${lang === 'hi' ? 'एआई का विश्वास स्तर कम है (Low Confidence Safeguard)' : 'AI Confidence Low (Responsible AI Safeguard)'}</span>
                </div>
                <div class="mt-2 text-xs font-semibold text-orange-700">
                    Confidence: ${diagnosis.confidence_display} | Threshold Required: 65%
                </div>
                <p class="mt-2 text-slate-700">
                    ${lang === 'hi' 
                        ? 'एआई इस लक्षण को लेकर पूरी तरह आश्वस्त नहीं है। हम अनुमान के आधार पर रासायनिक कीटनाशक के छिड़काव की सलाह नहीं देते।' 
                        : 'The AI is not confident enough to provide a reliable identification. Symptoms overlap between multiple nutrient deficiencies or early pathogens.'}
                </p>
                <div class="mt-3 p-3 bg-white rounded-lg border border-orange-200">
                    <div class="font-semibold text-slate-800 text-xs mb-1">Recommended Safe Next Steps:</div>
                    <ul class="text-xs text-slate-600 space-y-1">
                        <li>• Take another photo in brighter daylight from a closer distance.</li>
                        <li>• Avoid applying toxic chemicals until verified by an expert.</li>
                        <li>• Consult Krishi Vigyan Kendra (KVK) Bhagalpur or Sabour scientists with a leaf sample.</li>
                    </ul>
                </div>
            </div>
        `;
        return;
    }

    // Standard High-Confidence Diagnosis Display
    diseaseContainer.innerHTML = `
        <div class="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3">
            <div class="flex items-start justify-between">
                <div>
                    <span class="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">
                        ${diagnosis.crop} • ${diagnosis.pathogen_type}
                    </span>
                    <h3 class="text-lg font-bold text-slate-900 mt-1">
                        ${lang === 'hi' ? diagnosis.hindi_issue : diagnosis.possible_issue}
                    </h3>
                </div>
                <div class="text-right">
                    <div class="text-xl font-black text-emerald-700">${diagnosis.confidence_display}</div>
                    <div class="text-[10px] text-slate-500 uppercase tracking-wider">AI Confidence</div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="bg-slate-50 p-2 rounded-lg border border-slate-200">
                    <span class="text-slate-500">Severity:</span>
                    <span class="font-bold text-slate-800 ml-1">${lang === 'hi' ? diagnosis.severity_hindi : diagnosis.severity}</span>
                </div>
                <div class="bg-slate-50 p-2 rounded-lg border border-slate-200">
                    <span class="text-slate-500">Model Type:</span>
                    <span class="font-bold text-slate-800 ml-1">Demo Computer Vision</span>
                </div>
            </div>

            <div>
                <h5 class="text-xs font-bold uppercase text-slate-500 tracking-wider mb-1">Identified Symptoms:</h5>
                <ul class="text-xs text-slate-700 space-y-1 list-disc list-inside">
                    ${(lang === 'hi' ? diagnosis.symptoms_hindi : diagnosis.symptoms).map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>

            <div class="bg-emerald-50 border border-emerald-200 p-3 rounded-lg">
                <div class="text-xs font-bold text-emerald-900 mb-0.5">🌱 Recommended Treatment / Action:</div>
                <p class="text-xs text-emerald-800 font-medium">
                    ${lang === 'hi' ? diagnosis.immediate_action_hindi : diagnosis.immediate_action}
                </p>
            </div>

            <div class="text-[11px] text-slate-400 italic">
                ${diagnosis.disclaimer}
            </div>
        </div>
    `;
}

window.executeScan = executeScan;
