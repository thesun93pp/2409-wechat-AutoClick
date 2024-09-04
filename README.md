# Mobile Testing Automation - AutoX

pip install -U uiautomator2

pip install -U weditor

pip install pytesseract Pillow

install [Download and install Tesseract from here.](https://github.com/UB-Mannheim/tesseract/wiki)

After installation, you will need to add the Tesseract installation path to your system’s PATH environment variable. Typically, the installation path is:

C:\Program Files\Tesseract-OCR\

## Connect multi devices!
```sh
    # Device IDs (replace with actual IDs if needed)
    device_ids = ['device_id_1', 'device_id_2']  # Replace with your actual device IDs

    # Connect to devices
    devices = [u2.connect(device_id) for device_id in device_ids]
```
## List Connected Devices!
```sh
    adb devices
```