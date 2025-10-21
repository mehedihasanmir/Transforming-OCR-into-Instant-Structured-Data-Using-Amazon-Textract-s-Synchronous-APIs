import os 
import boto3
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")

if not all([aws_access_key,aws_secret_key, aws_region]):
    raise Exception("AWS credentials or region not loaded from .env file")

#textract client 
textract = boto3.client(
    "textract",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

pdf_file = "sample.pdf"

# read pdf bytes
with open(pdf_file, "rb") as file:
    pdf_bytes = file.read()

response = textract.detect_document_text(Document={"Bytes": pdf_bytes})

# Extract text from file
lines = []
for block in response["Blocks"]:
    if block["BlockType"] == "LINE":
        lines.append(block["Text"])
        
# Save file in output.txt
with open("output1.txt", "w", encoding ="utf-8") as f:
    f.write("\n".join(lines))

print("Text extration complete and saved to output1.txt")