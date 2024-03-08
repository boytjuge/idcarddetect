import cv2
import pytesseract

# Load the image
image_path = '6577.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use Haar Cascade Classifier to detect license plate region
cascade_path = 'E:\pythonproject\IDPY\env\Lib\site-packages\cv2\data\haarcascade_russian_plate_number.xml'
cascade = cv2.CascadeClassifier(cascade_path)
#plates = cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=9, minSize=(120, 120)) 
plates = cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

# Loop through the detected plates and extract text using Tesseract OCR
for (x, y, w, h) in plates:
    
    plate_image = gray_image[y:y+h, x:x+w]
    custom_config = r'--oem 3 --psm 6 -l tha'
    try:
        text = pytesseract.image_to_string(plate_image, config=custom_config)
    except pytesseract.TesseractError as e:
        print("Tesseract Error:", e)

    # Draw a rectangle around the detected license plate
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Display the image with the detected license plate
cv2.imshow('License Plate Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2

cascade_path = 'E:\pythonproject\IDPY\env\Lib\site-packages\cv2\data\haarcascade_russian_plate_number.xml'
# โหลดฟังก์ชันตรวจจับจากไฟล์ XML
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# เปิดกล้อง
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # แปลงภาพเป็นภาพขาวดำ
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ตรวจจับทะเบียนรถ
    plates = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(120, 120))

    # วาดกรอบสี่เหลี่ยมรอบทะเบียนรถ
    for (x, y, w, h) in plates:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # แสดงผลลัพธ์
    cv2.imshow('License Plate Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()