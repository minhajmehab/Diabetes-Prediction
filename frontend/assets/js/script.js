// Global variables
let accessToken = '';

// DOM Elements
const loginForm = document.getElementById('loginForm');
const uploadForm = document.getElementById('uploadForm');
const logoutBtn = document.getElementById('logoutBtn');
const extractedDataCard = document.getElementById('extractedDataCard');
const predictionCard = document.getElementById('predictionCard');
const modelBtns = document.querySelectorAll('.model-btn');
const predictionResult = document.getElementById('predictionResult');

// Event Listeners
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}

if (uploadForm) {
    uploadForm.addEventListener('submit', handleUpload);
}

if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.model-btn').forEach(btn => {
        btn.addEventListener('click', handleModelSelection);
    });
});

// Check if user is already logged in
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('accessToken');
    console.log('[Redirect Check] Token:', token, 'Path:', window.location.pathname);
    if (token && window.location.pathname.endsWith('index.html')) {
        console.log('[Redirect] To dashboard.html');
        window.location.href = 'dashboard.html';
    } else if (!token && !window.location.pathname.endsWith('index.html')) {
        console.log('[Redirect] To index.html');
        window.location.href = 'index.html';
    }
});

// Functions
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        accessToken = data.access_token;
        localStorage.setItem('accessToken', accessToken);
        window.location.href = 'dashboard.html';
    } catch (error) {
        alert('Login failed. Please check your credentials.');
        console.error(error);
    }
}

async function handleUpload(e) {
    e.preventDefault();

    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a PDF file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/classical/extract-patient-data', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to extract data');
        }

        const data = await response.json();
        displayExtractedData(data.extracted_data);
        extractedDataCard.style.display = 'block';
        predictionCard.style.display = 'block';
    } catch (error) {
        alert('Error extracting data from PDF');
        console.error(error);
    }
}

function displayExtractedData(data) {
    const tableBody = document.querySelector('#extractedDataTable tbody');
    tableBody.innerHTML = '';

    for (const [key, value] of Object.entries(data)) {
        const row = document.createElement('tr');

        const keyCell = document.createElement('td');
        keyCell.textContent = key;
        keyCell.style.fontWeight = 'bold';

        const valueCell = document.createElement('td');
        valueCell.textContent = value;

        row.appendChild(keyCell);
        row.appendChild(valueCell);
        tableBody.appendChild(row);
    }
}

async function handleModelSelection(e) {
    e.preventDefault();
    console.log('[ModelSelection] Started');
    console.log('[ModelSelection] Token before fetch:', localStorage.getItem('accessToken'));

    const model = e.target.dataset.model;

    if (model === 'transformer' || model === 'neural') {
        predictionResult.innerHTML = `
            <div class="alert alert-info">
                ${model === 'transformer' ? 'Transformer' : 'Neural Network'} model is not implemented yet. 
                Please use the Classical model for predictions.
            </div>
        `;
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/${model}/predict`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                'Content-Type': 'application/json'
            }
        });
        console.log('[ModelSelection] Response status:', response.status);

        if (response.status === 401) {
            alert('Session expired. Please log in again.');
            localStorage.removeItem('accessToken');
            window.location.href = 'index.html';
            return;
        }

        if (!response.ok) {
            const errText = await response.text();
            throw new Error('Prediction failed: ' + errText);
        }

        const data = await response.json();
        console.log('[ModelSelection] Prediction data:', data);

        let resultHtml = '';
        if (model === 'classical') {
            const prediction = data.prediction === 1 ? 'Positive' : 'Negative';
            const alertClass = data.prediction === 1 ? 'danger' : 'success';

            let factorsHtml = '';
            if (data.prediction === 1 && data.top_factors && Object.keys(data.top_factors).length > 0) {
                factorsHtml = `
                    <p><strong>Top factors influencing this prediction:</strong></p>
                    <ul>
                        ${Object.entries(data.top_factors).map(([key, value]) => `<li>${key}: ${value}</li>`).join('')}
                    </ul>
                `;
            }

            resultHtml = `
                <div class="alert alert-${alertClass}">
                    <h4>Prediction Result: ${prediction}</h4>
                    <p class="mb-0">The model predicts that the patient is <strong>${prediction.toLowerCase()}</strong> for diabetes.</p>
                    ${factorsHtml}
                    <p><strong>Prediction Score:</strong> ${data.score}</p>
                </div>
            `;
        }

        predictionResult.innerHTML = resultHtml;
        // Add after predictionResult is updated
        showHistoryButton();
        console.log('[ModelSelection] Finished. Token after fetch:', localStorage.getItem('accessToken'));
    } catch (error) {
        predictionResult.innerHTML = `
            <div class="alert alert-danger">
                Error making prediction: ${error.message}
            </div>
        `;
        console.error('[ModelSelection] Error:', error);
    }
}

function showHistoryButton() {
    const historySection = document.getElementById('historySection');
    if (historySection) {
        historySection.style.display = 'block';
    }
}

if (document.getElementById('viewHistoryBtn')) {
    document.getElementById('viewHistoryBtn').addEventListener('click', function() {
        window.location.href = 'history.html';
    });
}

async function fetchAndShowHistory() {
    const token = localStorage.getItem('accessToken');
    try {
        const response = await fetch('http://localhost:8000/classical/get-patient-data', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Failed to fetch history');
        const data = await response.json();
        renderHistoryTable(data.extracted_data);
        renderHistoryGraphs(data.extracted_data);
    } catch (err) {
        alert('Could not fetch history');
        console.error(err);
    }
}

function renderHistoryTable(records) {
    const container = document.getElementById('historyTableContainer');
    if (!records.length) {
        container.innerHTML = '<div class="alert alert-info">No history found.</div>';
        return;
    }
    // Specify the desired column order here:
    const headers = [
        'date',
        'glucose',
        'bmi',
        'blood_pressure',
        'insulin',
        'skin_thickness',
        'diabetes_pedigree_function',
        'pregnancies',
        'score',
        'prediction_class'
    ];
    let html = '<div class="table-responsive"><table class="table table-bordered"><thead><tr>';
    headers.forEach(h => html += `<th>${h.replace(/_/g, ' ')}</th>`);
    html += '</tr></thead><tbody>';
    records.forEach(rec => {
        html += '<tr>';
        headers.forEach(h => html += `<td>${rec[h]}</td>`);
        html += '</tr>';
    });
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.endsWith('history.html')) {
        fetchAndShowHistory();
    }
});

function renderHistoryGraphs(records) {
    const exclude = ['top_factors', 'prediction_class', 'username', 'date', 'age'];
    const features = Object.keys(records[0]).filter(k => !exclude.includes(k));
    const dates = records.map(r => r.date);

    let html = '';
    features.forEach((f) => {
        const values = records.map(r => r[f]);
        const canvasId = `graph_${f}`;
        html += `
            <div class="mb-4">
                <div class="card p-2">
                    <h6 class="text-center">${f.replace(/_/g, ' ')}</h6>
                    <canvas id="${canvasId}" height="200" width="250"></canvas>
                </div>
            </div>
        `;
        setTimeout(() => drawLineChart(canvasId, dates, values, f), 0);
    });
    document.getElementById('historyGraphs').innerHTML = html;
}

// Draw chart using Chart.js
function drawLineChart(canvasId, labels, data, label) {
    if (!window.Chart) return;
    const ctx = document.getElementById(canvasId).getContext('2d');
    // Set y-axis min/max for score
    const yAxisOptions = label === 'score'
        ? { beginAtZero: true, min: 0, max: 1 }
        : { beginAtZero: true };
    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: label.replace(/_/g, ' '),
                data,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13,110,253,0.1)',
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { 
                x: { title: { display: true, text: 'Date' } }, 
                y: yAxisOptions
            }
        }
    });
}

function handleLogout() {
    localStorage.removeItem('accessToken');
    window.location.href = 'index.html';
}
