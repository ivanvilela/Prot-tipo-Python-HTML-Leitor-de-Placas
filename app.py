from flask import Flask, render_template, send_from_directory
import cv2
import numpy as np
import imutils
import pytesseract
import os

app = Flask(__name__)

# Configurar o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_plate(file_img):
    img = cv2.imread(file_img)
    (H, W) = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blur, 30, 200)
    
    # Salvar imagem de bordas para depuração
    cv2.imwrite('static/images/edged.png', edged)
    
    conts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = imutils.grab_contours(conts)
    conts = sorted(conts, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for c in conts:
        peri = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.02 * peri, True)
        if cv2.isContourConvex(aprox):
            if len(aprox) == 4:
                location = aprox
                break

    beginX = beginY = endX = endY = None
    if location is None:
        plate = False
    else:
        mask = np.zeros(gray.shape, np.uint8)
        img_plate = cv2.drawContours(mask, [location], 0, 255, -1)
        img_plate = cv2.bitwise_and(img, img, mask=mask)

        (y, x) = np.where(mask == 255)
        (beginX, beginY) = (np.min(x), np.min(y))
        (endX, endY) = (np.max(x), np.max(y))

        plate = gray[beginY:endY, beginX:endX]
        
        # Salvar imagem da placa para depuração
        cv2.imwrite('static/images/plate.png', plate)

    return img, plate, beginX, beginY, endX, endY

def ocr_plate(plate):
    config_tesseract = "--tessdata-dir tessdata --psm 8"  # Ajustar psm conforme necessário
    text = pytesseract.image_to_string(plate, lang="por", config=config_tesseract)
    text = "".join(c for c in text if c.isalnum())
    return text

def preprocessing(img):
    increase = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    _, otsu = cv2.threshold(increase, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return otsu

@app.route('/')
def index():
    # Caminho da imagem e dos arquivos de saída
    input_image_path = 'static/images/img_carro03.jpg'
    output_image_path = 'static/images/plate_detected.jpg'
    text_file = 'static/images/plate_text.txt'

    img, plate, beginX, beginY, endX, endY = detect_plate(input_image_path)
    
    if plate is not False:
        processed_plate = preprocessing(plate)
        text = ocr_plate(processed_plate)
        
        # Adicionar texto e retângulo na imagem original
        img = cv2.putText(img, text, (beginX, beginY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (150, 255, 0), 2, lineType=cv2.LINE_AA)
        img = cv2.rectangle(img, (beginX, beginY), (endX, endY), (150, 255, 0), 2)
        cv2.imwrite(output_image_path, img)
        
        # Salvar texto em arquivo
        with open(text_file, 'w') as f:
            f.write(text)
    else:
        text = "Placa não detectada"

    return render_template('index.html', plate_image='plate_detected.jpg', plate_text=text)

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    try:
        return send_from_directory('static/images', filename)
    except FileNotFoundError:
        return "Arquivo não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
