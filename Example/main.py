import sys
import uiautomator2 as u2
import time
from PIL import Image, ImageOps
import pytesseract

user = 'tuioai2'
password = 'asdaXXX12@eze'
phone = '0859781699'

# Get the device IDs from command-line arguments
# For example: python script.py emulator-5554 emulator-5556
device_ids = sys.argv[1:]  # List of device IDs from command-line arguments

def SolveCapcha(d, device_id):
    # Take screenshot
    d.screenshot(f"photos/{device_id}_capcha.jpg")

def CheckCase(d, device_id):
    # Take screenshot
    d.screenshot(f"photos/{device_id}_home.jpg")
    
    # Example usage
    result_1 = pytesseract.image_to_string(Image.open(f"photos/{device_id}_home.jpg"))

    print("================================================")
    print(result_1)
    print("================================================")

    if "Invite another user to scan" in result_1 or "Select a Security verification method" in result_1:
        return False
    else:
        return True

def preprocess_image(image_path):
    img = Image.open(image_path)
    # Convert image to grayscale
    img = ImageOps.grayscale(img)
    # Increase contrast or apply thresholding as needed
    # img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img

def process_device(d, device_id):
    # Stop all apps
    d.app_stop_all()

    # Open WeChat app
    d.app_start("com.tencent.mm")

    # Register via phone number
    d(resourceId="com.tencent.mm:id/mjy").click()
    d.xpath('//*[@resource-id="com.tencent.mm:id/avc"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()

    # Enter name
    d(resourceId="com.tencent.mm:id/d98", text="Trần Anh").click()
    d.send_keys(user, clear=True)

    # Enter phone number
    d(resourceId="com.tencent.mm:id/d98", text="Nhập số di động").click()
    d.send_keys(phone, clear=True)

    # Enter password
    d(resourceId="com.tencent.mm:id/d98", text="Nhập mật khẩu").click()
    d.send_keys(password, clear=True)

    # Agree to terms and conditions
    d(resourceId="com.tencent.mm:id/lrt").click()
    d(resourceId="com.tencent.mm:id/lrn").click()

    time.sleep(10)

    # Agree to privacy policy
    d.click(0.143, 0.742)
    time.sleep(5)

    # Next
    d.click(0.484, 0.812)
    time.sleep(5)

    # Check if spamming is detected
    if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
        print("Spamming Found!")
        d.app_stop_all()
        return

    # Verify security
    d.click(0.489, 0.847)
    time.sleep(5)

    # Solve captcha
    SolveCapcha(d, device_id)
    d.click(0.211, 0.787)
    time.sleep(30)

    while True:
        if CheckCase(d, device_id):
            print("Done")
            break
        else:
            print("Try to re-sign up")
            # Get back to form sign up
            d.click(0.05, 0.063)
            d(resourceId="com.tencent.mm:id/lrn").click()

            if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
                d.app_stop_all()
                break

            time.sleep(5)

            # Verify security
            print("Xac minh bao mat....")
            time.sleep(5)
            d.click(0.491, 0.852)
            print("Xac minh bao mat xong")

            if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
                d.app_stop_all()
                break

            time.sleep(5)

            # Captcha
            print("Capcha")
            d.click(0.244, 0.749)
            time.sleep(30)

        time.sleep(2)

# Connect to devices
devices = [u2.connect(device_id) for device_id in device_ids]

# Process each device
for device_id, d in zip(device_ids, devices):
    process_device(d, device_id)
