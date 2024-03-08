from flask import Flask, request, jsonify ,redirect ,render_template
from PIL import Image
import pytesseract
import os
import re
from flask import json

app = Flask(__name__)

# Path to Tesseract executable (replace with your path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_id_card(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='tha+eng')
    print(text)
    return text


@app.route('/api/read_id_card', methods=['POST'])
def api_read_id_card():
    # Assume the image file is sent as form data with key 'image'
    image_file = request.files['image']
    print(image_file)
    image_path =  'temp.jpg'
    image_file.save(image_path)
    text = read_id_card(image_path)
    print(text)
    # ใช้ regex เพื่อหา pattern ของข้อมูลที่ต้องการ
    # regex pattern สำหรับคำนำหน้าในภาษาไทย
    # title_pattern = r"(Mr\.|นาย|นาง|นางสาว|น\.ส\.)\s(\w+)"
    #     # ค้นหาคำนำหน้าในข้อความ
    # name_pattern = r"Name (\w+)" or r"ชื่อ (\w+)"
    # last_name_pattern = r"Lastname (\w+)"or r"สกุล (\w+)"
    # id_pattern = r"เลขประจําตัวประชาชน =. (\d{1,2} \d{4} \d{4} \d{2} \d)"
    # dob_pattern = r"เกิดวันที (\d+ \w+ \d{4})"
    # religion_pattern = r"ศาสนา (\w+)"

    # # ค้นหาข้อมูลที่ต้องการในข้อความ
    # title_match = re.search(title_pattern, text)
    # name_match = re.search(name_pattern, text)
    # last_name_match = re.search(last_name_pattern, text)
    # id_match = re.search(id_pattern, text)
    # dob_match = re.search(dob_pattern, text)
    # religion_match = re.search(religion_pattern, text)
    # title = ''
    # # สร้าง dictionary เพื่อเก็บข้อมูล
    # data = {}
    # if title_match: 
    #     data['คำนำหน้า'] = title_match.group(1)
    #     data['ชื่อ'] = title_match.group(2)
    # # if name_match:
    # #     data['ชื่อ'] = name_match.group(1)
    # if last_name_match:
    #     data['สกุล'] = last_name_match.group(1)
    # if id_match:
    #     data['รหัสบัตรประชาชน'] = id_match.group(1)
    # if dob_match:
    #     data['วันเดือนปีเกิด'] = dob_match.group(1)
    # if religion_match:
    #     data['ศาสนา'] = religion_match.group(1)
    # regex pattern สำหรับค้นหาข้อมูลที่ต้องการ
    prefix_pattern = r"(นาย|นาง|นางสาว|น\.ส\.|M\.R\.)"
    #name_pattern = r"ชื่อตัวและชื่อสกุล\s(\S+)\s(\S+)"
    name_pattern = r"ชื่อตัวและชื่อสกุล\s(.+)" or r"ชื่อ\s(.+)" or r"Name \s(.+)"
    id_pattern = r"เลขประจําตัวประชาชน\s(.+)"
    dob_pattern = r"เกิดวันที (\d+ \w+ \d{4})"
    address_pattern = r"ที่อยู่\s(.+)"
    religion_pattern = r"ศาสนา\s(.+)"
    prefix_en = r"(Mr\.)"
    name_en_pattern = r"Name \s(.+)"
    lastname_en_pattern = r"Last Name \s(.+)"
    # ค้นหาข้อมูลที่ต้องการในข้อความ
    prefix_match = re.search(prefix_pattern, text)
    name_match = re.search(name_pattern, text)
    id_match = re.search(id_pattern, text)
    dob_match = re.search(dob_pattern, text)
    address_match = re.search(address_pattern, text)
    religion_match = re.search(religion_pattern, text)
    prefix_en_match = re.search(prefix_en, text)
    name_en_match = re.search(name_en_pattern, text)
    lastname_en_match = re.search(lastname_en_pattern,text)
    # ใช้ regex เพื่อค้นหาวันที่ในรูปแบบ dd MMM yyyy
    date_pattern = r'\b\d{1,2}\s(?:ม.ค.|ก.พ.|มี.ค.|เม.ย.|พ.ค.|มิ.ย.|ก.ค.|ส.ค.|ก.ย.|ต.ค.|พ.ย.|ธ.ค.)\s\d{4}\b'

    dates = re.findall(date_pattern, text)
    print(dates)
    for date in dates:
        print(date)
    # สร้าง dictionary เพื่อเก็บข้อมูล
    data = {}
    if prefix_match:
        data['title'] = prefix_match.group(1)
    if name_match:
        data['name'] = name_match.group(1)
        #data['สกุล'] = name_match.group(2)
    if id_match:
        data['nationalid'] = id_match.group(1)
    if prefix_en_match: 
        data['title_en'] = prefix_en_match.group(1)
    if name_en_match: 
        data['name_en'] = name_en_match.group(1)
    if lastname_en_match:
        data['lastname_en'] = lastname_en_match.group(1)
    if dates:
        data['DOB'] = dates[0]
        try:
             data['DateofIssue']  = dates[1]
        except:
            data['DateofIssue'] =''
        try:
            data['DateofExpiry'] = dates[2]
        except:
            data['DateofExpiry'] = ''

    if address_match:
        data['address'] = address_match.group(1)
    if religion_match:
        data['religion'] = religion_match.group(1)
    # แสดงข้อมูลที่ได้
    for key, value in data.items():
        print(f"{key}: {value}")
    
    return jsonify({'text': data,'realtext':text}), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/api/fill_form', methods=['POST'])
def api_fill_form():
    data = request.json
    # Process the form data and fill out the form automatically
    # (Implementation depends on the form structure and requirements)
    return jsonify({'message': 'Form filled out successfully'})

@app.route('/upload')
def form_up():
    return render_template('uploadfile.html')

if __name__ == '__main__':
    app.run(debug=True)
