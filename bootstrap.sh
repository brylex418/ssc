#!/bin/bash

echo "Installing pip"

sudo apt update -y
sudo apt install -y python3-pip

echo "Installing some python packages"

sudo apt install -y python3-paramiko

echo "Setting up SSC tool"

alias ssc="python3 src/allthings.py"
