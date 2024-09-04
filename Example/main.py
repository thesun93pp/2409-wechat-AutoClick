import sys
import uiautomator2 as u2
import time
from PIL import Image, ImageChops, ImageOps
import pytesseract 


user= 'tuioai2'
password = 'asdaXXX12@eze'
phone = '0859781699'

def SolveCapcha():
    #Take screenshot
    d.screenshot("photos/capcha/capcha.jpg")

def CheckCase():
    #Take screenshot
    d.screenshot("photos/home.jpg")
    # Example usage
    result_1 = pytesseract.image_to_string(Image.open("photos/home.jpg"))

    print("================================================")
    print(result_1)
    print("================================================")

    if "Invite another user to scan" or "Select a Security verification method" in result_1:
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

d = u2.connect() # connect to device
print(d.info)

#Stop all app
d.app_stop_all()


#Mo app Wechat
d.app_start("com.tencent.mm")

#Dang ky bang so dien thoai
d(resourceId="com.tencent.mm:id/mjy").click()

#Dang ky qua so dien thoai
d.xpath('//*[@resource-id="com.tencent.mm:id/avc"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()

#Ten
d(resourceId="com.tencent.mm:id/d98", text="Trần Anh").click()

#Dien Ten
d.send_keys(user, clear=True)

#Dien thoai
d(resourceId="com.tencent.mm:id/d98", text="Nhập số di động").click()

#Dien so dien thoai
d.send_keys(phone, clear=True)

#Mat khau
d(resourceId="com.tencent.mm:id/d98", text="Nhập mật khẩu").click()

#Dien mat khau
d.send_keys(password, clear=True)

#Toi da doc va chap nhan dieu khoan dich vu
d(resourceId="com.tencent.mm:id/lrt").click()

#Chap nhan va tiep tuc
d(resourceId="com.tencent.mm:id/lrn").click()

time.sleep(10)

#Toi da doc va thua nhan chinh sach bao mat
#d.click(0.108, 0.655)
d.click(0.143, 0.742)

time.sleep(5)

#Tiep
d.click(0.484, 0.812)

time.sleep(5)

# Wait for the element to exist before clicking
if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
    print("Spaming Found!")
    d.app_stop_all()
    sys.exit()


#Xac Minh Bao Mat
# Wait for the element to exist before clicking
# Once the element exists, click it
d.click(0.489, 0.847)
time.sleep(5)

#Simple Mode or AI Capcha here
SolveCapcha()

d.click(0.211, 0.787)


time.sleep(30)

#Take screenshot

while True:
    if CheckCase():
        print("Done")
    else:
        print("Try to re sign up")
        #Get back to form sign up
        d.click(0.05, 0.063)
        #Chap nhan va tiep tuc
        d(resourceId="com.tencent.mm:id/lrn").click()

        if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
            d.app_stop_all()
            break

        time.sleep(5)

        #Xac minh bao mat
        print("Xac minh bao mat....")
        time.sleep(5)

        d.click(0.491, 0.852)
        print("Xac minh bao mat xong")

        if d.xpath('//*[@resource-id="com.tencent.mm:id/jlh"]').exists:
            d.app_stop_all()
            break
        
        time.sleep(5)

        #Capcha
        print("Capcha")
        d.click(0.244, 0.749)
        time.sleep(30)

    time.sleep(2)


