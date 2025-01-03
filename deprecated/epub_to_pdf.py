import os
import ebooklib
from ebooklib import epub
from fpdf import FPDF
from bs4 import BeautifulSoup
import re

class PDF(FPDF):
    #def header(self):
        # self.set_font('Arial', 'B', 12)
        # self.cell(0, 10, 'EPUB to PDF', 0, 1, 'C')
        
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

def epub_to_pdf(epub_file, output_pdf):
    # Load EPUB file
    book = epub.read_epub(epub_file)

    # Create PDF instance
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Loop through the EPUB items
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            
            # Extract title and body
            title = soup.title.string if soup.title else 'No Title'
            body_text = soup.get_text()
            body_text = clean_text(body_text)

            # Add chapter to PDF
            pdf.chapter_title(title)
            pdf.chapter_body(body_text)

            #track chapter number
            #text to speech hear
            #body_text.replace('\n',' ')

    # Save to PDF file
    pdf.output(output_pdf)
    print(f"Successfully converted {epub_file} to {output_pdf}")

if __name__ == "__main__":
    #epub_file = input("Enter the path to the .epub file: ")
    #output_pdf = input("Enter the output path for the PDF: ")

    epub_file = './epub/test.epub'
    output_pdf = './pdf/test2.pdf'


    if os.path.exists(epub_file):
        epub_to_pdf(epub_file, output_pdf)
    else:
        print("The specified .epub file does not exist.")
