FROM pytorch/pytorch:latest

# Set the working directory in the container
WORKDIR /stablediffusion

RUN apt-get update && apt-get install -y git

# Clone the diffusers repo and install it
RUN git clone https://github.com/wenyDev/diffusers.git && \
    cd diffusers && \
    pip install -e . && \
    python3 setup.py install

# Install additional dependencies
RUN pip install torchvision transformers accelerate scipy safetensors datasets

# Copy the Python script to the working directory
COPY diffuser.py .

# Run the Python script when the container starts
CMD ["python", "diffuser.py"]
