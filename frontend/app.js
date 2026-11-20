/**
 * Annadata (अन्नदाता) - Smart Crop Advisory System
 * Frontend Application Controller
 */

const API_BASE = window.location.origin;

// State management
let currentLanguage = 'hi';
let currentDashboardData = null;
let currentDiseaseData = {
    disease_id: "wheat_leaf_rust",
    disease_name_hi: "पत्ती रस्ट (गेहूं)",
    disease_name_en: "Leaf Rust (Puccinia triticina)",
    confidence_score: 94.0,
    severity: "मध्यम से उच्च (Moderate to High)",
    symptoms_hi: "पत्तियों की ऊपरी सतह पर छोटे, गोल-अंडाकार नारंगी-भूरे रंग के दाने (Pustules) बन जाते हैं जो हाथ लगाने पर पीले-भूरे पाउडर की तरह छूटते हैं।",
    organic_remedies_hi: [
        "नीम का तेल (5 मिली प्रति लीटर पानी) का छिड़काव करें।",
        "ट्राइकोडर्मा विरिडी (5-10 ग्राम/लीटर) का पर्णीय छिड़काव करें।",
        "खट्टी छाछ (50 मिली/लीटर) का छिड़काव फफूंद रोकने में सहायक है।"
    ],
    chemical_remedies_hi: [
        "प्रोपिकोनाजोल 25% EC (टिल्ट) @ 1 मिली प्रति लीटर पानी (200 मिली प्रति एकड़) का छिड़काव करें।",
        "टेबुकोनाजोल 25.9% EC @ 1-1.25 मिली प्रति लीटर पानी।",
        "मेंकोजेब 75% WP @ 2 ग्राम प्रति लीटर पानी का छिड़काव दोहराएं।"
    ],
    prevention_hi: "रोग प्रतिरोधी किस्मों (जैसे HD-2967, HD-3086, DBW-187) का चयन करें। समय पर बुवाई करें और अत्यधिक नाइट्रोजन उर्वरक से बचें।",
    voice_text_hi: "आपके गेहूं के पत्ते में पत्ती रस्ट यानी रतुआ रोग के लक्षण पाए गए हैं। तुरंत प्रोपिकोनाजोल 1 मिली प्रति लीटर पानी में मिलाकर छिड़कें, या नीम तेल 5 मिली प्रति लीटर का उपयोग करें।"
};

// Multilingual Translations Dictionary
const TRANSLATIONS = {
    hi: {
        brand_title: "अन्नदाता",
        brand_tagline: "सही सलाह, बेहतर फसल",
        location_btn: "स्थान बदलें",
        new_advice: "नयी सलाह प्राप्त करें",
        farm_info: "खेत की जानकारी",
        farm_size: "खेत का आकार",
        soil_type: "मिटटी का प्रकार",
        main_crop: "मुख्य फसल",
        last_update: "आखिरी अपडेट",
        today_advice: "आज की सलाह",
        pest_detect: "कीट एवं रोग पहचानें",
        pest_sub: "फसल के पत्ते की फोटो अपलोड करें और रोग जानें",
        upload_title: "फोटो अपलोड करें",
        upload_sub: "JPG, PNG (अधिकतम 5MB)",
        recent_diag: "हाल की पहचान",
        yield_est: "उपज का अनुमान",
        yield_sub: "आपके खेत के लिए अनुमानित उपज",
        yield_status: "उपज की स्थिति:",
        factors: "ध्यान में रखे गए कारक",
        quick_actions: "त्वरित कार्य",
        crop_adv: "फसल की सलाह",
        soil_test: "मिट्टी की जाँच",
        fert_adv: "खाद की सलाह",
        irrig_plan: "सिंचाई योजना",
        weather_info: "मौसम जानकारी",
        mandi_rates: "बाजार भाव",
        adv_history: "सलाह इतिहास",
        settings: "सेटिंग्स",
        help: "सहायता"
    },
    en: {
        brand_title: "Annadata",
        brand_tagline: "Right Advice, Better Harvest",
        location_btn: "Change Location",
        new_advice: "Get New Advisory",
        farm_info: "Farm Overview",
        farm_size: "Farm Size",
        soil_type: "Soil Type",
        main_crop: "Primary Crop",
        last_update: "Last Updated",
        today_advice: "Today's Advisory",
        pest_detect: "Detect Pests & Diseases",
        pest_sub: "Upload leaf image to identify disease & treatment",
        upload_title: "Upload Crop Photo",
        upload_sub: "JPG, PNG (Max 5MB)",
        recent_diag: "Recent Diagnosis",
        yield_est: "Yield Estimation",
        yield_sub: "Estimated harvest for your farm",
        yield_status: "Yield Status:",
        factors: "Influencing Factors",
        quick_actions: "Quick Actions",
        crop_adv: "Crop Advisory",
        soil_test: "Soil Testing",
        fert_adv: "Fertilizer Advisory",
        irrig_plan: "Irrigation Plan",
        weather_info: "Weather Info",
        mandi_rates: "Mandi Rates",
        adv_history: "Advisory History",
        settings: "Settings",
        help: "Help & Support"
    },
    mr: {
        brand_title: "अन्नदाता",
        brand_tagline: "योग्य सल्ला, उत्तम पीक",
        location_btn: "स्थान बदला",
        new_advice: "नवीन सल्ला मिळवा",
        farm_info: "शेताची माहिती",
        farm_size: "शेताचा आकार",
        soil_type: "मातीचा प्रकार",
        main_crop: "मुख्य पीक",
        last_update: "शेवटचे अपडेट",
        today_advice: "आजचा सल्ला",
        pest_detect: "रोग व कीड ओळखा",
        pest_sub: "पानांचा फोटो अपलोड करा व रोग ओळखा",
        upload_title: "फोटो अपलोड करा",
        upload_sub: "JPG, PNG (कमाल 5MB)",
        recent_diag: "अलीकडील तपासणी",
        yield_est: "उत्पादनाचा अंदाज",
        yield_sub: "तुमच्या शेतासाठी अंदाजित उत्पादन",
        yield_status: "उत्पादनाची स्थिती:",
        factors: "विचारात घेतलेले घटक",
        quick_actions: "द्रुत कृती",
        crop_adv: "पीक सल्ला",
        soil_test: "माती परीक्षण",
        fert_adv: "खत सल्ला",
        irrig_plan: "सिंचन नियोजन",
        weather_info: "हवामान माहिती",
        mandi_rates: "बाजार भाव",
        adv_history: "इतिहास",
        settings: "सेटिंग्ज",
        help: "मदत"
    }
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardSummary();
    setupDragAndDrop();
});

// Fetch Dashboard Summary
async function fetchDashboardSummary() {
    try {
        const response = await fetch(`${API_BASE}/api/dashboard-summary`);
        if (!response.ok) throw new Error("Network error");
        const data = await response.json();
        currentDashboardData = data;
        renderDashboard(data);
    } catch (err) {
        console.warn("Using offline / fallback rendering:", err);
    }
}

// Render Dashboard Data
function renderDashboard(data) {
    const { profile, mini_cards, weather, yield_data } = data;

    // 1. Profile & Farm Banner
    if (profile) {
        document.getElementById('current-location-text').innerText = profile.location || "इंदौर , मध्य प्रदेश";
        document.getElementById('profile-name').innerText = profile.farmer_name.split('(')[0].trim() || "किसान भाई";
        document.getElementById('val-farm-size').innerText = `${profile.farm_size_acres} एकड़`;
        document.getElementById('val-soil-type').innerText = profile.soil_type.split('(')[0].trim();
        document.getElementById('val-main-crop').innerText = profile.primary_crop;
        document.getElementById('val-last-update').innerText = profile.last_updated;
    }

    // 2. Mini Cards
    if (mini_cards && mini_cards.length >= 5) {
        document.getElementById('card-val-1').innerText = mini_cards[0].value;
        document.getElementById('card-sub-1').innerText = mini_cards[0].subtitle;

        document.getElementById('card-val-2').innerText = mini_cards[1].value;
        document.getElementById('card-sub-2').innerText = mini_cards[1].subtitle;

        document.getElementById('card-val-3').innerText = mini_cards[2].value;
        document.getElementById('card-sub-3').innerText = mini_cards[2].subtitle;

        document.getElementById('card-val-4').innerText = mini_cards[3].value;
        document.getElementById('card-sub-4').innerText = mini_cards[3].subtitle;

        document.getElementById('card-val-5').innerText = mini_cards[4].value;
        document.getElementById('card-sub-5').innerText = mini_cards[4].subtitle;
    }

    // 3. Yield Engine Card
    if (yield_data) {
        document.getElementById('val-yield-num').innerText = yield_data.estimated_yield_per_acre;
        document.getElementById('val-yield-status').innerText = yield_data.status_hi.split('(')[0].trim();
        if (yield_data.svg_polyline) {
            document.getElementById('yield-polyline').setAttribute('points', yield_data.svg_polyline);
        }
    }
}

// Drag & Drop Setup
function setupDragAndDrop() {
    const dropZone = document.getElementById('drop-zone');
    if (!dropZone) return;

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            uploadFileForDiagnosis(files[0]);
        }
    });
}

// Handle Image Upload
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        uploadFileForDiagnosis(file);
    }
}

// Upload and Diagnose Leaf Image
async function uploadFileForDiagnosis(file) {
    showToast("छवि का AI विश्लेषण किया जा रहा है...");
    
    // Preview local image immediately
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('disease-preview-img').src = e.target.result;
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('crop_hint', document.getElementById('val-main-crop').innerText);

    try {
        const response = await fetch(`${API_BASE}/api/detect-disease`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        currentDiseaseData = result;

        // Update UI
        document.getElementById('res-disease-name').innerText = result.disease_name_hi;
        document.getElementById('res-confidence').innerText = `${result.confidence_score}%`;
        document.getElementById('res-date').innerText = new Date().toLocaleDateString('hi-IN', { day: 'numeric', month: 'short', year: 'numeric' });

        showToast("रोग की सफल पहचान हुई!");
        speakText(result.voice_text_hi);
    } catch (err) {
        console.error("Diagnosis error:", err);
        showToast("सर्वर त्रुटि, ऑफलाइन परिणाम दिखाया जा रहा है");
    }
}

// Test Sample Disease Buttons
async function testSampleDisease(type) {
    showToast(`परीक्षण नमूना लोड हो रहा है: ${type}`);
    let cropHint = "Wheat";
    let sampleImg = "./assets/leaf.jpg";

    if (type === 'rice') {
        cropHint = "Rice";
    } else if (type === 'tomato') {
        cropHint = "Tomato";
    } else if (type === 'healthy') {
        cropHint = "Healthy";
    }

    const formData = new FormData();
    formData.append('crop_hint', cropHint);

    try {
        const response = await fetch(`${API_BASE}/api/detect-disease`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        currentDiseaseData = result;

        document.getElementById('res-disease-name').innerText = result.disease_name_hi;
        document.getElementById('res-confidence').innerText = `${result.confidence_score}%`;
        document.getElementById('res-date').innerText = new Date().toLocaleDateString('hi-IN', { day: 'numeric', month: 'short', year: 'numeric' });

        speakText(result.voice_text_hi);
        openDiseaseDetailModal();
    } catch (e) {
        console.error(e);
    }
}

// Open Disease Detail Modal
function openDiseaseDetailModal() {
    const data = currentDiseaseData;
    const body = document.getElementById('disease-modal-body');
    
    body.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; background:#fee2e2; padding:12px 16px; border-radius:10px;">
            <div>
                <h3 style="color:#b91c1c; font-size:18px; font-weight:800;">${data.disease_name_hi}</h3>
                <p style="font-size:12px; color:#7f1d1d;">${data.disease_name_en} | गंभीरता: ${data.severity}</p>
            </div>
            <span style="font-size:18px; font-weight:800; color:#b91c1c;">${data.confidence_score}% विश्वास</span>
        </div>

        <div style="margin-top:12px;">
            <h4 style="font-size:14px; font-weight:700; color:#1e293b;">लक्षण (Symptoms):</h4>
            <p style="font-size:13px; color:#475569; margin-top:4px;">${data.symptoms_hi}</p>
        </div>

        <div style="background:#e8f5e9; padding:12px; border-radius:10px; border:1px solid #c8e6c9; margin-top:8px;">
            <h4 style="font-size:14px; font-weight:800; color:#2e7d32; display:flex; align-items:center; gap:6px;">
                <span class="material-symbols-outlined" style="font-size:18px;">eco</span> जैविक / प्राकृतिक उपचार (Organic Remedies):
            </h4>
            <ul style="padding-left:20px; font-size:13px; color:#1b5e20; margin-top:6px; line-height:1.6;">
                ${data.organic_remedies_hi.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>

        <div style="background:#fff3e0; padding:12px; border-radius:10px; border:1px solid #ffe0b2; margin-top:8px;">
            <h4 style="font-size:14px; font-weight:800; color:#e65100; display:flex; align-items:center; gap:6px;">
                <span class="material-symbols-outlined" style="font-size:18px;">science</span> रासायनिक उपचार एवं मात्रा (Chemical Treatment):
            </h4>
            <ul style="padding-left:20px; font-size:13px; color:#bf360c; margin-top:6px; line-height:1.6;">
                ${data.chemical_remedies_hi.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>

        <div style="margin-top:8px;">
            <h4 style="font-size:13px; font-weight:700; color:#334155;">रोकथाम एवं बचाव (Prevention):</h4>
            <p style="font-size:12px; color:#64748b; margin-top:2px;">${data.prevention_hi}</p>
        </div>

        <button class="btn-tts" onclick="speakText('${data.voice_text_hi.replace(/'/g, "\\'")}')" style="margin-top:12px; align-self:flex-start;">
            <span class="material-symbols-outlined">volume_up</span> यह सलाह आवाज में सुनें
        </button>
    `;
    
    openModal('modal-disease-detail');
}

// Submit Crop Recommendation (AI ML Predict)
async function submitCropRecommendation() {
    const payload = {
        nitrogen: parseFloat(document.getElementById('input-n').value),
        phosphorus: parseFloat(document.getElementById('input-p').value),
        potassium: parseFloat(document.getElementById('input-k').value),
        ph: parseFloat(document.getElementById('input-ph').value),
        rainfall: parseFloat(document.getElementById('input-rain').value),
        temperature: parseFloat(document.getElementById('input-temp').value),
        humidity: 65.0
    };

    showToast("AI मॉडल गणना कर रहा है...");

    try {
        const response = await fetch(`${API_BASE}/api/recommend-crop`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        
        const container = document.getElementById('crop-recommendation-result');
        container.style.display = 'block';
        container.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="color:#1b5e20; font-size:18px; font-weight:800;">
                    अनुशंसित फसल: ${result.recommended_crop_hi} (${result.recommended_crop})
                </h3>
                <span style="background:#2e7d32; color:#fff; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:700;">
                    उपयुक्तता: ${result.suitability_percentage}%
                </span>
            </div>
            <p style="font-size:13px; color:#2e7d32; margin-top:6px; font-weight:600;">
                ऋतु: ${result.season_hi}
            </p>
            <p style="font-size:13px; color:#334155; margin-top:8px; line-height:1.4;">
                ${result.rationale_hi}
            </p>

            <h4 style="font-size:13px; font-weight:700; color:#1e293b; margin-top:10px;">वैकल्पिक फसलें (Alternative Choices):</h4>
            <div style="display:flex; gap:8px; margin-top:6px; flex-wrap:wrap;">
                ${result.alternatives.map(alt => `
                    <span style="background:#fff; border:1px solid #c8e6c9; padding:4px 10px; border-radius:14px; font-size:12px; font-weight:700; color:#2e7d32;">
                        ${alt.crop_hi} (${alt.suitability}%)
                    </span>
                `).join('')}
            </div>

            <button class="btn-tts" onclick="speakText('${result.rationale_hi.replace(/'/g, "\\'")}')" style="margin-top:10px;">
                <span class="material-symbols-outlined">volume_up</span> सलाह सुनें
            </button>
        `;

        speakText(`आपकी मिट्टी के लिए सबसे उपयुक्त फसल ${result.recommended_crop_hi} है जिसकी अनुकूलता ${result.suitability_percentage} प्रतिशत है।`);
    } catch (e) {
        console.error(e);
        showToast("फसल सिफारिश गणना में त्रुटि");
    }
}

// Calculate Fertilizer Schedule
async function calculateFertilizerSchedule() {
    const crop = document.getElementById('fert-crop-select').value;
    const farmSize = parseFloat(document.getElementById('fert-farm-size').value) || 2.5;

    showToast("खाद की गणना की जा रही है...");

    try {
        const response = await fetch(`${API_BASE}/api/fertilizer-plan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nitrogen: 42.0,
                phosphorus: 38.0,
                potassium: 45.0,
                ph: 6.8,
                farm_size_acres: farmSize,
                crop: crop,
                soil_type: "दोमट"
            })
        });
        const result = await response.json();
        
        const container = document.getElementById('fertilizer-calc-result');
        container.style.display = 'block';
        container.innerHTML = `
            <div style="background:#f1f8e9; padding:14px; border-radius:12px; border:1px solid #dcedc8; margin-top:14px;">
                <h3 style="color:#33691e; font-size:16px; font-weight:800;">
                    ${result.farm_size_acres} एकड़ ${result.crop_hi} हेतु कुल आवश्यक खाद:
                </h3>
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; margin-top:10px; text-align:center;">
                    <div style="background:#fff; padding:8px; border-radius:8px;">
                        <span style="font-size:11px; color:#64748b;">यूरिया</span>
                        <h4 style="color:#2e7d32; font-weight:800;">${result.fertilizer_requirements.urea_bags} बोरी</h4>
                        <span style="font-size:10px; color:#94a3b8;">(${result.fertilizer_requirements.urea_kg} kg)</span>
                    </div>
                    <div style="background:#fff; padding:8px; border-radius:8px;">
                        <span style="font-size:11px; color:#64748b;">DAP</span>
                        <h4 style="color:#e65100; font-weight:800;">${result.fertilizer_requirements.dap_bags} बोरी</h4>
                        <span style="font-size:10px; color:#94a3b8;">(${result.fertilizer_requirements.dap_kg} kg)</span>
                    </div>
                    <div style="background:#fff; padding:8px; border-radius:8px;">
                        <span style="font-size:11px; color:#64748b;">पोटाश (MOP)</span>
                        <h4 style="color:#0284c7; font-weight:800;">${result.fertilizer_requirements.mop_bags} बोरी</h4>
                        <span style="font-size:10px; color:#94a3b8;">(${result.fertilizer_requirements.mop_kg} kg)</span>
                    </div>
                </div>

                <div style="margin-top:12px; background:#fff; padding:10px; border-radius:8px; font-size:12px; color:#1b5e20;">
                    <strong>अनुमानित बचत:</strong> ${result.cost_analysis.savings_text_hi}
                </div>

                <h4 style="font-size:13px; font-weight:700; color:#1e293b; margin-top:12px;">खाद देने का सही समय (Application Schedule):</h4>
                <div style="margin-top:6px; font-size:12px; color:#475569; display:flex; flex-direction:column; gap:8px;">
                    ${result.schedule.map(s => `
                        <div style="background:#fff; padding:8px; border-radius:6px; border-left:3px solid #689f38;">
                            <strong style="color:#33691e;">${s.stage_hi}</strong>
                            <p style="margin-top:2px;">${s.items_hi.join(' • ')}</p>
                        </div>
                    `).join('')}
                </div>

                <button class="btn-tts" onclick="speakText('${result.voice_text_hi.replace(/'/g, "\\'")}')" style="margin-top:10px;">
                    <span class="material-symbols-outlined">volume_up</span> खाद सलाह सुनें
                </button>
            </div>
        `;

        speakText(result.voice_text_hi);
    } catch (e) {
        console.error(e);
        showToast("खाद गणना में त्रुटि");
    }
}

// Fetch Mandi Prices
async function fetchMandiPrices(crop = "Wheat") {
    try {
        const response = await fetch(`${API_BASE}/api/mandi-prices?crop=${crop}`);
        const data = await response.json();
        
        const container = document.getElementById('mandi-data-container');
        container.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; background:#e8f5e9; padding:12px 16px; border-radius:10px;">
                <div>
                    <h3 style="color:#2e7d32; font-size:18px; font-weight:800;">${data.crop_hi} औसत भाव: ₹${data.modal_price_inr} / क्विंटल</h3>
                    <p style="font-size:12px; color:#1b5e20;">सरकारी MSP: ₹${data.msp_inr || 'लागू नहीं'} | बाजार रुझान: ${data.trend_pct} (${data.trend_label_hi})</p>
                </div>
            </div>

            <h4 style="font-size:14px; font-weight:700; color:#1e293b; margin-top:14px;">आसपास की मंडियों के भाव:</h4>
            <div style="display:flex; flex-direction:column; gap:8px; margin-top:8px;">
                ${data.mandis.map(m => `
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:10px 14px; border-radius:8px; border:1px solid #e2e8f0;">
                        <div>
                            <strong style="font-size:13px; color:#1e293b;">${m.mandi}</strong>
                            <p style="font-size:11px; color:#64748b;">दूरी: ${m.distance_km} किमी | आवक: ${m.arrival_tonnes} टन</p>
                        </div>
                        <span style="font-size:16px; font-weight:800; color:#2e7d32;">₹${m.modal_price}</span>
                    </div>
                `).join('')}
            </div>

            <button class="btn-tts" onclick="speakText('${data.voice_text_hi.replace(/'/g, "\\'")}')" style="margin-top:12px;">
                <span class="material-symbols-outlined">volume_up</span> भाव सुनें
            </button>
        `;
    } catch (e) {
        console.error(e);
    }
}

// Show Advice Detail Modal
function showAdviceDetail(category) {
    const titles = {
        crop: "फसल सलाह (Crop Guidance)",
        fertilizer: "खाद एवं पोषक तत्व सलाह (Fertilizer Plan)",
        irrigation: "सिंचाई प्रबंधन सलाह (Irrigation Schedule)",
        pest: "कीट एवं रोग सुरक्षा (Pest & Disease Advisory)",
        weather: "मौसम एवं कृषि कार्य सलाह (Agromet Advisory)"
    };

    const details = {
        crop: "आपकी 2.5 एकड़ दोमट मिट्टी में गेहूं (HD-3086/DBW-187) की फसल 92% उपयुक्त है। 100 किग्रा/एकड़ बीज की दर से बुवाई करें और कतार से कतार की दूरी 20 सेमी रखें।",
        fertilizer: "मिट्टी में नाइट्रोजन की कमी है। 7 दिनों में प्रति एकड़ 30 किग्रा यूरिया की टॉप ड्रेसिंग करें। पोटाश का पर्णीय स्प्रे (00:00:50) दानों के वजन के लिए लाभप्रद रहेगा।",
        irrigation: "वर्तमान मिट्टी नमी 32% है। अगले 2 दिनों में 5 सेमी हल्की सिंचाई करें। मौसम पूर्वानुमान में 3 दिन बाद बारिश संभावित है, अतः अत्यधिक पानी न भरें।",
        pest: "हवा में आर्द्रता अधिक होने से गेहूं की पत्ती पर पीला/भूरा रतुआ (Rust) का खतरा है। रोकथाम हेतु प्रोपिकोनाजोल 1 मिली/लीटर अथवा नीम तेल 5 मिली/लीटर का सुरक्षात्मक छिड़काव करें।",
        weather: "अगले 3 दिनों में 18 मिमी मध्यम बारिश की संभावना है। कीटनाशक छिड़काव स्थगित रखें और खेत में जल निकासी नाली साफ रखें।"
    };

    document.getElementById('advice-modal-title').innerText = titles[category] || "सलाह विवरण";
    document.getElementById('advice-modal-body').innerHTML = `
        <p style="font-size:14px; color:#334155; line-height:1.6;">${details[category] || ""}</p>
        <button class="btn-tts" onclick="speakText('${(details[category] || "").replace(/'/g, "\\'")}')" style="margin-top:14px;">
            <span class="material-symbols-outlined">volume_up</span> यह सलाह सुनें
        </button>
    `;
    openModal('modal-advice-detail');
}

// Speak All Today's Advice (Voice Assistant)
function speakAllTodayAdvice() {
    const text = "आज की कृषि सलाह: गेहूं की फसल के लिए मौसम उपयुक्त है। मिट्टी में नाइट्रोजन की कमी है, 7 दिनों में यूरिया दें। 2 दिनों में हल्की सिंचाई करें। पत्तियों पर रतुआ रोग की नियमित जांच करें, और आने वाले दिनों में 18 मिमी बारिश की संभावना को ध्यान में रखें।";
    speakText(text);
}

function speakYieldAdvice() {
    const text = "आपके 2.5 एकड़ खेत के लिए अनुमानित उपज 34.6 क्विंटल प्रति एकड़ है, जो कि अच्छी स्थिति में है।";
    speakText(text);
}

// Text-to-Speech Engine (Web Speech API)
function speakText(text) {
    if (!('speechSynthesis' in window)) {
        showToast("आपके ब्राउज़र में आवाज की सुविधा उपलब्ध नहीं है");
        return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = currentLanguage === 'en' ? 'en-IN' : 'hi-IN';
    utterance.rate = 0.92;
    utterance.pitch = 1.0;
    
    showToast("आवाज चल रही है...");
    window.speechSynthesis.speak(utterance);
}

// Modal Helpers
function openModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('active');
}

function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
}

function openCropModal() { openModal('modal-crop'); }
function openSoilModal() { openModal('modal-crop'); }
function openFertilizerModal() { openModal('modal-fertilizer'); }
function openIrrigationModal() { showAdviceDetail('irrigation'); }
function openWeatherModal() { showAdviceDetail('weather'); }
function openYieldModal() { speakYieldAdvice(); }
function openMandiModal() { fetchMandiPrices('Wheat'); openModal('modal-mandi'); }
function openLocationModal() { openModal('modal-location'); }
function openProfileModal() { openModal('modal-profile'); }

async function openHistoryModal() {
    openModal('modal-history');
    try {
        const response = await fetch(`${API_BASE}/api/history`);
        const list = await response.json();
        const container = document.getElementById('history-container');
        container.innerHTML = list.map(item => `
            <div style="background:#f8fafc; padding:12px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:12px; color:#64748b; font-weight:600;">
                    <span>${item.type_hi}</span>
                    <span>${item.date}</span>
                </div>
                <h4 style="font-size:14px; color:#1e293b; margin-top:4px;">${item.result_hi}</h4>
                <p style="font-size:12px; color:#2e7d32; margin-top:2px;">कार्रवाई: ${item.action_taken_hi}</p>
            </div>
        `).join('');
    } catch (e) {
        console.error(e);
    }
}

function openHelpModal() {
    speakText("अन्नदाता किसान सहायता केंद्र। किसी भी समस्या के लिए 9520412093 पर कॉल करें।");
    showToast("किसान हेल्पलाइन: +91 9520412093");
}

function updateLocation() {
    const loc = document.getElementById('location-picker').value;
    document.getElementById('current-location-text').innerText = loc;
    closeModal('modal-location');
    showToast(`स्थान बदला गया: ${loc}`);
    fetchDashboardSummary();
}

async function saveFarmProfile() {
    const name = document.getElementById('prof-name-input').value;
    const size = parseFloat(document.getElementById('prof-size-input').value);
    const soil = document.getElementById('prof-soil-input').value;
    const crop = document.getElementById('prof-crop-input').value;

    try {
        await fetch(`${API_BASE}/api/farm-profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                farmer_name: name,
                farm_size_acres: size,
                soil_type: soil,
                primary_crop: crop
            })
        });
        closeModal('modal-profile');
        showToast("प्रोफाइल सफलतापूर्वक सुरक्षित की गई");
        fetchDashboardSummary();
    } catch (e) {
        console.error(e);
    }
}

function toggleNotifications() {
    speakText("आपके पास 2 नए कृषि अलर्ट हैं: 3 दिन बाद वर्षा की संभावना, और गेहूं में खाद देने का समय।");
    showToast("🔔 2 नए कृषि अलर्ट उपलब्ध हैं");
}

function switchTab(tab) {
    document.querySelectorAll('#sidebar-links a').forEach(a => a.classList.remove('active'));
    event.currentTarget.classList.add('active');
}

// Language Switcher
function changeLanguage(lang) {
    currentLanguage = lang;
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['hi'];
    
    document.getElementById('brand-title').innerText = dict.brand_title;
    document.getElementById('brand-tagline').innerText = dict.brand_tagline;
    document.getElementById('btn-change-location').innerText = dict.location_btn;
    document.getElementById('farm-info-title').innerText = dict.farm_info;
    document.getElementById('label-farm-size').innerText = dict.farm_size;
    document.getElementById('label-soil-type').innerText = dict.soil_type;
    document.getElementById('label-main-crop').innerText = dict.main_crop;
    document.getElementById('label-last-update').innerText = dict.last_update;
    document.getElementById('heading-today-advice').innerText = dict.today_advice;
    document.getElementById('heading-disease-card').innerText = dict.pest_detect;
    document.getElementById('sub-disease-card').innerText = dict.pest_sub;
    document.getElementById('text-upload-title').innerText = dict.upload_title;
    document.getElementById('text-upload-sub').innerText = dict.upload_sub;
    document.getElementById('heading-recent-diag').innerText = dict.recent_diag;
    document.getElementById('heading-yield-card').innerText = dict.yield_est;
    document.getElementById('sub-yield-card').innerText = dict.yield_sub;
    document.getElementById('heading-factors').innerText = dict.factors;
    document.getElementById('heading-quick-actions').innerText = dict.quick_actions;

    showToast(lang === 'en' ? "Language changed to English" : (lang === 'mr' ? "भाषा मराठीत बदलली" : "भाषा हिंदी में बदली गई"));
}

// Toast notification helper
function showToast(msg) {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toast-msg');
    toastMsg.innerText = msg;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
