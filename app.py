from flask import *
import cv2
app=Flask(__name__)

def prediction1(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    number_plate_contours = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(contour)
        if aspect_ratio > 2.0 and aspect_ratio < 5.0 and area > 1000:
            number_plate_contours.append(contour)
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
    for contour in number_plate_contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        roi = blurred[y:y+h, x:x+w]
        number_plate_text = pytesseract.image_to_string(roi, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -l eng')
        return number_plate_text

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/NPR')
def NPR():
    return render_template('NPR.html')

@app.route('/NPRImage')
def NPRImage():
    return render_template('NPR Image.html')

@app.route('/predict1',methods=["GET","POST"])
def predict1():
    file=request.files['file']
    file_path = r"D:\Project Space\Front End\static\Storage" + file.filename
    file.save(file_path)  
    k=prediction1(file_path)
    return render_template('prediction1.html',ans=k)

@app.route('/NPRVideo')
def NPRVideo():
    return render_template('NPR Video.html')

if __name__=='__main__':
    app.run(debug=True)