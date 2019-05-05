import os
import pdfkit

PAGE_SIZE = "A4"

class PDF:
    def __init__(self):
        self.options = {
            'page-size': PAGE_SIZE,
        }
    
    def save_pdf(self, html_path, output_file):
        with open(html_path) as f:
            pdfkit.from_file(f, output_file, options=self.options)