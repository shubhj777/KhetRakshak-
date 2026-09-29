/**
 * KhetRakshak - Voice AI Assistant Module
 * Provides Speech-to-Text, Voice Intent Processing, and Text-to-Speech (TTS)
 * with dedicated support for Hindi (hi-IN) and English (en-IN).
 */

let recognition = null;
let isRecording = false;

document.addEventListener('DOMContentLoaded', () => {
    initSpeechRecognition();
    setupVoiceListeners();
});

function initSpeechRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
        recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'hi-IN'; // Default Hindi

        recognition.onstart = () => {
            isRecording = true;
            updateRecordingUI(true);
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            handleVoiceQuery(transcript);
        };

        recognition.onerror = (event) => {
            console.warn("Speech recognition error:", event.error);
            isRecording = false;
            updateRecordingUI(false);
            showToast("Voice capture stopped or unsupported. You can also click sample voice prompts.", "info");
        };

        recognition.onend = () => {
            isRecording = false;
            updateRecordingUI(false);
        };
    } else {
        console.warn("Web Speech API not supported in this browser environment.");
    }
}

function setupVoiceListeners() {
    const micBtn = document.getElementById('btn-voice-mic');
    const voiceLangSelect = document.getElementById('voice-lang-select');
    
    if (micBtn) {
        micBtn.addEventListener('click', toggleVoiceRecording);
    }

    if (voiceLangSelect && recognition) {
        voiceLangSelect.addEventListener('change', (e) => {
            recognition.lang = e.target.value;
        });
    }

    // Quick Voice Prompt chips (Essential for judge testing without physical mic)
    document.querySelectorAll('.voice-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const queryText = chip.getAttribute('data-query');
            const lang = chip.getAttribute('data-lang') || 'hi';
            handleVoiceQuery(queryText, lang);
        });
    });
}

function toggleVoiceRecording() {
    if (!recognition) {
        showToast("Speech recognition is not supported in this browser. Please use quick prompts or type.", "info");
        return;
    }

    if (isRecording) {
        recognition.stop();
    } else {
        const langSelect = document.getElementById('voice-lang-select');
        if (langSelect) recognition.lang = langSelect.value;
        try {
            recognition.start();
        } catch (e) {
            console.error(e);
        }
    }
}

function updateRecordingUI(recording) {
    const micBtn = document.getElementById('btn-voice-mic');
    const waveContainer = document.getElementById('voice-wave-container');
    const statusText = document.getElementById('voice-status-text');

    if (micBtn) {
        if (recording) {
            micBtn.classList.add('bg-red-600', 'animate-pulse');
            micBtn.classList.remove('bg-emerald-600');
        } else {
            micBtn.classList.remove('bg-red-600', 'animate-pulse');
            micBtn.classList.add('bg-emerald-600');
        }
    }

    if (waveContainer) {
        if (recording) waveContainer.classList.add('recording');
        else waveContainer.classList.remove('recording');
    }

    if (statusText) {
        statusText.textContent = recording ? '🎙️ Listening... (बोलिए, खेतरक्षक सुन रहा है)' : 'Tap microphone to speak (माइक्रोफ़ोन दबाकर बोलें)';
    }
}

async function handleVoiceQuery(queryText, lang = 'hi') {
    const transcriptEl = document.getElementById('voice-transcript-text');
    const answerContainer = document.getElementById('voice-answer-container');
    const answerTextEl = document.getElementById('voice-answer-text');
    const sourcesEl = document.getElementById('voice-sources-list');

    if (transcriptEl) transcriptEl.textContent = `"${queryText}"`;

    if (answerTextEl) {
        answerTextEl.innerHTML = `<span class="animate-pulse">Thinking... (खेतरक्षक विचार कर रहा है...)</span>`;
    }
    if (answerContainer) answerContainer.classList.remove('hidden');

    try {
        const res = await fetch('/api/voice-query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                transcript: queryText,
                language: lang
            })
        });

        const data = await res.json();

        const spokenAnswer = data.audio_spoken_text || data.response_hindi || data.response_text;
        if (answerTextEl) {
            answerTextEl.textContent = spokenAnswer;
        }

        if (sourcesEl && data.sources) {
            sourcesEl.innerHTML = data.sources.map(s => `<li class="text-[11px] text-emerald-800">🏛️ ${s}</li>`).join('');
        }

        // Speak aloud via Text-to-Speech
        speakSpokenResponse(spokenAnswer, lang);

    } catch (e) {
        console.error("Voice query failed:", e);
        if (answerTextEl) {
            answerTextEl.textContent = "Unable to process query. Please check network.";
        }
    }
}

function speakSpokenResponse(text, lang = 'hi') {
    if (!('speechSynthesis' in window)) return;

    window.speechSynthesis.cancel(); // Stop any pending speech

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-IN';
    utterance.rate = 0.95; // Clear deliberate pace for farmers
    utterance.pitch = 1.0;

    window.speechSynthesis.speak(utterance);
}

window.handleVoiceQuery = handleVoiceQuery;
window.speakSpokenResponse = speakSpokenResponse;
