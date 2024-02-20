# Copyright (c) 2024 Ho Kim (ho.kim@ulagbulag.io). All rights reserved.
# Use of this source code is governed by a license
# that can be found in the LICENSE file.

# Configure environment variables
export PYTHON_VERSION := env_var_or_default('ALPINE_VERSION', '3.12-bookworm')
export OCI_IMAGE := env_var_or_default('OCI_IMAGE', 'quay.io/ulagbulag/openark-demo')
export OCI_IMAGE_VERSION := env_var_or_default('OCI_IMAGE_VERSION', 'latest')
export OCI_PLATFORMS := env_var_or_default('OCI_PLATFORMS', 'linux/amd64')

# Configure runtime environment variables
export NATS_ALLOW_DROP := env_var_or_default('NATS_ALLOW_DROP', 'true')

default:
  @just run

clean:
    # Clean up all iPython outputs
    find . -name '*.ipynb' -exec jupyter nbconvert --clear-output --inplace {} \;

run *ARGS:
  streamlit run Home.py \
    --browser.gatherUsageStats=False \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.headless=true \
    --server.port=8501 \
    {{ ARGS }}

oci-build:
  docker buildx build \
    --file './Dockerfile' \
    --tag "${OCI_IMAGE}:${OCI_IMAGE_VERSION}" \
    --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
    --platform "${OCI_PLATFORMS}" \
    --pull \
    --push \
    .

oci-push: oci-build

oci-push-and-update-dash: oci-push
  kubectl -n dash delete pods --selector name=openark-demo
