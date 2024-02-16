#!/bin/sh

# Copy template files
if [ ! -f pages/.ready ]; then
    cp -rn pages-prebuilt/*.py pages/
fi

# Mark pages are loaded
touch pages/.ready

exec streamlit run 'Home.py' \
    --browser.gatherUsageStats=False \
    --server.address="0.0.0.0" \
    --server.baseUrlPath="/dev/openark/demo/" \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.headless=true \
    --server.port=80
