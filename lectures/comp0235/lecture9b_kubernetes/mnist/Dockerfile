FROM docker.io/library/almalinux:10

# Update packages
RUN dnf install -y epel-release && /usr/bin/crb enable && dnf update -y 

# Set up python
RUN dnf install -y python3-pip python3-devel

# Make directory
RUN mkdir /mnist
WORKDIR /mnist

# Copy in our python files
COPY *.py /mnist/

# Install Pytorch
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
RUN pip3 install tqdm onnx onnxruntime onnxscript numpy

# Command to run
CMD ["python3", "training.py"]
