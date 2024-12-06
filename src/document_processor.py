import pymupdf

def process_document(file):
    file_path = f"../data/uploaded_document.{file.type.split('/')[-1]}"
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return [file_path]

def extract_text_from_pdf(file_path):
    pdf_document = pymupdf.open(file_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text