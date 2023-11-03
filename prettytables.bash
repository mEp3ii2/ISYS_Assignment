#!/bin/bash

if pip3 show prettytable > /dev/null 2>&1; then
    echo "prettyTables is already installed."
else
    # If not installed, install it
    pip3 install prettytable
    echo "prettyTables installed."
fi