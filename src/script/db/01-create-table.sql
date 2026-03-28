-- Create the Dimension Table for Merchant Mapping
CREATE TABLE IF NOT EXISTS dim_merchant_mapping (
    original_description TEXT PRIMARY KEY,
    mapped_category TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);