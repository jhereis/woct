-- 1. Total de operações
SELECT
    COUNT(*) AS total_operations
FROM operations;


-- 2. Volume financeiro solicitado
SELECT
    ROUND(SUM(requested_amount), 2) AS total_requested_amount
FROM operations;


-- 3. Operações por status
SELECT
    current_status,
    COUNT(*) AS total_operations
FROM operations
GROUP BY current_status
ORDER BY total_operations DESC;


-- 4. Operações fora do SLA
SELECT
    sla_status,
    COUNT(*) AS total_operations
FROM operations
GROUP BY sla_status
ORDER BY total_operations DESC;


-- 5. Operações por nível de risco
SELECT
    operational_risk,
    COUNT(*) AS total_operations
FROM operations
GROUP BY operational_risk
ORDER BY total_operations DESC;


-- 6. Taxa de exceções
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN exception_flag = 1 THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS exception_rate_percentage
FROM operations;


-- 7. Resultado da reconciliação
SELECT
    reconciliation_status,
    COUNT(*) AS total_operations
FROM operations
GROUP BY reconciliation_status
ORDER BY total_operations DESC;


-- 8. Valor financeiro das divergências
SELECT
    ROUND(SUM(ABS(difference_amount)), 2) AS total_reconciliation_difference
FROM operations
WHERE reconciliation_status <> 'Matched';


-- 9. Operações críticas ou de alto risco
SELECT
    operation_id,
    client_id,
    operation_type,
    requested_amount,
    current_status,
    sla_status,
    operational_risk,
    reconciliation_status
FROM operations
WHERE operational_risk = 'High'
   OR reconciliation_status <> 'Matched'
ORDER BY requested_amount DESC
LIMIT 20;

-- 10. Resumo executivo para o dashboard
SELECT
    COUNT(*) AS total_operations,

    ROUND(SUM(requested_amount), 2) AS total_requested_amount,

    SUM(
        CASE
            WHEN sla_status = 'Outside SLA' THEN 1
            ELSE 0
        END
    ) AS outside_sla_operations,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN sla_status = 'Outside SLA' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS outside_sla_percentage,

    SUM(
        CASE
            WHEN exception_flag = 1 THEN 1
            ELSE 0
        END
    ) AS exception_operations,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN exception_flag = 1 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS exception_percentage,

    SUM(
        CASE
            WHEN reconciliation_status <> 'Matched' THEN 1
            ELSE 0
        END
    ) AS reconciliation_issues,

    ROUND(
        SUM(
            CASE
                WHEN reconciliation_status <> 'Matched'
                THEN ABS(difference_amount)
                ELSE 0
            END
        ),
        2
    ) AS reconciliation_difference_value

FROM operations;
