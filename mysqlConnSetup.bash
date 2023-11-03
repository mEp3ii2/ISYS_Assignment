#!/bin/bash

# Check if mysql-connector-python is installed
if pip3 show mysql-connector-python > /dev/null 2>&1; then
    echo "mysql-connector-python is already installed."
else
    # If not installed, install it
    pip3 install mysql-connector-python==8.0.5  # Use the desired version
    echo "mysql-connector-python installed."
fi

