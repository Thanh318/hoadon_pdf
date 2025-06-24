import streamlit as st
import pandas as pd
import pdfplumber
import re
import json

# Load từ khóa
with open("keywords.json", "r", encoding="utf-8") as f:
    KEYWORDS = json.load(f)

def clean_number(value):
    return re.sub(r"\s+", "", value)

def extract_fields(text):
    result = {
        "mst": "",
        "seller": "",
        "invoice_series": "",
        "invoice_no": "",
        "invoice_date": "",
        "total_amount": ""
    }
    for line in text.split("\n"):
        for field, keywords in KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in line.lower() and result[field] == "":
                    value = re.sub(rf"{kw}[:\-–\s]*", "", line, flags=re.IGNORECASE)
                    if field in ["mst", "invoice_no", "total_amount"]:
                        value = clean_number(value)
                    result[field] = value.strip()
    return result

st.title("Trích xuất hóa đơn PDF (text-based)")

uploaded_file = st.file_uploader("Tải file PDF", type="pdf")
if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    data = extract_fields(text)
    df = pd.DataFrame([data])
    st.dataframe(df)

    st.download_button("Tải Excel", df.to_csv(index=False).encode("utf-8"), file_name="hoa_don.csv")

