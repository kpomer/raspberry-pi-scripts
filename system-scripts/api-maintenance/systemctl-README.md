# Raspberry Pi API Scripts

The API code is stored in the `raspberry-pi-scripts/api` directory. I'm using a Gunicorn Python WSGI HTTP Server to run a Flask Web Application

See scripts below to manage and edit the service:

### Systemctl Commands

- Reload Systemd Manager Config and Restart Service. Run this after any code or configuration changes by executing the `api-reload-restart.sh` script in this directory

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl restart flask-api.service
  ```

- Start the service

  ```bash
  sudo systemctl start flask-api.service
  ```

- Immediately stop the service

  ```bash
  sudo systemctl stop flask-api.service
  ```

- Restarts the service by safely stopping and starting back up

  ```bash
  sudo systemctl restart flask-api.service
  ```

- Checks the current status of the service, including whether it's running and recent log messages

  ```bash
  sudo systemctl status flask-api.service
  ```

- Enables the service to start automatically on boot

  ```bash
  sudo systemctl enable flask-api.service
  ```

- Prevents the service from starting automatically on boot

  ```bash
  sudo systemctl disable flask-api.service
  ```

### Log Commands

- Snapshot of the most recent few log entries

  ```bash
  systemctl status
  ```

- Shows the complete log history for your service. The `-r` flag tells it to return in reverse to see the most recent logs at the top, but it can be excluded to see it from oldest to newest

  ```bash
  journalctl -u flask-api.service -r
  ```

- Follow logs in realtime (useful for debugging)

  ```bash
  journalctl -u flask-api.service -f
  ```

### Editing Service Configuration

- Edit systemd service configuration

  ```bash
  sudo nano /etc/systemd/system/flask-api.service
  ```

  - The ExecStart line can be modified by adding flags like `--log-level debug` for more descriptive journalctl logging, or `--timeout 60` to explicitly set the timeout duration. These changes would be added just before the `app:app` text
