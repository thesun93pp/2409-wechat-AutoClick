from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.action_chains import ActionChains

# Create Appium Options
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app_package = 'com.ldmnq.launcher3'
options.app_activity = 'com.android.launcher3.Launcher'

# Initialize WebDriver
driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
driver.implicitly_wait(30)

try:
    # Click on the element using XPath
    search_input_view = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//android.widget.FrameLayout[@content-desc="Thư mục: System Apps"]/android.widget.ImageView'))
    ).click()

    # Click on the search bar
    search_bar = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@content-desc="Cài đặt"]'))
    ).click()

    # Locate the input field
    input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.view.ViewGroup'))
    ).click()

    
    ActionChains(driver).send_keys('Fat gay').perform()

    # Another way to send keys if set_value doesn't work
    # input_field.send_keys("Fat gay")

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    driver.quit()



# desired_cap = {
#     "uuid": "emulator-5554", 
#     "platformName": "Android", 
#     "appPackage": "com.ldmnq.launcher3", 
#     "appActivity": "com.android.launcher3.Launcher"
# }