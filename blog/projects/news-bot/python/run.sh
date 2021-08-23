#!/bin/bash

# Running with google
# poetry run python newsbot.py fetch \
#   --type "sr_google" \
#   --news-apikey "${NEWS_API_KEY}" \
#   --ibm-username "${IBM_USERNAME}" \
#   --ibm-password "${IBM_PASSWORD}" \
#   --ibm-apikey "${IBM_API_KEY}"

poetry run python newsbot.py fetch \
  --type "ws_watson" \
  --news-apikey "${NEWS_API_KEY}" \
  --ibm-username "${IBM_USERNAME}" \
  --ibm-password "${IBM_PASSWORD}" \
  --ibm-apikey "${IBM_API_KEY}" \
  --ibm-apiurl "${IBM_API_URL}"