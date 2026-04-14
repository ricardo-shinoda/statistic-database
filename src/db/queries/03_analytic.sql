
select * from analytics.fact_unified_payments;

drop table analytics.fact_pagamentos_unificados cascade;
drop table analytics.dim_categorias cascade;
drop table analytics.my_first_dbt_model cascade; -- Esse exemplo do dbt também não deveria estar aí

-- Teste rápido para ver se o Pix está chegando na camada final
select payment_type, count(*) 
from analytics.payments 
group by 1;

drop table analytics.payments cascade;
drop table postgres_raw.nissan_kick_consumption;

select * from postgres_raw.pagamento_cartao;
