#/bin/bash

# Check if input data directory exists
if [ ! -d "/workspaces/ocr_extract_nps_tables/data/input" ]; then

    # Create input data directory
    mkdir -p /workspaces/ocr_extract_nps_tables/data/input

    # Download the data, shared as public links from Google Cloud Storage Bucket
    echo "Downloading input data..."
    wget -O /workspaces/ocr_extract_nps_tables/data/input/Appendix_A_JOTR_Vegetation_Descriptions_2012.pdf https://storage.googleapis.com/ecotech_dev_demo/Appendix_A_JOTR_Vegetation_Descriptions_2012.pdf
    wget -O /workspaces/ocr_extract_nps_tables/data/input/table_mapping.json https://storage.googleapis.com/ecotech_dev_demo/table_mapping.json

fi

