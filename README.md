# 🧾 Transforming-OCR-into-Instant-Structured-Data-Using-Amazon-Textract-s-Synchronous-APIs

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![AWS Textract](https://img.shields.io/badge/Service-AWS%20Textract-orange.svg)
![Environment](https://img.shields.io/badge/Config-.env-success.svg)
![Mode](https://img.shields.io/badge/Mode-Synchronous%20OCR-yellowgreen.svg)

## 📘 Overview
This project demonstrates how to use **Amazon Textract** to extract text, key-value pairs, tables, and specific fields from documents — **without uploading them to Amazon S3**.  
It processes local files such as **PDFs**, **PNGs**, or **JPGs**, using the `Bytes` method of Textract.

Each script is designed for a specific purpose:
- **Basic OCR** → Extract raw text  
- **Forms** → Extract key–value pairs  
- **Invoice** → Extract specific information from Invoice with key-value pairs  
- **Tables** → Extract table data and metadata  

All results are saved locally in Output file(`e. g. output3.txt` / `output4.json`) for easy analysis and debugging.

---

## 🚀 Features

✅ Works with **local documents** (no S3 upload required)  
✅ Secure credential management using **`.env`** file  
✅ Supports **PDF**, **PNG**, and **JPG** files  
✅ Extracts:
- Plain text  
- Key-value pairs  
- Invoice
- Tables and metadata  
✅ Saves results to **JSON or TXT** files  
✅ Clean modular Python scripts for each extraction type  

---

## 🧩 Folder Structure

```
📂 Amazon-Textract-Local
│
├── 1.ExtractingTextLinesFromPDF.py                        # Basic OCR from Lines
├── 2.Basic_Synchronous_OCR_with_DetectDocumentText.py     # Basic OCR (DetectDocumentText)
├── 3.Extracting_Key_Value_Pairs_from_a_Form.py            # Extract key-value pairs (FORMS)
├── 4.Processing_an_Invoice_with_AnalyzeExpense.py         # Extract Invoice with key-value pairs
├── 5.Extracting_Enhanced_Table_Structure.py               # Extract tables and metadata (TABLES)
│
├── .env                           # AWS credentials (not shared in repo)
├── myenv                          # Creating Vartual environment
├── output1,2,3,4,5                # output
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/mehedihasanmir/Transforming-OCR-into-Instant-Structured-Data-Using-Amazon-Textract-s-Synchronous-APIs.git
cd Transforming-OCR-into-Instant-Structured-Data-Using-Amazon-Textract-s-Synchronous-APIs
```

### 2️⃣ Create a virtual environment
```bash
python -m venv textract-env
source textract-env/bin/activate    # For Linux/Mac
# OR
textract-env\Scripts\activate       # For Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` file
Add your AWS credentials securely:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

---

## Usage

You can process **local PDFs or images** using any of the provided scripts.

---

### 1. Basic OCR Extraction

**File:** `1.ExtractingTextLinesFromPDF.py`

Extracts raw text lines from documents.

```bash
python 1.ExtractingTextLinesFromPDF.py
```

**Output:**  
- Extracted text printed on screen  
- Saved to `output1.txt`

---

### 2. Basic OCR with Detect Document

**File:** `2.Basic_Synchronous_OCR_with_DetectDocumentText.py`

Extracts pain data 

```bash
python 2.Basic_Synchronous_OCR_with_DetectDocumentText.py
```

**Output:**  
- Extracted text printed on screen  
- Saved to `output2.txt`

---

###  3. Extracting key-value pairs from Form

**File:** `3.Extracting_Key_Value_Pairs_from_a_Form.py`

Uses **Textract Queries** to answer questions such as:
- What is the Name?
- What is the Id?
- Who is the Italsocontainsfieldcorier?
- etc

```bash
python 3.Extracting_Key_Value_Pairs_from_a_Form.py
```

**Output Example:**

```text
Key: NO -> Value:  (Confidence: 89.3%)
Key: NAME: -> Value: JohnDoe (Confidence: 94.3%)
Key: ThisisatesttoevaluateOCRaccuracyonformdata. -> Value:  (Confidence: 89.5%)
Key: Italsocontainsfieldcorier. -> Value:  (Confidence: 80.0%)
Key: Theformincludesvariousfieldtypes. -> Value:  (Confidence: 88.7%)
Key: Theformincludesvariousfieldtypes. -> Value:  (Confidence: 89.4%)
Key: Overallclarityshouldtohighforextraction. -> Value:  (Confidence: 60.0%)
```

Saved to: **`output3.txt`**

---

### 4. Invoice Extraction

**File:** `4.Processing_an_Invoice_with_AnalyzeExpense.py`

Extracts structured data form Invoice

```bash
python 4.Processing_an_Invoice_with_AnalyzeExpense.py
```

**Output Example:**

```json
    "extracted_data": {},
    "needs_review": [
        {
            "key": "Due Date:",
            "value": "02/01/2019",
            "confidence": 94.9
        },
        {
            "key": "BILLED TO",
            "value": "Jon Smith 6701 Mesquite Ct Heights, Maryland(MD), 20747",
            "confidence": 94.99
        },
        {
            "key": "Total",
            "value": "$900",
            "confidence": 94.71
        },
        {
            "key": "NO.",
            "value": "0000354",
            "confidence": 94.7
        },
        {
            "key": "DATE",
            "value": "01/01/2019",
            "confidence": 94.64
        },
        {
            "key": "Account:",
            "value": "04USDLR023400545064",
            "confidence": 92.49
        },
        {
            "key": "Townline Ln NE",
            "value": "1632",
            "confidence": 82.12
        }
    ],
    "line_items": [
        {
            "description": "Item 1",
            "unit_price": 100,
            "quantity": 1,
            "line_total": 100
        },
        {
            "description": "Item 2",
            "unit_price": 300,
            "quantity": 1,
            "line_total": 300
        },
        {
            "description": "Item 3",
            "unit_price": 500,
            "quantity": 1,
            "line_total": 500
        },
        {
            "description": "",
            "unit_price": "",
            "quantity": "",
            "line_total": ""
        }
    ]
}
```

Saved to: **`output4.json`**

---

### 5. Table Extraction with Metadata

**File:** `5.Extracting_Enhanced_Table_Structure.py`

Extracts structured tables and metadata (title, footer, type).

```bash
python 5.Extracting_Enhanced_Table_Structure.py
```

**Output Example:**

```json
[
  {
    "TableNumber": 1,
    "Type": "STANDARD",
    "Title": "Monthly Statement",
    "Footer": "Confidential",
    "Cells": [
      {"RowIndex": 1, "ColumnIndex": 1, "Text": "Date"},
      {"RowIndex": 1, "ColumnIndex": 2, "Text": "Amount"},
      {"RowIndex": 2, "ColumnIndex": 1, "Text": "2025-10-01"},
      {"RowIndex": 2, "ColumnIndex": 2, "Text": "$500"}
    ]
  }
]
```

Saved to: **`output5.json`**

---

## 🧰 Requirements

- Python 3.10
- AWS account with Textract permissions
- Libraries:
  - `boto3`
  - `python-dotenv`
  - `json`
  - `os`

---

## 🔒 Security Note
Your AWS credentials are **never hardcoded** in the scripts.  
They are securely loaded from a local `.env` file using `python-dotenv`.

> ⚠️ Never commit `.env` to GitHub.  
> Add it to `.gitignore` to protect your credentials.

---

## 🌎 Supported File Types

| Format | Supported | Notes |
|--------|------------|-------|
| `.pdf` | Single or multi-page (synchronous < 5 MB) |
| `.png` | Works well for high-contrast scans |
| `.jpg` / `.jpeg` | Ideal for camera-based document captures |

---

## 🧩 Possible Enhancements

- Convert extracted tables to CSV or Excel  
- Add asynchronous document processing for larger files  
- Build a **Streamlit** or **Flask** UI for uploading and visualizing results  
- Add **error handling and logging** for better debugging  

---

## 🧑‍💻 Author

**Mehedi Hasan Mir**  
AI & Machine Learning Enthusiast  
📍 Bangladesh  

💼 [LinkedIn](https://www.linkedin.com/in/mehedi-hasan-mir/) • 🐙 [GitHub](https://github.com/mehedihasanmir)

---

## 🪪 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it.
