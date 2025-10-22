import boto3
import os
import json
from dotenv import load_dotenv

# Load AWS credentials from .env
load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

# Initialize Textract client
textract = boto3.client(
    "textract",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

def extract_tables_local(file_path, output_file="output5.json"):
    # Read the file (no S3 needed)
    with open(file_path, "rb") as document:
        image_bytes = document.read()

    # Analyze document for TABLES
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES']
    )

    # Map block IDs to blocks
    block_map = {block['Id']: block for block in response['Blocks']}
    table_blocks = [b for b in response['Blocks'] if b['BlockType'] == 'TABLE']

    all_tables_data = []

    for idx, table in enumerate(table_blocks, start=1):
        table_type = table.get('TableType', 'STANDARD')
        title = table.get('Title', {}).get('Text', '')
        footer = table.get('Footer', {}).get('Text', '')

        print(f"\nTable {idx}:")
        print(f"Type: {table_type}")
        print(f"Title: {title}")
        print(f"Footer: {footer}")

        # Extract rows & cells
        rows = []
        for relationship in table.get('Relationships', []):
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell = block_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        cell_text = ""
                        for cell_rel in cell.get('Relationships', []):
                            if cell_rel['Type'] == 'CHILD':
                                for word_id in cell_rel['Ids']:
                                    word = block_map[word_id]
                                    if word['BlockType'] == 'WORD':
                                        cell_text += word.get('Text', '') + " "
                        rows.append({
                            "RowIndex": cell['RowIndex'],
                            "ColumnIndex": cell['ColumnIndex'],
                            "Text": cell_text.strip()
                        })

        # Sort by row and column
        rows_sorted = sorted(rows, key=lambda x: (x['RowIndex'], x['ColumnIndex']))
        all_tables_data.append({
            "TableNumber": idx,
            "Type": table_type,
            "Title": title,
            "Footer": footer,
            "Cells": rows_sorted
        })

    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_tables_data, f, indent=4)

    print(f"\nExtracted table data saved to {output_file}")

# Example usage
extract_tables_local("table.png")
