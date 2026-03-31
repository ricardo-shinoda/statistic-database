-- Run this in SQLTools/VS Code first!
CREATE TABLE IF NOT EXISTS dim_merchant_mapping (
    original_description TEXT PRIMARY KEY,
    mapped_category TEXT NOT NULL,
    mapped_subcategory TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    subcategory TEXT,
    amount_brl NUMERIC(15, 2) NOT NULL,
    card_holder_name TEXT,     
    installment_info TEXT,     -- e.g., '1/4'
    transaction_type TEXT,      -- 'credit_card' or 'manual_bill'
    status TEXT,               
    source_file TEXT,          
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE fact_transactions ADD COLUMN IF NOT EXISTS installment_info TEXT;

ALTER TABLE fact_transactions 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

