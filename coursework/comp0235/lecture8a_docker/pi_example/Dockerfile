FROM almalinux:10-kitten

# Update packages
RUN dnf install -y epel-release && /usr/bin/crb enable && dnf update -y

# Some basic deps
RUN dnf install -y wget

# Get the Python code
RUN wget https://raw.githubusercontent.com/owainkenwayucl/coursework-c0235/refs/heads/main/lecture8a_docker/pi_example/pi.py

# Run it.
CMD ["python3", "pi.py"]

