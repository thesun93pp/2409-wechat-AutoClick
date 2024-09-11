import sys
import uiautomator2 as u2
import time
from PIL import Image, ImageOps
import pytesseract
import re
import cv2
import subprocess
import requests
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

# Get the device_id, username, password, and phone from command-line arguments
device_ids = sys.argv[1:]  # Accepts multiple device IDs
username = sys.argv[2]
password = sys.argv[3]
phone = sys.argv[4]

spamDetect = False

def toggle_mobile_data(device_id, state):
    command = ["adb", "-s", device_id, "shell", "svc", "data", "enable"] if state else ["adb", "-s", device_id, "shell", "svc", "data", "disable"]
    subprocess.run(command)

def solve_captcha(d, device_id):
    d.screenshot(f"photos/captcha/{device_id}_captcha.jpg")

def picture_compare(d, text):
    screenshot = d.screenshot(format='opencv')
    extracted_text = pytesseract.image_to_string(screenshot)
    return normalize_text(text) in normalize_text(extracted_text)

def reset_phone(d):
    global spamDetect
    spamDetect = True
    d.app_stop_all()
    time.sleep(3)
    app_icon = d(description="Pixel Changer")
    if app_icon.exists:
        app_icon.click()
        if d(resourceId="app.haonam.xz2changer:id/").wait(timeout=5):
            d(resourceId="app.haonam.xz2changer:id/").click()
    else:
        print("App 'Pixel Changer' not found.")

def check_web_policy(d):
    d.click(0.143, 0.742)
    time.sleep(1)
    d.click(0.484, 0.812)
    time.sleep(5)
    if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
        print("Spamming detected!")
        reset_phone(d)
        return False
    return True

def check_security_verification(d):
    d.click(0.489, 0.847)

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    return img

def handle_captcha_result(d, captcha_result):
    posCapcha = [
        (0.1889, 0.4982),  # Index 0
        (0.4843, 0.5054),  # Index 1
        (0.7981, 0.5041),  # Index 2
        (0.1889, 0.6477),  # Index 3
        (0.9926, 0.405),   # Index 4
        (0.8009, 0.65)     # Index 5
    ]
    result = captcha_result.get('result', [])
    for index in result:
        if 1 <= index <= len(posCapcha):
            x, y = posCapcha[index-1]
            print(f"Clicking at position: ({x}, {y})")
            d.click(x, y)
            time.sleep(2)
        else:
            print(f"Invalid index {index} for posCapcha list")

# def post_device_success(device_id):
#     # Update the Flask server with the successful device
#     headers = {'Content-Type': 'application/json'}
#     try:
#         response = requests.post('http://127.0.0.1:5000/api/success', json={
#             'device_id': device_id,
#         }, headers=headers)
#         if response.status_code == 200:
#             print(f"Successfully posted {device_id} to the server.")
#         else:
#             print(f"Failed to post {device_id} to the server. Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error posting {device_id} to the server: {e}")


def captcha_process(api_url, request_id, d):
    screenshot = d.screenshot(format='opencv')
    _, buffer = cv2.imencode('.jpg', screenshot)
    image_bytes = BytesIO(buffer)
    files = {'image': ('captcha.jpg', image_bytes, 'image/jpeg')}
    data = {'requestID': request_id}
    response = requests.post(api_url, files=files, data=data)
    if response.status_code == 200:
        print("CAPTCHA processed successfully.")
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def process_device(d, device_id, username, password, phone):
    global spamDetect
    try:
        d.app_stop_all()
        try:
            d.app_info("com.tencent.mm")
            print(f"WeChat app is already installed on {device_id}.")
        except Exception as e:
            print(f"WeChat app is not installed on {device_id}. Installing the app...")
            d.app_install('apk/wechat.apk')

        toggle_mobile_data(device_id, True)
        d.app_start("com.tencent.mm")
        d(resourceId="com.tencent.mm:id/mjy").click()
        d.xpath('//*[@resource-id="com.tencent.mm:id/avc"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()

        d(resourceId="com.tencent.mm:id/d98", text="Trần Anh").click()
        d.send_keys(username, clear=True)
        d(resourceId="com.tencent.mm:id/d98", text="Nhập số di động").click()
        d.send_keys(phone, clear=True)
        d(resourceId="com.tencent.mm:id/d98", text="Nhập mật khẩu").click()
        d.send_keys(password, clear=True)

        d(resourceId="com.tencent.mm:id/lrt").click()
        d(resourceId="com.tencent.mm:id/lrn").click()
        time.sleep(10)

        if picture_compare(d, "CHINH SACH BAO MAT CUA WECHAT"):
            print('Web Policy [ PASSED ]')
            if not check_web_policy(d):
                return False
        else:
            print('Web Policy [ FAILED ]')
            return False
        
        time.sleep(3)

        if picture_compare(d, "XAC MINH BAO MAT"):
            print('Xac Minh Bao Mat [ PASSED ]')
            check_security_verification(d)
        else:
            print('Xac Minh Bao Mat [ FAILED ]')
            return False

        time.sleep(5)
        if picture_compare(d, "select all images that match"):
            print('Xac Minh Capcha [ PASSED ]')
            captcha_result = captcha_process('https://resolver.metajobs.vn/process-image', device_id, d)
            if captcha_result:
                print(captcha_result)
                handle_captcha_result(d, captcha_result)
                time.sleep(0.5)
                d.click(0.8815, 0.7455)
                time.sleep(0.5)
                if picture_compare(d, "Operation too often"):
                    print("Spam Capcha Detected!")
                    reset_phone(d)
            else:
                print('Xac Minh Capcha [ FAILED ]')
                return False

        time.sleep(2)
        
        if picture_compare(d, "select all images that match"):
            return False
        
        if picture_compare(d, "Invite another user") or  picture_compare(d, "Select a Security"):
            print("Good but we better should try again!")
            return False
        
        

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
    return True

def process_device_task(device_id, username, password, phone):
    d = u2.connect(device_id)
    retries = 0
    while True:
        if spamDetect:
            print("spamDetect is True, exiting Auto Mode.")
            break

        if process_device(d, device_id, username, password, phone):
            print(f"Process completed successfully on {device_id}.")
            break
        else:
            retries += 1
            print(f"Retrying device {device_id}... ({retries})")
            time.sleep(10)

def main(device_ids, username, password, phone):
    global spamDetect
    with ThreadPoolExecutor(max_workers=len(device_ids)) as executor:
        futures = [executor.submit(process_device_task, device_id, username, password, phone) for device_id in device_ids]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

if __name__ == "__main__":
    main(device_ids, username, password, phone)
