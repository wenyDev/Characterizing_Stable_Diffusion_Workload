# Stable Diffusion Docker Setup
This guide provides instructions on how to set up and run Stable Diffusion using Docker. Ensure you have Docker installed on your system to proceed with the setup.

# Getting Started
Prerequisites   
Docker must be installed on your machine. If Docker is not already installed, you can download and install it from Docker's official website.

Installation  
1. Clone the repository
First, clone the repository to your local machine using the following command:
```
git clone https://github.com/wenyDev/Characterizing_Stable_Diffusion_Workload.git
cd Characterizing_Stable_Diffusion_Workload
```

2. Build the Docker Image  
Build the Docker image by running:
```
sudo docker build -t stable-diffusion .
```
This command creates a Docker image named stable-diffusion from the Dockerfile located in the current directory.

# Usage
Run the Application  
To run Stable Diffusion inside a Docker container, execute:
```
docker run --name stable-diffusion -v /YOUR/PATH:/stablediffusion -e NUM_PROMPTS=10 stable-diffusion
```
Here's what each part of this command does:

--name stable-diffusion assigns the name stable-diffusion to your Docker container.  
-v /YOUR/PATH:/stablediffusion mounts the directory /YOUR/PATH from your host to /stablediffusion inside the Docker container. 
-e NUM_PROMPTS=10 sets the environment variable NUM_PROMPTS with the value 10, which can be adjusted based on how many prompts you want to process.  
test
[Open in Colab](https://colab.research.google.com/drive/19zZqunRLepQalh7REmbcu7dlfxJ4yVL0?usp=sharing)
