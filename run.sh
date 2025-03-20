#!/bin/bash

SERVICE_NAME="my_service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
SCRIPT_FILE="/usr/local/bin/my_script.sh"

# Create a simple script to run
echo -e "#!/bin/bash\nwhile true; do echo \"Service Running...\"; sleep 10; done" > $SCRIPT_FILE
chmod +x $SCRIPT_FILE

# Create systemd service file
cat <<EOF > $SERVICE_FILE
[Unit]
Description=My Custom Service
After=network.target

[Service]
ExecStart=$SCRIPT_FILE
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the service
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo "Service $SERVICE_NAME has been created and started successfully!"
