#!/bin/bash
set -e

TARGET=/opt/smartkip/shutdown

echo "Creating target directory..."
sudo mkdir -p $TARGET

echo "Copying shutdown server..."
sudo cp shutdown_server.py $TARGET/
sudo chmod +x $TARGET/shutdown_server.py

echo "Installing systemd service..."
sudo cp shutdown-server.service /etc/systemd/system/shutdown-server.service

echo "Reloading systemd..."
sudo systemctl daemon-reload

echo "Enabling and starting service..."
sudo systemctl enable shutdown-server
sudo systemctl restart shutdown-server

echo "Adding sudoers rule..."
sudo bash -c 'echo "pi ALL=NOPASSWD: /sbin/shutdown" >/etc/sudoers.d/smartkip_shutdown'

echo "Done."