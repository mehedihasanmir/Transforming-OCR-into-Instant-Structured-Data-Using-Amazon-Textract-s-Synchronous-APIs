import boto3
import os
from dotenv import load_dotenv

load_dotenv()

textract = boto3.client(
    'textract',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

file_path = "sample.png"

with open(file_path, 'rb') as document:
    image_bytes = document.read()

response = textract.detect_document_text(Document={'Bytes': image_bytes})

#Extract text from image and document
texts = []
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        texts.append(item["Text"])
        
with open("Output2.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(texts))

print("Text extraction complete and saved to Output2.txt")