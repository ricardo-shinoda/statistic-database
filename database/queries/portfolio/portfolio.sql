-- Sum of all the portfolio grouped by investor
SELECT
    i.investor,
    'R$ ' || 
    REPLACE(
        REPLACE(
            REPLACE(
                TO_CHAR(SUM(i.montante_total)::numeric, 'FM999,999,990.00'), 
                ',', 'X'
            ), 
            '.', ','
        ), 
        'X', '.'
    ) AS patrimonio_formatado
FROM analytics.fct_investments_portfolio i
GROUP BY i.investor
ORDER BY SUM(i.montante_total) DESC;