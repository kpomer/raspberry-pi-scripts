#!/bin/bash

# Reload Systemd Manager Config and Restart the flask-api service (raspberry-pi-scripts/api)
# Run this after any code or configuration changes

sudo systemctl daemon-reload
sudo systemctl restart flask-api.service