import boto3
from dotenv import load_dotenv
import os
import json

# --- Helper Function 1: Get Text from Word Blocks ---
def get_text_from_relationships(block, block_map):
    """
    Gets the text from a block's 'CHILD' relationships (which are WORD blocks).
    """
    text = ""
    if 'Relationships' in block:
        for relationship in block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    child = block_map[child_id]
                    if child['BlockType'] == 'WORD':
                        text += child['Text'] + " "
    return text.strip()

# --- Helper Function 2: Find the Value Block for a Key Block ---
def find_value_block(key_block, value_map):
    """
    Finds the 'VALUE' block associated with a given 'KEY' block.
    """
    for relationship in key_block.get('Relationships', []):
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                return value_map.get(value_id)
    return None

# --- NEW Helper Function 3: Data Cleaning & Type-Casting ---
def clean_value(text_value):
    """
    Cleans a string value, removes currency/commas, and
    attempts to cast it to an integer or float.
    """
    if text_value is None:
        return None
    
    # Strip whitespace first
    text = str(text_value).strip()
    
    # Remove common currency symbols and commas
    cleaned = text.replace('$', '').replace('€', '').replace('£', '').replace('BDT', '').replace(',', '').strip()

    # Don't process empty strings
    if not cleaned:
        return text # return original empty/whitespace string

    # Try to convert to a number
    try:
        # First try float to see if it's like "2.0"
        float_val = float(cleaned)
        if float_val.is_integer():
            # It's a whole number, return as int
            return int(float_val)
        # It's a float, return it
        return float_val
    except ValueError:
        # Not a number, return the original *stripped* text
        return text

# --- UPDATED Helper Function 4: Parse Table Data (with cleaning) ---
def parse_tables(blocks, block_map):
    """
    Parses table blocks and returns a list of dictionaries for items.
    Now auto-cleans all cell values.
    """
    tables = [b for b in blocks if b['BlockType'] == 'TABLE']
    if not tables:
        return []

    table = tables[0]
    cell_blocks = [b for b in blocks if b['BlockType'] == 'CELL']
    
    rows = {}
    for cell in cell_blocks:
        row_idx = cell['RowIndex']
        col_idx = cell['ColumnIndex']
        
        if row_idx not in rows:
            rows[row_idx] = {}
        
        rows[row_idx][col_idx] = get_text_from_relationships(cell, block_map)

    if 1 not in rows:
        return [] # No header row
        
    header_row = rows[1]
    headers = [header_row[col] for col in sorted(header_row.keys())]
    
    # Normalize headers (e.g., "Unit Price" -> "unit_price")
    normalized_headers = []
    for h in headers:
        h_lower = h.lower()
        if 'desc' in h_lower:
            normalized_headers.append('description')
        elif 'qty' in h_lower or 'quantity' in h_lower:
            normalized_headers.append('quantity')
        elif 'unit' in h_lower or 'price' in h_lower:
            normalized_headers.append('unit_price')
        elif 'tax' in h_lower:
            normalized_headers.append('tax')
        elif 'total' in h_lower or 'line' in h_lower:
            normalized_headers.append('line_total')
        else:
            normalized_headers.append(h_lower.replace(' ', '_'))

    # Build the list of item dictionaries
    items_list = []
    for r_idx in sorted(rows.keys()):
        if r_idx == 1:  # Skip header row
            continue
        
        row = rows[r_idx]
        item_dict = {}
        for c_idx in sorted(row.keys()):
            if (c_idx - 1) < len(normalized_headers):
                key = normalized_headers[c_idx - 1]
                value = row[c_idx]
                
                # Auto-clean every value from the table
                item_dict[key] = clean_value(value)
        
        # Only add non-empty rows
        if item_dict:
            items_list.append(item_dict)

    return items_list

# --- Main Analysis Function (Silent, Generic, with Confidence Handling) ---
def analyze_local_invoice(file_path):
    """
    Analyzes a local document silently, extracts ALL key-value pairs,
    cleans them, and sorts by confidence.
    """

    # --- Confidence Thresholds ---
    CONFIDENCE_PRIMARY = 95.0  # >= 95% -> Clean and add to main data
    CONFIDENCE_REVIEW = 70.0   # >= 70% -> Add to "needs_review" list
                               # < 70%  -> Discard
    
    load_dotenv()

    try:
        textract_client = boto3.client('textract')
    except Exception as e:
        print(f"Error creating Boto3 client: {e}")
        return

    try:
        with open(file_path, 'rb') as document:
            file_bytes = document.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'.")
        return

    try:
        response = textract_client.analyze_document(
            Document={'Bytes': file_bytes},
            FeatureTypes=['FORMS', 'TABLES'] 
        )
        
        blocks = response['Blocks']
        
        key_map = {}
        value_map = {}
        block_map = {}
        
        for block in blocks:
            block_id = block['Id']
            block_map[block_id] = block
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block['EntityTypes']:
                    key_map[block_id] = block
                else:
                    value_map[block_id] = block

        # 5. Extract and process all FORMS data
        extracted_data = {}
        needs_review = []

        for block_id, key_block in key_map.items():
            value_block = find_value_block(key_block, value_map)
            
            if value_block:
                key_text = get_text_from_relationships(key_block, block_map)
                val_text = get_text_from_relationships(value_block, block_map)
                
                # Use the average confidence of the key-value pair
                avg_confidence = (key_block['Confidence'] + value_block['Confidence']) / 2
                
                if avg_confidence >= CONFIDENCE_PRIMARY:
                    # High confidence: clean and add to main data
                    extracted_data[key_text] = clean_value(val_text)
                
                elif avg_confidence >= CONFIDENCE_REVIEW:
                    # Medium confidence: add to review list
                    needs_review.append({
                        'key': key_text,
                        'value': val_text,
                        'confidence': round(avg_confidence, 2)
                    })
                # Else: (avg_confidence < CONFIDENCE_REVIEW) -> Discard silently

        # 6. Extract TABLE data
        line_items = parse_tables(blocks, block_map)

        # 7. Structure the final output
        final_json_output = {
            "extracted_data": extracted_data,
            "needs_review": needs_review,
            "line_items": line_items
        }
        
        # 8. Save the final JSON to output4.json
        output_filename = 'output4.json'
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(final_json_output, f, indent=4)
        
        print(f"Successfully saved structured output to {output_filename}.")
            
    except Exception as e:
        print(f"Error during Textract API call: {e}")

# --- RUN THE SCRIPT ---
if __name__ == "__main__":
    
    # !! IMPORTANT: Change this to the path of your local invoice !!
    local_file_path = "invoice.png"
    
    analyze_local_invoice(local_file_path)