import PyPDF2
import re
import os
import csv

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
            return text
    except PyPDF2.errors.PdfReadError:
        print(f"Error reading {pdf_path}. Skipping this file.")
        return ''  # Return empty text for unreadable PDFs

# Function to extract emails from the text
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)

# Function to extract phone numbers from the text
def extract_phone_numbers(text):
    phone_pattern = r'\+?\d{1,4}[-.\s]?\d{10}'  # For country code and 10-digit numbers
    return re.findall(phone_pattern, text)

# Function to extract names from the text
def extract_names(text):
    name_pattern = r'\b([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b'
    return re.findall(name_pattern, text)

# Directory path containing the PDF files
path = 'C:/Users/nanda/Downloads/RISHITHA_BBT/Indeed_Resume/'

# List to store the extracted data
data = []

# Loop through each file in the directory
for i in os.listdir(path):
    if i.endswith(".pdf"):  # Process only PDF files
        pdf_name = i[:-4]  # Remove the ".pdf" extension
        first_letter = pdf_name[2:] 
        print(first_letter)
        # Extract the first letter of the file name
 # Full path to the PDF file
        pdf_path = os.path.join(path, i)
        pdf_text = extract_text_from_pdf(pdf_path)

        if pdf_text:  # Process only if text was successfully extracted
            emails = extract_emails(pdf_text)
            phone_numbers = extract_phone_numbers(pdf_text)
            names = extract_names(pdf_text)

            # Add the extracted data as a dictionary to the list
            data.append({
                'File Name': first_letter,
                'Phone Numbers': ', '.join(phone_numbers),
                'Emails': ', '.join(emails)
            })

# CSV file path
csv_file_path = "extracted_data.csv"

# Writing data to the CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['File Name', 'Phone Numbers', 'Emails'])
    writer.writeheader()  # Write the header
    writer.writerows(data)  # Write the data rows

print(f"Data has been saved to {csv_file_path}")
