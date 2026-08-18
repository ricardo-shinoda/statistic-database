SELECT * FROM analytics.fct_monthly_investments;

SELECT
    investor,
    data_mes,
    sum(total_aplicado) as total_aplicado
FROM analytics.fct_monthly_investments
GROUP BY data_mes, investor
ORDER BY data_mes DESC;