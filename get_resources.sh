#!/bin/bash

# Use this script to retrieve any resources you need from HuggingFace, Nexus, etc.
# Large files should all go in a single directory named "resources/"

# TODO: example download nltk

# Example download nexus
nexus_username=""
nexus_password=""
nexus_base_url=""

# "nexus_location" should be the filepath within Nexus (ex. /speechview/asr/embedding/ecapa_tdnn.nemo)
# Edit as required
if [ ! -d resources/model_name ]; then
    python3 download_nexus.py $nexus_base_url $nexus_username $nexus_password "nexus_location" --dest /resources/
fi
