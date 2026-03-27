from PIL import Image
import pytesseract
import json

image = Image.open('expense2.jpg')
text = pytesseract.image_to_string(image)
print(text)

text_lines = [line.strip() for line in text.split('\n') if line.strip()]

data = {
    'ocr_text': text_lines
}

output_file_path = 'cupom.json'

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print('Json file coverted and saved')