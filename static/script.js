
console.log("FutureProof AI Engine Loaded");

// Global chart instances to prevent collision
let charts = {
    radar: null,
    bar: null,
    pie: null,
    line: null
};

document.getElementById('analysis-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const submitBtn = document.querySelector('.cta-button');
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.innerHTML = 'Crunching ML Models...';
    submitBtn.disabled = true;

    const gpaValue = document.getElementById('gpa').value;

    if (parseFloat(gpaValue) === 0 || gpaValue === "") {
        Swal.fire({
            icon: 'warning',
            title: 'Incomplete Profile',
            text: 'Please fill in your CGPA. It cannot be zero.',
            background: '#1e1e2d',
            color: '#fff',
            confirmButtonColor: '#6366f1'
        });
        submitBtn.innerHTML = originalBtnText;
        submitBtn.disabled = false;
        return;
    }

    const formData = {
        name: document.getElementById('name').value,
        gpa: gpaValue,
        projects: document.getElementById('projects').value,
        internships: document.getElementById('internships').value,
        certifications: document.getElementById('certifications').value,
        skills: document.getElementById('skills').value,
        aptitude: document.getElementById('aptitude').value,
        soft_skills: document.getElementById('soft_skills').value,
        tech_skills: document.getElementById('tech_skills').value,

        // New Personalization Inputs
        pace: document.getElementById('pace').value,
        daily_time: document.getElementById('daily_time').value
    };

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.status === 'success') {
            displayResults(data);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Analysis Failed',
                text: data.message,
                background: '#1e1e2d',
                color: '#fff',
                confirmButtonColor: '#6366f1'
            });
        }

    } catch (error) {
        console.error('API Connection Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Connection Lost',
            text: 'Could not reach the AI server. Please ensure the backend is running.',
            background: '#1e1e2d',
            color: '#fff',
            confirmButtonColor: '#6366f1'
        });
    } finally {
        submitBtn.innerHTML = originalBtnText;
        submitBtn.disabled = false;
    }
});

function displayResults(data) {
    const inputSection = document.getElementById('input-section');
    const resultsSection = document.getElementById('results-section');

    inputSection.style.opacity = '0';
    inputSection.style.transform = 'translateY(-20px)';

    setTimeout(() => {
        inputSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        document.getElementById('student-greeting').textContent = `Tailored career architecture for ${data.name}`;
        document.getElementById('res-career').textContent = data.recommended_career;
        document.getElementById('res-level').textContent = data.predicted_level;
        document.getElementById('res-prob').textContent = data.hiring_probability + '%';
        
        // Dynamic color for hireability score
        const probVal = parseFloat(data.hiring_probability);
        const probElem = document.getElementById('res-prob');
        if (probVal >= 70) {
            probElem.style.color = 'var(--success)';
        } else if (probVal >= 40) {
            probElem.style.color = 'var(--accent)';
        } else {
            probElem.style.color = '#ff4d4d'; // Red for low probability
        }

        // Render multiple career suggestions
        const suggestionsContainer = document.getElementById('career-suggestions-list');
        const countainerBox = document.getElementById('recommendation-list');
        if (data.all_recommendations && data.all_recommendations.length > 0) {
            suggestionsContainer.innerHTML = '';
            data.all_recommendations.forEach(rec => {
                const item = document.createElement('div');
                item.style.display = 'flex';
                item.style.justifyContent = 'space-between';
                item.style.fontSize = '0.85rem';
                item.style.marginBottom = '5px';
                item.innerHTML = `
                    <span>${rec.career}</span>
                    <span style="color: var(--accent); font-weight: bold;">${(rec.probability * 100).toFixed(0)}%</span>
                `;
                suggestionsContainer.appendChild(item);
            });
            countainerBox.style.display = 'block';
        } else {
            countainerBox.style.display = 'none';
        }

        const roadmap = document.getElementById('roadmap-container');
        roadmap.innerHTML = '';

        const gaps = data.gaps || [];

        if (gaps.length === 0) {
            roadmap.innerHTML = '<div style="text-align:center; padding: 40px;"><h4>🎯 High Alignment Detected</h4><p>Your current skill profile perfectly matches the market requirements for this role.</p></div>';
        } else {
            gaps.forEach((gap, index) => {
                const card = document.createElement('div');
                card.className = 'gap-card';
                card.style.animation = `fadeIn 0.6s ease-out forwards ${index * 0.1}s`;

                // Generate MULTI-LEVEL ROADMAP HTML
                const roadmapLevels = gap.Roadmap || [];
                const roadmapHTML = roadmapLevels.length > 0 ? `
                    <div class="roadmap-section" style="margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;">
                        <h5 style="margin-bottom:10px; color: var(--text-secondary);">Path to Mastery</h5>
                        <div class="roadmap-levels">
                            ${roadmapLevels.map(level => `
                                <div class="level-card ${level.status.toLowerCase()}" style="background: rgba(255,255,255,0.03); margin-bottom: 10px; border-radius: 8px; border-left: 3px solid ${level.status === 'Completed' ? '#10b981' : '#f59e0b'};">
                                    <div class="level-header" style="padding: 12px; cursor: pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <strong style="color: ${level.status === 'Completed' ? '#10b981' : 'white'};">${level.level}</strong>
                                            <span style="font-size: 0.8rem; opacity: 0.7;">${level.duration}</span>
                                        </div>
                                    </div>
                                    <div class="level-details" style="display: none; padding: 0 12px 12px 12px; border-top: 1px solid rgba(255,255,255,0.05);">
                                        <div style="margin-top: 10px;">
                                            <div style="font-size: 0.8rem; color: var(--accent); margin-bottom: 4px;">🎯 Concepts</div>
                                            <div style="font-size: 0.85rem;">${level.details.concepts ? level.details.concepts.join(' • ') : 'Fundamentals'}</div>
                                        </div>
                                        <div style="margin-top: 10px;">
                                            <div style="font-size: 0.8rem; color: var(--accent); margin-bottom: 4px;">🛠 Tools</div>
                                            <div style="font-size: 0.85rem;">${level.details.tools ? level.details.tools.join(', ') : 'Basic Tools'}</div>
                                        </div>
                                        <div style="margin-top: 10px;">
                                            <div style="font-size: 0.8rem; color: var(--accent); margin-bottom: 4px;">🚀 Project</div>
                                            <div style="font-size: 0.85rem; background: rgba(16, 185, 129, 0.1); padding: 5px; border-radius: 4px;">${level.details.project || 'Practice Project'}</div>
                                        </div>
                                         <div style="margin-top: 10px;">
                                            <div style="font-size: 0.8rem; color: var(--accent); margin-bottom: 4px;">📚 Resources</div>
                                            <div style="font-size: 0.85rem;">
                                                ${level.details.resources && level.details.resources.free ? level.details.resources.free.map(r => `<a href="#" style="color: #60a5fa; text-decoration: none; margin-right: 10px;">${r}</a>`).join('') : ''}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : '';

                card.innerHTML = `
                    <div class="gap-header">
                        <div class="gap-title-group">
                            <h4>${gap.Skill}</h4>
                            <div class="gap-subtitle">
                                <span class="badge-sm">${gap.Category}</span>
                                <span>${gap.Current_Level} → ${gap.Target_Level}</span>
                            </div>
                        </div>
                        <div class="duration-pill">
                            ${gap.Duration}
                        </div>
                    </div>
                    
                    <div class="resource-grid">
                        <a href="${gap.Resources.Premium}" target="_blank" class="res-btn premium">Elite Course</a>
                        <a href="${gap.Resources.Free}" target="_blank" class="res-btn">Learning Guide</a>
                        <a href="${gap.Resources.Practice}" target="_blank" class="res-btn">Hands-on Lab</a>
                    </div>
                    
                    ${roadmapHTML}
                `;
                roadmap.appendChild(card);
            });
        }

        // Render Government Jobs (NEW)
        const govJobs = data.government_jobs || [];
        const jobsContainer = document.getElementById('government-jobs-container');
        jobsContainer.innerHTML = '';

        if (govJobs.length === 0) {
            jobsContainer.innerHTML = '<div style="text-align:center; padding: 40px;"><h4>No Matching Jobs</h4><p>Build more skills to unlock government opportunities!</p></div>';
        } else {
            govJobs.forEach((job, index) => {
                const jobCard = document.createElement('div');
                jobCard.className = 'gap-card';
                jobCard.style.animation = `fadeIn 0.6s ease-out forwards ${index * 0.1}s`;

                // Eligibility badge color
                const eligibilityColor = job.eligibility_status === 'Eligible' ? '#10b981' :
                    job.eligibility_status === 'Partial' ? '#f59e0b' : '#ef4444';

                jobCard.innerHTML = `
                    <div class="gap-icon">🏛️</div>
                    <div class="gap-info">
                        <h4>${job.job_name}</h4>
                        <p style="opacity: 0.8; font-size: 0.85rem;">${job.conducting_body}</p>
                        <div style="margin-top: 8px;">
                            <span style="background: ${eligibilityColor}20; color: ${eligibilityColor}; padding: 4px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">${job.eligibility_status}</span>
                        </div>
                    </div>
                    <div class="gap-meta" style="grid-column: 1 / -1;">
                        <p style="font-size: 0.85rem; margin: 10px 0;"><strong>Why Matched:</strong> ${job.matched_skills.join(', ')}</p>
                        ${job.skill_gaps.length > 0 ? `<p style="font-size: 0.85rem; opacity: 0.7;"><strong>Skill Gaps:</strong> ${job.skill_gaps.join(', ')}</p>` : ''}
                        <p style="font-size: 0.85rem; opacity: 0.7;"><strong>Age:</strong> ${job.age_limit} | <strong>Education:</strong> ${job.education}</p>
                        <p style="font-size: 0.85rem; margin-top: 8px;"><strong>Preparation Focus:</strong> ${job.preparation_focus.join(', ')}</p>
                    </div>
                `;
                jobsContainer.appendChild(jobCard);
            });
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });

        const skillStats = data.skill_stats || {};
        renderAllCharts(skillStats, gaps);
    }, 400);
}

function renderAllCharts(stats, gaps) {
    const labels = Object.keys(stats);
    const scores = Object.values(stats);

    // 1. Radar Chart (Overall Profile)
    renderRadar(labels, scores);

    // 2. Bar Chart (Strength vs Weakness)
    renderBar(labels, scores);

    // 3. Pie Chart (Gap Distribution)
    renderPie(stats, gaps);

    // 4. Line Chart (Improvement Roadmap)
    renderLine(labels, scores);
}

function renderRadar(labels, scores) {
    if (charts.radar) charts.radar.destroy();
    const ctx = document.getElementById('skillRadarChart').getContext('2d');
    charts.radar = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Current Proficiency',
                data: scores,
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: '#818cf8',
                borderWidth: 2
            }, {
                label: 'Market High',
                data: labels.map(() => 9),
                borderColor: 'rgba(217, 70, 239, 0.4)',
                borderDash: [5, 5],
                pointRadius: 0
            }]
        },
        options: getChartOptions('radar')
    });
}

function renderBar(labels, scores) {
    if (charts.bar) charts.bar.destroy();
    const ctx = document.getElementById('skillBarChart').getContext('2d');

    // Background colors based on proficiency
    const backgroundColors = scores.map(s => s >= 7 ? 'rgba(16, 185, 129, 0.6)' : 'rgba(239, 68, 68, 0.6)');
    const borderColors = scores.map(s => s >= 7 ? '#10b981' : '#ef4444');

    charts.bar = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Skill Score',
                data: scores,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: getChartOptions('bar')
    });
}

function renderPie(stats, gaps) {
    if (charts.pie) charts.pie.destroy();
    const ctx = document.getElementById('skillPieChart').getContext('2d');

    const strong = Object.values(stats).filter(s => s >= 7).length;
    const weak = Object.values(stats).filter(s => s > 0 && s < 7).length;
    const missing = Object.values(stats).filter(s => s === 0).length;

    charts.pie = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Strong (7-10)', 'Weak (1-6)', 'Gaps (0)'],
            datasets: [{
                data: [strong, weak, missing],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                borderWidth: 0,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#f8fafc', font: { family: 'Outfit' } } }
            }
        }
    });
}

// Toggle study plan visibility
function toggleStudyPlan(index) {
    const planContent = document.getElementById(`study-plan-${index}`);
    if (planContent.style.display === 'none') {
        planContent.style.display = 'block';
    } else {
        planContent.style.display = 'none';
    }
}

function renderLine(labels, scores) {
    if (charts.line) charts.line.destroy();
    const ctx = document.getElementById('skillLineChart').getContext('2d');

    // Projection: Current -> +2 months -> +4 months
    const datasets = [{
        label: 'Current Status',
        data: scores,
        borderColor: '#818cf8',
        tension: 0.4,
        fill: false
    }, {
        label: '2 Month Projection',
        data: scores.map(s => Math.min(10, s + 1.5)),
        borderColor: 'rgba(99, 102, 241, 0.3)',
        borderDash: [5, 5],
        tension: 0.4,
        fill: false
    }, {
        label: 'Expert Goal',
        data: labels.map(() => 9.5),
        borderColor: '#d946ef',
        borderWidth: 1,
        pointRadius: 0,
        fill: false
    }];

    charts.line = new Chart(ctx, {
        type: 'line',
        data: { labels: labels, datasets: datasets },
        options: getChartOptions('line')
    });
}

function getChartOptions(type) {
    const common = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#f8fafc', font: { family: 'Outfit', size: 12 } } }
        }
    };

    if (type === 'radar') {
        return {
            ...common,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: { color: '#94a3b8', font: { family: 'Outfit' } },
                    suggestedMin: 0,
                    suggestedMax: 10,
                    ticks: { display: false }
                }
            }
        };
    }

    const cartesian = {
        ...common,
        scales: {
            y: {
                beginAtZero: true,
                max: 10,
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#94a3b8' }
            },
            x: {
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            }
        }
    };

    return cartesian;
}
