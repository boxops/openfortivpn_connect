"""
Purpose:
    Use the openfortivpn terminal client to establish a VPN connection and keep it alive.

Requirements:
    - openfortivpn: https://github.com/adrienverge/openfortivpn
    - pyotp: https://pyauth.github.io/pyotp

Usage:
    sudo python3 openfortivpn_connect.py
"""

import subprocess
import pyotp
import time

# Define your configuration here
profile_name = 'config.txt'
host = 'vpn.example.net'
port = 443
username = 'myusername'
password = 'mysecurepassword'
totp_secret = 'mysecuretotpsecret'
trusted_cert = 'abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz123'

def get_totp(secret):
    """Generate TOTP using the provided secret."""
    totp = pyotp.TOTP(secret)
    return totp.now()

def connect(profile_name):
    """Connect to the VPN using the given profile and credentials."""
    command = ['openfortivpn', '-c', profile_name]
    subprocess.run(command)
    # Run the command in the background
    # subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def disconnect():
    """Disconnect from the VPN."""
    command = ['killall', 'openfortivpn']
    subprocess.run(command)

def status():
    """Check the status of the VPN connection."""
    command = ['pgrep', 'openfortivpn']
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return bool(result.stdout)

def generate_config_file(profile_name, host, port, username, password, trusted_cert, totp_secret):
    """Generate a configuration file for the VPN."""
    totp = get_totp(totp_secret)
    lines = [
        f"host = {host}",
        f"port = {port}",
        f"username = {username}",
        f"password = {password}{totp}",
        f"trusted-cert = {trusted_cert}"
    ]
    with open(profile_name, 'w') as f:
        f.write('\n'.join(lines))

# generate_config_file(profile_name, host, port, username, password, trusted_cert, totp_secret)
# connect(profile_name)

# Session drops after x hours, reconnect automatically
while True:
    if not status():
        generate_config_file(profile_name, host, port, username, password, trusted_cert, totp_secret)
        connect(profile_name)
    time.sleep(60)
