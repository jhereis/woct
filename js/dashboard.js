const CSV_PATH = "../data/processed/dashboard_operations.csv";

let allOperations = [];
let filteredOperations = [];

let charts = {};

/* =========================================================
   WOCT — Institutional Color Palette
   ========================================================= */

const CHART_COLORS = [
    "#315D9B", // Azul institucional
    "#557DB2", // Azul médio
    "#7899C4", // Azul intermediário
    "#8FA8CC", // Azul suave
    "#B5C5DA", // Azul claro
    "#D5DFEC", // Azul muito suave
    "#E3EAF3", // Azul quase branco
    "#6B88B5", // Azul complementar
    "#476D9F", // Azul escuro médio
    "#244A82"  // Azul-marinho
];

const SLA_COLORS = [
    "#315D9B",
    "#557DB2",
    "#8FA8CC",
    "#D5DFEC"
];

const RECONCILIATION_COLORS = [
    "#315D9B", // Matched
    "#C98218", // Status Difference
    "#C9281D", // Amount Difference
    "#8FA8CC"  // Missing in External System
];

const EXCEPTION_COLORS = [
    "#C98218",
    "#C9281D",
    "#557DB2",
    "#8FA8CC",
    "#B5C5DA"
];

/* =========================================================
   Formatters
   ========================================================= */

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

function formatCurrency(value) {
    return currencyFormatter.format(value);
}

const numberFormatter = new Intl.NumberFormat("pt-BR");

/* =========================================================
   Helpers
   ========================================================= */

function parseNumber(value) {
    if (value === null || value === undefined || value === "") {
        return 0;
    }

    return Number(String(value).replace(",", ".")) || 0;
}

function normalizeBoolean(value) {
    return value === true ||
        value === 1 ||
        value === "1" ||
        value === "true" ||
        value === "True";
}

function uniqueValues(data, field) {
    return [...new Set(
        data
            .map(row => row[field])
            .filter(value => value !== undefined && value !== "")
    )].sort();
}

/* =========================================================
   Filters
   ========================================================= */

function populateFilters() {
    const filters = [
        {
            id: "statusFilter",
            field: "current_status"
        },
        {
            id: "riskFilter",
            field: "operational_risk"
        },
        {
            id: "slaFilter",
            field: "sla_status"
        },
        {
            id: "reconciliationFilter",
            field: "reconciliation_status"
        }
    ];

    filters.forEach(filter => {
        const select = document.getElementById(filter.id);

        uniqueValues(allOperations, filter.field).forEach(value => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value;
            select.appendChild(option);
        });
    });
}

function applyFilters() {
    const status = document.getElementById("statusFilter").value;
    const risk = document.getElementById("riskFilter").value;
    const sla = document.getElementById("slaFilter").value;
    const reconciliation = document.getElementById("reconciliationFilter").value;

    filteredOperations = allOperations.filter(operation => {
        return (
            (status === "all" || operation.current_status === status) &&
            (risk === "all" || operation.operational_risk === risk) &&
            (sla === "all" || operation.sla_status === sla) &&
            (
                reconciliation === "all" ||
                operation.reconciliation_status === reconciliation
            )
        );
    });

    updateDashboard();
}

function clearFilters() {
    document.getElementById("statusFilter").value = "all";
    document.getElementById("riskFilter").value = "all";
    document.getElementById("slaFilter").value = "all";
    document.getElementById("reconciliationFilter").value = "all";

    applyFilters();
}

/* =========================================================
   Aggregations
   ========================================================= */

function countByField(data, field) {
    return data.reduce((result, row) => {
        const value = row[field] || "Not informed";
        result[value] = (result[value] || 0) + 1;
        return result;
    }, {});
}

function sumByField(data, categoryField, valueField) {
    return data.reduce((result, row) => {
        const category = row[categoryField] || "Not informed";
        result[category] = (result[category] || 0) + parseNumber(row[valueField]);
        return result;
    }, {});
}

/* =========================================================
   KPIs
   ========================================================= */

function updateKpis() {
    const total = filteredOperations.length;

    const volume = filteredOperations.reduce(
        (sum, operation) => sum + parseNumber(operation.requested_amount),
        0
    );

    const outsideSla = filteredOperations.filter(
        operation => operation.sla_status === "Outside SLA"
    ).length;

    const exceptions = filteredOperations.filter(
        operation => normalizeBoolean(operation.exception_flag)
    ).length;

    const reconciliationIssues = filteredOperations.filter(
        operation => operation.reconciliation_status !== "Matched"
    );

    const reconciliationValue = reconciliationIssues.reduce(
        (sum, operation) => sum + Math.abs(parseNumber(operation.difference_amount)),
        0
    );

    document.getElementById("totalOperations").textContent =
        numberFormatter.format(total);

    document.getElementById("totalVolume").textContent =
        currencyFormatter.format(volume);

    document.getElementById("outsideSla").textContent =
        `${total ? ((outsideSla / total) * 100).toFixed(1) : 0}%`;

    document.getElementById("exceptionRate").textContent =
        `${total ? ((exceptions / total) * 100).toFixed(1) : 0}%`;

    document.getElementById("reconciliationValue").textContent =
        currencyFormatter.format(reconciliationValue);
}

/* =========================================================
   Chart Defaults
   ========================================================= */

function chartOptions(showLegend = false) {
    return {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                display: showLegend,
                position: "bottom",

                labels: {
                    color: "#697386",
                    font: {
                        family: "Inter, Arial, sans-serif",
                        size: 12
                    },
                    padding: 18,
                    usePointStyle: true,
                    pointStyle: "circle"
                }
            },

            tooltip: {
                backgroundColor: "#172033",
                titleColor: "#FFFFFF",
                bodyColor: "#FFFFFF",
                borderColor: "#E3E8EF",
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8
            }
        },

        scales: {
            y: {
                beginAtZero: true,

                grid: {
                    color: "#E3E8EF",
                    drawBorder: false
                },

                ticks: {
                    precision: 0,
                    color: "#697386",
                    font: {
                        family: "Inter, Arial, sans-serif",
                        size: 11
                    }
                }
            },

            x: {
                grid: {
                    display: false,
                    drawBorder: false
                },

                ticks: {
                    color: "#697386",
                    font: {
                        family: "Inter, Arial, sans-serif",
                        size: 11
                    }
                }
            }
        }
    };
}

/* =========================================================
   Chart Creation
   ========================================================= */

function createOrUpdateChart(id, type, labels, values, options = {}) {
    if (charts[id]) {
        charts[id].destroy();
    }

    let colors = CHART_COLORS;

    if (id === "slaChart") {
        colors = SLA_COLORS;
    }

    if (id === "reconciliationChart") {
        colors = RECONCILIATION_COLORS;
    }

    if (id === "exceptionChart") {
        colors = EXCEPTION_COLORS;
    }

    charts[id] = new Chart(
        document.getElementById(id),
        {
            type,

            data: {
                labels,

                datasets: [{
                    data: values,

                    backgroundColor: colors,

                    borderColor: "#FFFFFF",
                    borderWidth: type === "doughnut" ? 3 : 0,

                    borderRadius: type === "bar" ? 5 : 0,

                    hoverOffset: type === "doughnut" ? 4 : 0
                }]
            },

            options: {
                ...chartOptions(options.showLegend),
                ...options
            }
        }
    );
}

/* =========================================================
   Charts
   ========================================================= */

function updateCharts() {

    /* Operations by current status */

    const statusData = countByField(
        filteredOperations,
        "current_status"
    );

    createOrUpdateChart(
        "statusChart",
        "bar",
        Object.keys(statusData),
        Object.values(statusData),
        {
            indexAxis: "y"
        }
    );


    /* SLA performance */

    const slaData = countByField(
        filteredOperations,
        "sla_status"
    );

    createOrUpdateChart(
        "slaChart",
        "doughnut",
        Object.keys(slaData),
        Object.values(slaData),
        {
            showLegend: true,

            scales: {},

            cutout: "62%"
        }
    );


    /* Operational risk */

    const riskData = countByField(
        filteredOperations,
        "operational_risk"
    );

    createOrUpdateChart(
        "riskChart",
        "bar",
        Object.keys(riskData),
        Object.values(riskData)
    );


    /* Reconciliation */

    const reconciliationData = countByField(
        filteredOperations,
        "reconciliation_status"
    );

    createOrUpdateChart(
        "reconciliationChart",
        "bar",
        Object.keys(reconciliationData),
        Object.values(reconciliationData),
        {
            indexAxis: "y"
        }
    );


    /* Financial volume by operation type */

    const volumeData = sumByField(
        filteredOperations,
        "operation_type",
        "requested_amount"
    );

    createOrUpdateChart(
        "volumeChart",
        "bar",
        Object.keys(volumeData),
        Object.values(volumeData),
        {
            indexAxis: "y",

            plugins: {
                tooltip: {
                    callbacks: {
                        label: context =>
                            currencyFormatter.format(context.raw)
                    }
                }
            }
        }
    );


    /* Exceptions */

    const exceptionData = countByField(
        filteredOperations.filter(operation =>
            normalizeBoolean(operation.exception_flag)
        ),
        "exception_type"
    );

    createOrUpdateChart(
        "exceptionChart",
        "bar",
        Object.keys(exceptionData),
        Object.values(exceptionData),
        {
            indexAxis: "y"
        }
    );
}

/* =========================================================
   Badges
   ========================================================= */

function badgeClass(value) {
    const normalized = String(value || "").toLowerCase();

    if (normalized.includes("critical")) return "badge badge-critical";
    if (normalized.includes("high")) return "badge badge-high";
    if (normalized.includes("low")) return "badge badge-low";
    if (normalized.includes("within")) return "badge badge-within";
    if (normalized.includes("outside")) return "badge badge-outside";
    if (normalized.includes("matched")) return "badge badge-matched";

    if (
        normalized.includes("difference") ||
        normalized.includes("missing")
    ) {
        return "badge badge-divergence";
    }

    return "badge";
}

/* =========================================================
   Operations Table
   ========================================================= */

function updateTable() {
    const tableBody = document.getElementById("operationsTable");

    const priorityOperations = [...filteredOperations]
        .filter(operation =>
            operation.sla_status === "Outside SLA" ||
            operation.operational_risk === "Critical" ||
            operation.reconciliation_status !== "Matched"
        )
        .sort((a, b) => {
            const riskWeight = {
                Critical: 3,
                High: 2,
                Low: 1
            };

            const riskDifference =
                (riskWeight[b.operational_risk] || 0) -
                (riskWeight[a.operational_risk] || 0);

            if (riskDifference !== 0) {
                return riskDifference;
            }

            return parseNumber(b.requested_amount) -
                parseNumber(a.requested_amount);
        })
        .slice(0, 20);

    tableBody.innerHTML = "";

    priorityOperations.forEach(operation => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${operation.operation_id || "-"}</td>
            <td>${operation.client_id || "-"}</td>
            <td>${operation.operation_type || "-"}</td>
            <td>${currencyFormatter.format(parseNumber(operation.requested_amount))}</td>
            <td>${operation.current_status || "-"}</td>
            <td>
                <span class="${badgeClass(operation.sla_status)}">
                    ${operation.sla_status || "-"}
                </span>
            </td>
            <td>
                <span class="${badgeClass(operation.operational_risk)}">
                    ${operation.operational_risk || "-"}
                </span>
            </td>
            <td>
                <span class="${badgeClass(operation.reconciliation_status)}">
                    ${operation.reconciliation_status || "-"}
                </span>
            </td>
        `;

        tableBody.appendChild(row);
    });

    document.getElementById("tableCount").textContent =
        `${priorityOperations.length} priority operations`;
}

/* =========================================================
   Dashboard
   ========================================================= */

function updateDashboard() {
    updateKpis();
    updateCharts();
    updateTable();
}

/* =========================================================
   CSV Loading
   ========================================================= */

function loadCsv() {
    Papa.parse(CSV_PATH, {
        download: true,
        header: true,
        skipEmptyLines: true,

        complete: results => {
            allOperations = results.data;
            filteredOperations = [...allOperations];

            populateFilters();
            updateDashboard();
        },

        error: error => {
            console.error("Error loading CSV:", error);

            alert(
                "Could not load the CSV. Run the dashboard through a local server."
            );
        }
    });
}

/* =========================================================
   Initialization
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    document
        .getElementById("statusFilter")
        .addEventListener("change", applyFilters);

    document
        .getElementById("riskFilter")
        .addEventListener("change", applyFilters);

    document
        .getElementById("slaFilter")
        .addEventListener("change", applyFilters);

    document
        .getElementById("reconciliationFilter")
        .addEventListener("change", applyFilters);

    document
        .getElementById("clearFilters")
        .addEventListener("click", clearFilters);

    loadCsv();
});
