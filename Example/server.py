import time
import requests
from flask import Flask, jsonify, request, send_from_directory
import subprocess
from flask_cors import CORS
import threading
import os
import webbrowser
import json
import sys

app = Flask(__name__)
CORS(app)

# Set the path to the directory containing index.html and data.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE_PATH = os.path.join(BASE_DIR, 'index.html')
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data.json')

# Function to detect if the app is bundled by PyInstaller
def resource_path(relative_path):
    # If the app is bundled with PyInstaller, adjust the path accordingly
    if getattr(sys, 'frozen', False):  # Check if bundled with PyInstaller
        base_path = sys._MEIPASS  # Temporary folder created by PyInstaller
    else:
        base_path = os.path.abspath(".")  # Base directory in normal run
    return os.path.join(base_path, relative_path)


# Load data from data.json
def load_data():
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return []

# Save updated data back to data.json
def save_data(data):
    try:
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving JSON data: {e}")

# Load data initially
data = load_data()

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
    # Reload data to get the latest changes
    data = load_data()
    for device in data:
        if device['adb'] == device_id:
            return device
    return None

def update_device_adb_with_empty_entry(device_id):
    # Reload data to get the latest changes
    data = load_data()
    
    # Find the first device with an empty adb field and update it
    for device in data:
        if device['adb'] == '':
            device['adb'] = device_id
            save_data(data)  # Save the changes back to JSON
            print(f"Device {device['user']} updated with adb: {device_id}")
            return device  # Return the updated device data
    return None

@app.route('/api/data', methods=['GET'])
def get_data():
    # Reload data to ensure it's always up-to-date
    data = load_data()
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
    # Reload data to ensure it's always up-to-date
    data = load_data()
    success_devices = [device for device in data if device['state'] == 'success']
    return jsonify(success_devices)

@app.route('/api/success', methods=['POST'])
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

    # Save the updated data
    save_data(load_data())

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
