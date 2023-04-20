import sys

import PyPDF2


def extract_text(pdf_file, output_file):
    with open(pdf_file, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
        extracted_text = ""

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

    with open(output_file, "w") as f:
        f.write(extracted_text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_txt.py input.pdf output.txt")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_file = sys.argv[2]

    extract_text(pdf_file, output_file)
