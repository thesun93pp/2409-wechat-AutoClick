from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
import time
import os


#Xpath
app = '//android.widget.TextView[@content-desc="WeChat"]'
btn_signup = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.Button[2]'

# Create Appium Options
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app_package = 'com.ldmnq.launcher3'
options.app_activity = 'com.android.launcher3.Launcher'

# Initialize WebDriver
driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
# driver.implicitly_wait(30)

# Create an instance of TouchAction
touch_action = TouchAction(driver)
time_wait = 30

try:

    # Open WeChat app
    print('Opening WeChat app')
    wechat_app = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, app))
    ).click()
    
    print('Opened WeChat successfully')
    
    # Find and click Sign Up button
    print('Finding Sign Up button')

    time.sleep(5)
    
    # Perform a tap action at the fixed position
    touch_action.tap(x=442, y=880).perform()
    # wechat_app_sign_up_btn = WebDriverWait(driver, time_wait).until(
    #     EC.visibility_of_element_located((By.XPATH, btn_signup))
    # ).click()
    
    print('Clicked Sign Up button successfully')

    # Find and click on phone number field
    print('Finding phone number field')
    wechat_app_sign_up_btn_phone_number = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout'))
    ).click()

    #Fill data to form sign up

     # Fill username
    print('Filling username')
    username_form_sign_up = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.EditText'))
    ).click()

    ActionChains(driver).send_keys('Testing001').perform()
    
    # Fill phone number
    print('Filling phone number')
    phonenumber_form_sign_up = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.EditText'))
    ).click()
    
    ActionChains(driver).send_keys('0859181635').perform()

    # Fill password
    print('Filling password')
    password_form_sign_up = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.EditText'))
    ).click()
    ActionChains(driver).send_keys('password').perform()

    # Approve policy
    print('Approving policy')
    approve_policy_form_sign_up = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, '//android.widget.CheckBox[@content-desc="Chấp nhận "]'))
    ).click()

    # Accept and continue
    print('Accepting and continuing')
    accept_continue_form_sign_up = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button'))
    ).click()

    # Accept Policy Detail
    print('Accepting policy detail')
    time.sleep(5)
    touch_action.tap(x=53, y=619).perform()

    # accept_checkbox_policy_form_sign_up = WebDriverWait(driver, time_wait).until(
    #     EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View'))
    # ).click()

    #Continue and next
    print('Finding')
    time.sleep(5)
    touch_action.tap(x=263, y=760).perform()
    # accept_continue_submit_form_sign_up = WebDriverWait(driver, time_wait).until(
    #     EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.widget.Button'))
    # ).click()


    #Verify
    print('Accepting policy detail')
    time.sleep(5)
    touch_action.tap(x=263, y=760).perform()
    
    # Check if the directory exists, and create it if it doesn't
    img_dir = "img"
    if not os.path.exists(img_dir): 
        os.makedirs(img_dir)

    # Define the screenshot path
    screenshot_path = os.path.join(img_dir, "screenshot.png")

    #Verify
    print('Accepting policy detail')
    time.sleep(5)
    touch_action.tap(x=38, y=500).perform()


except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    driver.quit()

desired_cap = {
    "uuid": "emulator-5554", 
    "platformName": "Android", 
    "appPackage": "com.ldmnq.launcher3", 
    "appActivity": "com.android.launcher3.Launcher"
}
