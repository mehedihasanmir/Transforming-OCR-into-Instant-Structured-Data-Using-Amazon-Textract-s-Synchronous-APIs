import boto3
import json
import os
from dotenv import load_dotenv

# Load AWS credentials from .env file
load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

# Initialize Textract client
textract = boto3.client(
    'textract',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

def analyze_invoice_queries_local(file_path, output_file="output4.json"):
    # Read file as bytes (no S3 needed)
    with open(file_path, "rb") as document:
        image_bytes = document.read()

    # Run Textract Query-based analysis
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['QUERIES'],
        QueriesConfig={
            "Queries": [
                {"Text": "What is the invoice date?", "Alias": "InvoiceDate"},
                {"Text": "What is the total amount?", "Alias": "TotalAmount"},
                {"Text": "What is the vendor name?", "Alias": "VendorName"}
            ]
        }
    )

    extracted_data = {}

    print("\n=== Extracted Invoice Fields ===")
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'QUERY_RESULT':
            alias = block.get('Query', {}).get('Alias', 'Unknown')
            answer = block.get('Text', '')
            confidence = block.get('Confidence', 0)
            extracted_data[alias] = {
                "Answer": answer,
                "Confidence": confidence
            }
            print(f"{alias}: {answer} (Confidence: {confidence:.1f}%)")

    # Save results to output4.json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"\nExtracted data saved to {output_file}")

# Example usage
analyze_invoice_queries_local("invoice.png")
