// ==========================================
// Adaptive SOC Dashboard
// dashboard.js
// ==========================================

let riskChart = null;

// ==========================================
// DOM HELPERS
// ==========================================

const el = (id) => document.getElementById(id);

function setText(id, value) {
    const element = el(id);
    if (element) element.textContent = value;
}

// ==========================================
// ALERT BANNER
// ==========================================

function updateAlertPanel(riskScore) {

    const panel = el("alertPanel");

    if (!panel) return;

    if (riskScore <= 30) {

        panel.className =
            "alert alert-success";

        panel.innerHTML =
            "🟢 System Operating Normally";

    }

    else if (riskScore <= 60) {

        panel.className =
            "alert alert-warning";

        panel.innerHTML =
            "🟡 Behavioral Anomaly Detected";

    }

    else {

        panel.className =
            "alert alert-danger";

        panel.innerHTML =
            "🔴 Critical Risk Detected";

    }
}

// ==========================================
// RISK BADGE
// ==========================================

function updateRiskBadge(score) {

    const badge =
        el("riskBadge");

    if (!badge) return;

    if (score <= 30) {

        badge.className =
            "badge bg-success fs-6";

        badge.innerHTML =
            "LOW";

    }

    else if (score <= 60) {

        badge.className =
            "badge bg-warning text-dark fs-6";

        badge.innerHTML =
            "MEDIUM";

    }

    else {

        badge.className =
            "badge bg-danger fs-6";

        badge.innerHTML =
            "HIGH";

    }
}

// ==========================================
// LIVE DATA
// ==========================================

async function loadLive() {

    try {

        const res =
            await fetch("/api/live");

        const data =
            await res.json();

        if (!data.id) return;

        setText(
            "temperature",
            `${data.temperature} °C`
        );

        setText(
            "humidity",
            `${data.humidity} %`
        );

        setText(
            "movement",
            data.movement_score
        );

        setText(
            "riskScore",
            data.risk_score
        );

        setText(
            "deviceId",
            data.device_id
        );

        setText(
            "presence",
            data.presence_status
        );

        setText(
            "touch",
            data.touch_activity
        );

        updateRiskBadge(
            data.risk_score
        );

        updateAlertPanel(
            data.risk_score
        );

    }

    catch (err) {

        console.error(
            "Live API Error:",
            err
        );

    }
}

// ==========================================
// EVENTS
// ==========================================

async function loadEvents() {

    try {

        const res =
            await fetch(
                "/api/events"
            );

        const events =
            await res.json();

        let html = "";

        events.forEach(event => {

            let severityClass =
                "table-info";

            if (
                event.severity ===
                "Critical"
            )
                severityClass =
                    "table-danger";

            else if (
                event.severity ===
                "Warning"
            )
                severityClass =
                    "table-warning";

            html += `
                <tr class="${severityClass}">
                    <td>${event.timestamp}</td>
                    <td>${event.event_type}</td>
                    <td>${event.severity}</td>
                    <td>${event.description}</td>
                </tr>
            `;
        });

        const table =
            el("eventsBody");

        if (table)
            table.innerHTML =
                html;

    }

    catch (err) {

        console.error(
            "Event API Error:",
            err
        );

    }
}

// ==========================================
// RISK TREND GRAPH
// ==========================================

async function loadRiskHistory() {

    try {

        const res =
            await fetch(
                "/api/risk-history"
            );

        const data =
            await res.json();

        const labels =
            data.map(
                item =>
                    item.timestamp
            ).reverse();

        const scores =
            data.map(
                item =>
                    item.risk_score
            ).reverse();

        const ctx =
            document
                .getElementById(
                    "riskChart"
                )
                .getContext("2d");

        if (riskChart)
            riskChart.destroy();

        riskChart =
            new Chart(ctx, {

                type: "line",

                data: {

                    labels:

                        labels,

                    datasets: [

                        {

                            label:
                                "Risk Score",

                            data:
                                scores,

                            borderWidth:
                                3,

                            fill:
                                true,

                            tension:
                                0.4

                        }

                    ]

                },

                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false,

                    plugins: {

                        legend: {

                            labels: {

                                color:
                                    "white"

                            }

                        }

                    },

                    scales: {

                        x: {

                            ticks: {

                                color:
                                    "white"

                            }

                        },

                        y: {

                            min: 0,

                            max: 100,

                            ticks: {

                                color:
                                    "white"

                            }

                        }

                    }

                }

            });

    }

    catch (err) {

        console.error(
            "Risk Graph Error:",
            err
        );

    }
}

// ==========================================
// DASHBOARD STATS
// ==========================================

async function updateStats() {

    try {

        const res =
            await fetch(
                "/api/events"
            );

        const events =
            await res.json();

        const warnings =
            events.filter(
                e =>
                    e.severity ===
                    "Warning"
            ).length;

        const critical =
            events.filter(
                e =>
                    e.severity ===
                    "Critical"
            ).length;

        setText(
            "warningCount",
            warnings
        );

        setText(
            "criticalCount",
            critical
        );

        setText(
            "deviceCount",
            "1"
        );

    }

    catch (err) {

        console.error(
            err
        );

    }
}

// ==========================================
// CLOCK
// ==========================================

function updateClock() {

    const now =
        new Date();

    const clock =
        el("clock");

    if (clock)
        clock.innerHTML =
            now.toLocaleString();
}

// ==========================================
// INIT
// ==========================================

function init() {

    loadLive();
    loadEvents();
    loadRiskHistory();
    updateStats()
    updateClock();

    setInterval(
        loadLive,
        3000
    );

    setInterval(
        loadEvents,
        5000
    );

    setInterval(
        loadRiskHistory,
        5000
    );

    setInterval(
        updateStats,
        5000
    );

    setInterval(
        updateClock,
        1000
    );
}

document.addEventListener(
    "DOMContentLoaded",
    init
);