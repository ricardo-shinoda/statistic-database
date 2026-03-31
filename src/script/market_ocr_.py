import cv2
import pytesseract
import re
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# --- CONFIGURAÇÃO ---
DB_URL = 'postgresql://ricardo:3136@localhost:5432/statistic_db'
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
IMAGE_PATH = ROOT_DIR / "data_lake" / "market" / "cupom_tauste.jpg" # Ajuste o nome aqui

engine = create_engine(DB_URL)

def preprocess_image(image_path):
    if not image_path.exists():
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {image_path}")
    
    img = cv2.imread(str(image_path))
    # Converte para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Redimensiona para aumentar a resolução (ajuda muito o Tesseract)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Aplica desfoque gaussiano para tirar ruído e então o Threshold
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    return thresh

def parse_receipt(text):
    items = []
    lines = text.split('\n')
    
    # Procura um valor financeiro (ex: 10,99) que NÃO seja seguido por mais dígitos
    price_pattern = r'(\d+[\.,]\d{2})\b'
    
    for i, line in enumerate(lines):
        # 1. Limpeza de caracteres que o OCR inventa e que colam nos números
        line = re.sub(r'[ªº°\*\|&§]', '', line).strip()
        
        if len(line) < 5 or any(x in line.upper() for x in ["TOTAL", "PAGAR", "NFC", "CNPJ", "RUA"]):
            continue

        matches = list(re.finditer(price_pattern, line))
        
        if matches:
            # Pegamos o último preço da linha
            last_match = matches[-1]
            price_str = last_match.group(1).replace(',', '.')
            
            try:
                total_price = float(price_str)
            except:
                continue

            # 2. Captura a descrição e remove códigos de barras (números longos)
            raw_desc = line[:last_match.start()].strip()
            clean_desc = re.sub(r'\d{7,14}', '', raw_desc) # Tira o EAN
            clean_desc = re.sub(r'[^a-zA-Z\s]', '', clean_desc).strip() # Tira o resto do lixo
            
            # Filtro de palavras curtas (remove 'X', 'KG', etc)
            clean_desc = " ".join([w for w in clean_desc.split() if len(w) > 2])

            if len(clean_desc) > 2:
                # 3. Lógica de Desconto (o Tauste coloca '-0,42' logo abaixo)
                discount = 0
                if i + 1 < len(lines):
                    next_line = lines[i+1]
                    if "Desconto" in next_line or "-0," in next_line:
                        d_match = re.search(r'(\d+[\.,]\d{2})', next_line)
                        if d_match:
                            discount = float(d_match.group(1).replace(',', '.'))

                items.append({
                    'market_name': 'Tauste',
                    'market_location': 'Vila America - Bauru',
                    'transaction_date': '2026-03-30 08:22:00',
                    'product_code': 'OCR_AUTO',
                    'product_description': clean_desc[:50].upper(),
                    'quantity': 1.0,
                    'unit_measure': 'UN',
                    'unit_price_raw': total_price + discount,
                    'discount_item': discount,
                    'total_price_final': total_price
                })

    return items

def run_pipeline():
    print("🚀 Iniciando OCR do Cupom...")
    processed_img = preprocess_image(IMAGE_PATH)
    
    # OCR com linguagem em Português
    raw_text = pytesseract.image_to_string(processed_img, lang='por')
    print(raw_text)
    
    data = parse_receipt(raw_text)
    df = pd.DataFrame(data)
    
    if not df.empty:
        df.to_sql('fact_market_items', engine, if_exists='append', index=False)
        print(f"✅ Sucesso! {len(df)} itens inseridos no banco.")
    else:
        print("⚠️ Nenhum item identificado. Verifique a qualidade da imagem.")

if __name__ == "__main__":
    run_pipeline()