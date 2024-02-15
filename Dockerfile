# Copyright (c) 2024 Ho Kim (ho.kim@ulagbulag.io). All rights reserved.
# Use of this source code is governed by a GPL-3-style license that can be
# found in the LICENSE file.

# Configure environment variables
ARG PYTHON_VERSION="3.12-bookworm"

# Be ready for serving
FROM "docker.io/library/python:${PYTHON_VERSION}" as server

# Install dependencies
RUN apt-get update && apt-get install -y \
    # Install core dependencies
    findutils \
    # Install build dependencies
    cargo && \
    # Cleanup
    rm -rf /var/lib/apt/lists/*

# Install it as a package
ADD ./ /opt/openark/demo
WORKDIR /opt/openark/demo
RUN pip install -r requirements.txt && \
    # Cleanup
    find /usr -type d -name '*__pycache__' -prune -exec rm -rf {} \;

# Serve
ENTRYPOINT [ "streamlit", "run", "Home.py", "--browser.gatherUsageStats=False", "--server.address=0.0.0.0", "--server.baseUrlPath=/dev/openark/demo/", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.headless=true", "--server.port=80" ]
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
