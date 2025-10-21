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

def analyze_form_from_local_file(file_path, output_file):
    with open(file_path, "rb") as document:
        image_bytes = document.read()

    response = textract.analyze_document(
        Document= {"Bytes": image_bytes},
        FeatureTypes=["FORMS"]
    )
    
    # Map block IDs to blocks
    block_map = {block["Id"]: block for block in response["Blocks"]}
    
    results = []

    # Traverse blocks to find key-value pairs
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in block.get('EntityTypes', []):
            key_text = ''
            value_text = ''

            # Extract key text
            for rel in block.get('Relationships', []):
                if rel['Type'] == 'CHILD':
                    for cid in rel['Ids']:
                        child = block_map[cid]
                        if child['BlockType'] in ['WORD', 'SELECTION_ELEMENT']:
                            key_text += child.get('Text', '') + ' '

            # Find the value block
            for rel in block.get('Relationships', []):
                if rel['Type'] == 'VALUE':
                    for vid in rel['Ids']:
                        value_block = block_map[vid]
                        for vrel in value_block.get('Relationships', []):
                            if vrel['Type'] == 'CHILD':
                                for vcid in vrel['Ids']:
                                    vchild = block_map[vcid]
                                    if vchild['BlockType'] in ['WORD', 'SELECTION_ELEMENT']:
                                        value_text += vchild.get('Text', '') + ' '

            if key_text.strip() or value_text.strip():
                line = f"Key: {key_text.strip()} -> Value: {value_text.strip()} (Confidence: {block['Confidence']:.1f}%)"
                print(line)
                results.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== Extracted Key-Value Pairs ===\n\n")
        for line in results:
            f.write(line + "\n")

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    file_path = "form.png"   # input filename
    output_file = "output3.txt"
    analyze_form_from_local_file(file_path, output_file)
