import time
import requests
from flask import Flask, jsonify, request, send_from_directory
import subprocess
from flask_cors import CORS
import threading
import os
import webbrowser

app = Flask(__name__)
CORS(app)

# Set the path to the directory containing index.html
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE_PATH = os.path.join(BASE_DIR, 'index.html')

#Device sign up successfully
data =[
    {}
]

# Data
data = [
    {'user': 'AKSIOD_H20', 'password': 'AKSIOD_H20@new', 'phone': '0855324420', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H21', 'password': 'AKSIOD_H21@new', 'phone': '0855324421', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H22', 'password': 'AKSIOD_H22@new', 'phone': '0859324422', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H23', 'password': 'AKSIOD_H23@new', 'phone': '0858324423', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H24', 'password': 'AKSIOD_H24@new', 'phone': '0857324424', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H25', 'password': 'AKSIOD_H25@new', 'phone': '0856324425', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H26', 'password': 'AKSIOD_H26@new', 'phone': '0857324426', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H27', 'password': 'AKSIOD_H27@new', 'phone': '0858324427', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H28', 'password': 'AKSIOD_H28@new', 'phone': '0859324428', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H29', 'password': 'AKSIOD_H29@new', 'phone': '0856324429', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H30', 'password': 'AKSIOD_H30@new', 'phone': '0855324430', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H31', 'password': 'AKSIOD_H31@new', 'phone': '0855324431', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H32', 'password': 'AKSIOD_H32@new', 'phone': '0859324432', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H33', 'password': 'AKSIOD_H33@new', 'phone': '0858324433', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H34', 'password': 'AKSIOD_H34@new', 'phone': '0857324434', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H35', 'password': 'AKSIOD_H35@new', 'phone': '0856324435', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H36', 'password': 'AKSIOD_H36@new', 'phone': '0857324436', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H37', 'password': 'AKSIOD_H37@new', 'phone': '0858324437', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H38', 'password': 'AKSIOD_H38@new', 'phone': '0859324438', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H39', 'password': 'AKSIOD_H39@new', 'phone': '0856324439', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H40', 'password': 'AKSIOD_H40@new', 'phone': '0855324440', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H41', 'password': 'AKSIOD_H41@new', 'phone': '0855324441', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H42', 'password': 'AKSIOD_H42@new', 'phone': '0859324442', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H43', 'password': 'AKSIOD_H43@new', 'phone': '0858324443', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H44', 'password': 'AKSIOD_H44@new', 'phone': '0857324444', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H45', 'password': 'AKSIOD_H45@new', 'phone': '0856324445', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H46', 'password': 'AKSIOD_H46@new', 'phone': '0857324446', 'adb': '', 'state' : ''},
    {'user': 'AKSIOD_H47', 'password': 'AKSIOD_H47@new', 'phone': '0858324447', 'adb': '', 'state' : ''}
]

def list_devices():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = result.stdout.splitlines()[1:]  # Skip the first line
        devices = [line.split()[0] for line in devices if line.strip()]
        return devices
    except Exception as e:
        print(f"Error listing devices: {e}")
        return []

def get_device_data(device_id):
    for device in data:
        if device['adb'] == device_id:
            return device
    return None

def update_device_adb_with_empty_entry(device_id):
    # Find the first device with an empty adb field and update it
    for device in data:
        if device['adb'] == '':
            device['adb'] = device_id
            print(f"Device {device['user']} updated with adb: {device_id}")
            return device  # Return the updated device data
    return None

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    devices = list_devices()
    return jsonify([{'id': device, 'name': device} for device in devices])

@app.route('/api/connect', methods=['POST'])
def connect_device():
    data = request.json
    device_id = data.get('deviceId')
    if device_id:
        # Perform device connection logic here (if needed)
        return jsonify({'message': f'Device {device_id} connected successfully!'})
    return jsonify({'message': 'No device ID provided!'}), 400

@app.route('/api/devices/success', methods=['GET'])
def get_success_devices():
    success_devices = [device for device in data if device['state'] == 'success']
    return jsonify(success_devices)

@app.route('/api/sucess', methods=['POST'])
def update_device_state():
    # Get the device ID from the request
    device_id = request.json.get('device_id')
    
    if not device_id:
        return jsonify({"success": False, "message": "No device ID provided!"}), 400

    # Find the device in the data
    device_data = get_device_data(device_id)

    if not device_data:
        return jsonify({"success": False, "message": f"No device found with ID: {device_id}!"}), 404

    # Update the state to 'success'
    device_data['state'] = 'success'

    return jsonify({"success": True, "message": f"Device {device_id} state updated to 'success'!"})


@app.route('/activate', methods=['POST'])
def activate_device(device_id=None):  # Add device_id as a parameter
    if not device_id:
        device_id = request.json.get('device_id')

    if not device_id:
        return jsonify({"success": False, "message": "No device ID provided!"}), 400

    # Update the device adb
    device_data = update_device_adb_with_empty_entry(device_id)

    if not device_data:
        return jsonify({"success": False, "message": "No available device slot found!"}), 400

    # Extract user, password, and phone from the updated device data
    user = device_data['user']
    password = device_data['password']
    phone = device_data['phone']

    # Respond with success immediately
    response = jsonify({"success": True, "message": f"Device {device_id} activation started."})

    # Run the script asynchronously
    def run_script():
        try:
            result = subprocess.run(['python', 'main.py', device_id, user, password, phone], capture_output=True, text=True)
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"Error running script: {e}")

    # Use threading to run the script asynchronously
    thread = threading.Thread(target=run_script)
    thread.start()

    return response

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

def fetch_devices():
    try:
        response = requests.get('http://127.0.0.1:5000/api/devices')
        response.raise_for_status()
        return response.json()  # Assuming the response is a list of devices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching devices: {e}")
        return []

# def enable_usb_debugging(device_id):
#     try:
#         # Enable Developer Options
#         subprocess.run(['adb', '-s', device_id, 'shell', 'su', '-c', 'settings put global development_settings_enabled 1'], check=True)
        
#         # Enable USB Debugging
#         subprocess.run(['adb', '-s', device_id, 'shell', 'su', '-c', 'settings put global adb_enabled 1'], check=True)

#         print(f"USB debugging enabled on device {device_id}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error enabling USB debugging on device {device_id}: {e}")

def check_for_new_devices():
    global seen_devices
    devices = fetch_devices()
    current_device_ids = {device['id'] for device in devices}

    # Find new devices that haven't been seen before
    new_devices = current_device_ids - seen_devices

    # Activate new devices
    for device_id in new_devices:
        print(f"New device found: {device_id}")
        time.sleep(15)  # Wait 15 seconds

        # Activate the device within the Flask app context
        with app.app_context():
            activate_device(device_id)  # Activate the device

    # Update the seen_devices set
    seen_devices.update(current_device_ids)

if __name__ == '__main__':
    # Start the Flask server
    def run_flask():
        app.run(debug=True, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Open index.html in the default web browser
    webbrowser.open(f'http://127.0.0.1:5000/')

    # Initial fetch to populate seen devices
    seen_devices = {device['id'] for device in fetch_devices()}

    # Polling loop
    while True:
        check_for_new_devices()
        time.sleep(10)  # Check every 10 seconds (adjust as needed)
