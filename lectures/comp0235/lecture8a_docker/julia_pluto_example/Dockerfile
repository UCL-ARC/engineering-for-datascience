# Base this image on current Julia install
FROM julia:latest

# Install dependencies - git
RUN apt-get update && apt-get install -y git

# Data mountpoint
RUN mkdir -p /data

RUN mkdir -p pluto_runtime

# Install Flux.jl + deps
WORKDIR "/pluto_runtime"
RUN julia -e "using Pkg; Pkg.update(); Pkg.add(\"Pluto\")"

# Agree to terms for FashionMNIST dataset.
ENV DATADEPS_ALWAYS_ACCEPT=true

# Run it.
CMD cd /data && julia -e "using Pluto; Pluto.run(port=2023)"
