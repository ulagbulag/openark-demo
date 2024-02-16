# Copyright (c) 2024 Ho Kim (ho.kim@ulagbulag.io). All rights reserved.
# Use of this source code is governed by a GPL-3-style license that can be
# found in the LICENSE file.

# Configure environment variables
ARG PYTHON_VERSION="3.12-bookworm"

# Be ready for serving
FROM "docker.io/library/python:${PYTHON_VERSION}" as server

# Configure server
CMD [ "./run.sh" ]
ENTRYPOINT [ "/usr/bin/env" ]
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Install dependencies
RUN apt-get update && apt-get install -y \
    # Install core dependencies
    findutils \
    python3-opencv \
    # Install build dependencies
    cargo && \
    # Cleanup
    rm -rf /var/lib/apt/lists/*

# Install it as a package
ADD ./requirements.txt /opt/openark/demo/requirements.txt
WORKDIR /opt/openark/demo
RUN pip install -r requirements.txt && \
    # Cleanup
    find /usr -type d -name '*__pycache__' -prune -exec rm -rf {} \;

# Add files (ordered by least updates)
ADD ./LICENSE /opt/openark/demo/
ADD ./run.sh /opt/openark/demo/
ADD ./README.md /opt/openark/demo/
ADD ./utils /opt/openark/demo/utils
ADD ./Home.py /opt/openark/demo/
ADD ./pages /opt/openark/demo/pages-prebuilt
VOLUME /opt/openark/demo/pages
