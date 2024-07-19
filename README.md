# doc-analysis
## Setup
- make virtual environment
- clone git repo
- pip install -r requirements.txt
- create .env file with env variables S3_BUCKET_URL (required) and TEXTRACT_ADAPTER_ID (optional)

## Run
### Run Streamlit Demo
- cd into src folder
- run `streamlit run main.py`
### Run tools.py
- cd into src folder
- run `python tools.py --adapter=False --filename=myfilename.pdf`