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

# Data
data = [
    {'user': 'MrLol111', 'password': 'MrLol111@ez', 'phone': '0859181111', 'adb': ''},
    {'user': 'MrLol222', 'password': 'MrLol222@ez', 'phone': '0869182211', 'adb': ''},
    {'user': 'MrLol333', 'password': 'MrLol333@ez', 'phone': '0879183311', 'adb': ''},
    {'user': 'MrLol444', 'password': 'MrLol444@ez', 'phone': '0889184411', 'adb': ''},
    {'user': 'MrLol555', 'password': 'MrLol555@ez', 'phone': '0899185511', 'adb': ''}
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

@app.route('/activate', methods=['POST'])
def activate_device():
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

if __name__ == '__main__':
    # Start the Flask server
    def run_flask():
        app.run(debug=True, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Open index.html in the default web browser
    webbrowser.open(f'http://127.0.0.1:5000/')
