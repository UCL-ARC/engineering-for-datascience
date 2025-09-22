# Base this image on current Julia install
FROM julia:latest

# Install dependencies - git
RUN apt-get update && apt-get install -y git

# Clone repo from git
RUN git clone https://github.com/owainkenwayucl/JuliaML

# Data mountpoint
RUN mkdir -p /data

# Install Flux.jl + deps
WORKDIR "/JuliaML/Fashion"
RUN bash setup.sh

# Agree to terms for FashionMNIST dataset.
ENV DATADEPS_ALWAYS_ACCEPT=true

# Create entrypoint script
COPY --chmod=755 <<EOF /entrypoint.sh
#!/bin/bash
julia --project="/JuliaML/Fashion" improved.jl && cp *.bson /data
EOF

# Run it.
ENTRYPOINT ["/entrypoint.sh"]
