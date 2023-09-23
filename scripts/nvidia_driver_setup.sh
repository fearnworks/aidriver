#!/bin/bash

cd ./scripts
git clone https://github.com/Scotchman0/NVIDIA_Drivers/
sudo ./NVIDIA_Drivers/NVIDIA_drivers.sh
sudo ./NVIDIA_Drivers/docker_gpu_setup.sh
cd ..
