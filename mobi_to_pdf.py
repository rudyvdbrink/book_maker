import os
import mobi
from fpdf import FPDF
from bs4 import BeautifulSoup
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'MOBI to PDF', 0, 1, 'C')

    def chapter_title(self, chapter_title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, chapter_title, 0, 1, 'L')

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

# Function to clean and remove non-ASCII characters
def clean_text(text):
    # Remove non-ASCII characters using regex
    clean_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return clean_text

def mobi_to_pdf(mobi_file, output_pdf):
    # Convert MOBI to HTML using mobi library
    mobi_folder = mobi.extract(mobi_file)
    #html_file = os.path.join(mobi_folder, "mobi7", "index.html")
    html_file = mobi_folder[1]

    if not os.path.exists(html_file):
        print("Failed to extract HTML from MOBI.")
        return

    # Create PDF instance
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Read the extracted HTML content
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract title and body
    title = soup.title.string if soup.title else 'No Title'
    body_text = soup.get_text()
    body_text = clean_text(soup.get_text())

    # Add the extracted content to the PDF
    pdf.chapter_title(title)
    pdf.chapter_body(body_text)

    # Save to PDF file
    pdf.output(output_pdf)
    print(f"Successfully converted {mobi_file} to {output_pdf}")

if __name__ == "__main__":
    # mobi_file = input("Enter the path to the .mobi file: ")
    # output_pdf = input("Enter the output path for the PDF: ")

    mobi_file = './mobi/test.mobi'
    output_pdf = './pdf/test.pdf'

    if os.path.exists(mobi_file):
        mobi_to_pdf(mobi_file, output_pdf)
    else:
        print("The specified .mobi file does not exist.")
