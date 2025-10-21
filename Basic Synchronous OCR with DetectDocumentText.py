import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Textract client
textract = boto3.client(
    'textract',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def extract_text_from_local_file(file_path):
    """Extracts text from a local image or PDF file using Textract."""
    with open(file_path, 'rb') as document:
        image_bytes = document.read()

    # Call Textract API
    response = textract.detect_document_text(Document={'Bytes': image_bytes})

    print("=== Extracted Text ===\n")
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print(item["Text"])

if __name__ == "__main__":
    file_path = "sample.pdf"  # Change to your file name
    extract_text_from_local_file(file_path)
