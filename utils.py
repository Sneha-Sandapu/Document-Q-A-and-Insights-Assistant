import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_file):
    \"\"\"Extract text from an uploaded PDF file.\"\"\"
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = \"\"
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + \"\\n\"
        return text
    except Exception as e:
        raise Exception(f\"Error reading PDF: {str(e)}\")

def extract_text_from_txt(txt_file):
    \"\"\"Extract text from an uploaded TXT file.\"\"\"
    try:
        return txt_file.getvalue().decode(\"utf-8\")
    except Exception as e:
        raise Exception(f\"Error reading TXT file: {str(e)}\")

def get_text_chunks(text):
    \"\"\"Split text into chunks for vector embedding.\"\"\"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
