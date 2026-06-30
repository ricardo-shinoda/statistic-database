SELECT
    i.investor,
    round(sum(i.montante_total)::numeric, 2) as patrimonio_em_reais
FROM analytics.fct_investments_portfolio i
GROUP BY i.investor
ORDER BY sum(i.montante_total) DESC;

-- Sum of all the portfolio grouped by investor1
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
