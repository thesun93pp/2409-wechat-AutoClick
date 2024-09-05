import sys
import uiautomator2 as u2
import time
from PIL import Image, ImageOps
import pytesseract
import re
import cv2

# Get the device_id, username, password, and phone from command-line arguments
device_id = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
phone = sys.argv[4]

posCapcha = [(0.1889, 0.4982), (0.4843, 0.5054), (0.7981, 0.5041), (0.1889, 0.6477), (0.9926, 0.405), (0.8009,0.65)]


def SolveCapcha(d, device_id):
    d.screenshot(f"photos/capcha/{device_id}_capcha.jpg")

def PictureCompare(d, text):
    screenshot = d.screenshot(format='opencv')
    extracted_text = pytesseract.image_to_string(screenshot)
    # print(normalize_text(extracted_text))
    # Normalize both the extracted and target text for a more reliable comparison
    return normalize_text(text) in normalize_text(extracted_text)

def CheckWebPolicy():
    d.click(0.143, 0.742)
    time.sleep(5)
    d.click(0.484, 0.812)
    time.sleep(5)
    #Detect Spamming
    if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
        print("Spamming Found!")
        d.app_stop_all()
        return

def CheckXacMinhBaoMat():
    d.click(0.489, 0.847)

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()  # Normalize spaces and convert to lowercase

def CheckCase(d, device_id):
    time.sleep(3)
    d.screenshot(f"photos/{device_id}_home.jpg")
    result_1 = pytesseract.image_to_string(Image.open(f"photos/{device_id}_home.jpg"))
    print("================================================")
    print(result_1)
    print("================================================")

    if "Invite another user to scan" in result_1 or "Select a Security Verification" in result_1:
        return False
    elif "SMS" in result_1:
        return True

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    return img

def process_device(d, device_id, username, password, phone):
    d.app_stop_all()

    # Check if the WeChat app is installed
    try:
        app_info = d.app_info("com.tencent.mm")
        print(f"WeChat app is already installed on {device_id}.")
    except Exception as e:
        print(f"WeChat app is not installed on {device_id}. Installing the app...")
        d.app_install('apk/wechat.apk')

    # Start the WeChat app
    d.app_start("com.tencent.mm")

    d(resourceId="com.tencent.mm:id/mjy").click()
    d.xpath('//*[@resource-id="com.tencent.mm:id/avc"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()

    # Enter name
    d(resourceId="com.tencent.mm:id/d98", text="Trần Anh").click()
    d.send_keys(username, clear=True)

    # Enter phone number
    d(resourceId="com.tencent.mm:id/d98", text="Nhập số di động").click()
    d.send_keys(phone, clear=True)

    # Enter password
    d(resourceId="com.tencent.mm:id/d98", text="Nhập mật khẩu").click()
    d.send_keys(password, clear=True)

    #Checkbox Read policy
    d(resourceId="com.tencent.mm:id/lrt").click()
    #Accept and continue
    d(resourceId="com.tencent.mm:id/lrn").click()
    time.sleep(10)

    # webPolicy
    if PictureCompare(d, "CHINH SACH BAO MAT CUA WECHAT"):
        print('Web Policy [ PASSED ]')
        CheckWebPolicy()
    else:
        print('Web Policy [ FAILED ]')

    # Xac Minh Bao Mat
    if PictureCompare(d, "XAC MINH BAO MAT"):
        print('Xac Minh Bao Mat [ PASSED ]')
        CheckXacMinhBaoMat()
    else:
        print('Xac Minh Bao Mat FAILED')

    # Wait to load Capcha
    time.sleep(5)
    # Xac Minh Capcha
    if PictureCompare(d, "select all images that match"):
        print('Xac Minh Capcha [ PASSED ]')
        SolveCapcha(d, device_id)
    else:
        print('Xac Minh Capcha [ FAILED ]')


    
    # d.click(0.143, 0.742)
    # time.sleep(5)
    # d.click(0.484, 0.812)
    # time.sleep(5)

    # if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
    #     print("Spamming Found!")
    #     d.app_stop_all()
    #     return

    # d.click(0.489, 0.847)
    # time.sleep(5)
    # SolveCapcha(d, device_id)
    # d.click(0.211, 0.787)

    # #Test
    # time.sleep(1)
    # d.screenshot(f"photos/{device_id}_test.jpg")

    # # Extract text from the image
    # result_test = pytesseract.image_to_string(Image.open(f"photos/{device_id}_test.jpg"))

    # # Filter out digits
    # timeMustWait = ''.join([char for char in result_test if char.isdigit()])

    # # Convert the filtered digits to a number (integer or float)
    # if timeMustWait:
    #     timeMustWait = int(timeMustWait)  # Use float(timeMustWait) if fractional seconds are needed
    #     time.sleep(timeMustWait)

    # #spam to get back login form
    # d.click(0.489, 0.847)
    # time.sleep(0.2)
    # d.click(0.489, 0.847)
    # time.sleep(0.2)
    # d.click(0.489, 0.847)
    # time.sleep(0.2)
    # d.click(0.489, 0.847)
    # time.sleep(0.2)
    # d.click(0.489, 0.847)

    # while True:
    #     if CheckCase(d, device_id):
    #         print("Done")
    #         break
    #     else:
    #         print("Try to re-sign up")
    #         d.click(0.05, 0.063)
    #         d(resourceId="com.tencent.mm:id/lrn").click()

    #         if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
    #             d.app_stop_all()
    #             break

    #         time.sleep(5)
    #         d.click(0.491, 0.852)
    #         time.sleep(5)
    #         d.click(0.244, 0.749)
    #         time.sleep(30)

    #     time.sleep(2)

# Connect to the device
d = u2.connect(device_id)
process_device(d, device_id, username, password, phone)
