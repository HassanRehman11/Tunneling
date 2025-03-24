import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to write the content to a file
def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File created: {file_path}")
    except Exception as e:
        print(f"Error creating file {file_path}: {e}")
        exit(1)

# Function to reload systemd and enable the service and timer
def enable_and_start_service():
    try:
        # Reload systemd daemon to recognize the new service and timer
        subprocess.run(['/usr/bin/sudo', 'chmod', '600', '/home/pi/Work/dahuatunnel.pem'], check=True)
        subprocess.run(['/usr/bin/sudo', 'chmod', '777', '/home/pi/Work/start.sh'], check=True)
        subprocess.run(['/usr/bin/sudo', 'chmod', '+x', '/home/pi/Work/start.sh'], check=True)
        subprocess.run(['/usr/bin/sudo', 'systemctl', 'stop', 'start_forwarding.service'], check=True)
        subprocess.run(['/usr/bin/sudo', 'systemctl', 'daemon-reload'], check=True)

        # Enable and start the service and timer
        subprocess.run(['/usr/bin/sudo', 'systemctl', 'enable', 'start_forwarding.service'], check=True)
        subprocess.run(['/usr/bin/sudo', 'systemctl', 'start', 'start_forwarding.service'], check=True)
        print("Service and timer enabled and started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running systemd command: {e}")
        exit(1)

# Main function to create the service, timer and run the necessary commands
def run(camera_ip, port_forward, server_ip):
    ssh_command = f'ssh -NT -o ServerAliveInterval=60 -o ServerAliveCountMax=10 -o ExitOnForwardFailure=yes -R {port_forward}:{camera_ip}:80 -i /home/pi/Work/dahuatunnel.pem ubuntu@{server_ip}'
    # Define paths for the service and timer files
    service_file_path = '/etc/systemd/system/start_forwarding.service'
    service_bash_file_path = '/home/pi/Work/start.sh'
    # Define the SSH tunnel command and necessary details
    # Create the systemd service file
    service_bash = f'''
#!/bin/bash
while true
do
    echo "Connecting new tunnel"
    {ssh_command}
    echo "Reconnection [+]"
    sleep 1
done
'''
    write_to_file(service_bash_file_path, service_bash)
    service_content = f"""Description=SSH Tunnel for WebStation
After=network.target

[Service]
Restart=always
RestartSec=1
User=pi
WorkingDirectory=/home/pi/Work
ExecStart=/bin/bash -c /home/pi/Work/start.sh
[Install]
WantedBy=multi-user.target
    """
    # Create service and timer files
    write_to_file(service_file_path, service_content)

    # Enable and start the service and timer
    enable_and_start_service()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        camera_ip = request.form.get('camera_ip')
        port = request.form.get('port')
        server_ip = request.form.get('server_ip')

        # Process the data (e.g., configure port forwarding)
        response = f"Port {port} forwarded for camera IP {camera_ip}"
        run(camera_ip, port, server_ip)
        print(response, flush=True)

        return jsonify({"message": response})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
