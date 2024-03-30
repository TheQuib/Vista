#!/bin/bash

# Initialize variables
GATEWAY_IP=""
LOG_FILE="~/skystat.log"

# Function to get the default gateway IP
get_gateway_ip() {
    GATEWAY_IP=$(ip route | grep default | awk '{print $3}')
}

# First attempt to get the gateway IP
get_gateway_ip

# Wait until a default gateway is set
while [ -z "$GATEWAY_IP" ]; do
    echo "No default gateway found. Waiting for network connection..."
    sleep 5
    get_gateway_ip  # Try to get the gateway IP again
done

echo "Default gateway found: $GATEWAY_IP. Checking network connectivity..."

# Now, wait for the network to become available by pinging the gateway
while ! ping -c 1 -W 1 $GATEWAY_IP > /dev/null; do
    echo "Waiting for network to become available..."
    sleep 5
done

echo "Network is up. Executing main.py."
/usr/bin/python3 /opt/skystat/main.py >> $LOG_FILE 2>&1
