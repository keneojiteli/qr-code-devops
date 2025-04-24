from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware #allows fe to connect to be even on diff domains
import qrcode #library to generate QR codes
import boto3 #aws sdk for python
import os #to access environment variables (like AWS keys) and work with file paths
from io import BytesIO #holds image data in memory, like a temporary file

# Loading Environment variable (AWS Access Key and Secret Key) from a .env file
from dotenv import load_dotenv 
load_dotenv()

app = FastAPI() #create a FastAPI instance

# Allowing CORS for local testing
origins = [
    # "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS S3 Configuration, connects to s3 with config from .env
s3 = boto3.client(
    's3',
    aws_access_key_id= os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key= os.getenv("AWS_SECRET_KEY"))

bucket_name = 'qr-code-bucket-17-04-25' # Add your bucket name here

@app.post("/generate-qr/")
async def generate_qr(url: str):
    # Generate QR Code and setup its config
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate file name for S3
    file_name = f"qr_codes/{url.split('//')[-1]}.png"

    try:
        # Upload to S3
        # s3.put_object(Bucket=bucket_name, Key=file_name, Body=img_byte_arr, ContentType='image/png', ACL='public-read')
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=img_byte_arr, ContentType='image/png')
        
        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return {"qr_code_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    