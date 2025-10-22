import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Textract client
textract = boto3.client(
    'textract',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def analyze_invoice_queries_local(file_path, output_file):
    # Read the local invoice file
    with open(file_path, 'rb') as document:
        image_bytes = document.read()

    # Call Textract with Queries
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['QUERIES'],
        QueriesConfig={
            "Queries": [
                {"Text": "What is the invoice date?", "Alias": "InvoiceDate"},
                {"Text": "What is the total amount?", "Alias": "TotalAmount"}
            ]
        }
    )

    results = []
    print("\n=== Extracted Invoice Fields ===\n")

    for block in response['Blocks']:
        if block['BlockType'] == 'QUERY_RESULT':
            alias = block['Query']['Alias']
            answer = block.get('Text', '')
            confidence = block.get('Confidence', 0)
            line = f"{alias}: {answer} (Confidence: {confidence:.1f}%)"
            print(line)
            results.append(line)

    # Save the output to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== Extracted Invoice Fields ===\n\n")
        for line in results:
            f.write(line + "\n")

    print(f"\n✅ Results saved to {output_file}")

if __name__ == "__main__":
    file_path = "invoice.png"       # your local invoice file
    output_file = "output4.txt"     # save result file
    analyze_invoice_queries_local(file_path, output_file)
