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

def list_devices():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = result.stdout.splitlines()[1:]  # Skip the first line
        devices = [line.split()[0] for line in devices if line.strip()]
        return devices
    except Exception as e:
        print(f"Error listing devices: {e}")
        return []

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
        return jsonify({"success": False, "message": "No device ID provided!"})

    # Respond with success immediately
    response = jsonify({"success": True})
    
    # Run the script asynchronously
    def run_script():
        try:
            result = subprocess.run(['python', 'main.py', device_id], capture_output=True, text=True)
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"Error running script: {e}")
    
    # Use threading to run the script asynchronously
    import threading
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
