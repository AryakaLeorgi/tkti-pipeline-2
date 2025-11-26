FROM openjdk:11-slim

# Install Ant
RUN apt-get update && \
    apt-get install -y ant python3 python3-pip && \
    apt-get clean

# Workspace where Jenkins mounts repo
WORKDIR /workspace

# Optional: install python tools for sandbox
COPY requirements-sandbox.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt || true

# The runner script is invoked by Jenkins
CMD ["python3", "/workspace/src/sandbox/runner.py"]
