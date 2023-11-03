#!/bin/bash

if pip3 show unidecode > /dev/null 2>&1; then
    echo "unidecode is already installed."
else
    # If not installed, install it
    pip3 install unidecode
    echo "unidecode installed."
fi