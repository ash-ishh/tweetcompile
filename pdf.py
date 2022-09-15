import os
import pdfkit

PAGE_SIZE = "A4"

class PDF:
    def __init__(self, *args, **kwargs):
        self.html_path = kwargs.get("html_path")
        self.output_file_path = kwargs.get("output_file_path")
        self.options = {
            'page-size': PAGE_SIZE,
            'enable-local-file-access': None
        }
    
    def save_pdf(self):
        with open(self.html_path) as f:
            pdfkit.from_file(f, self.output_file_path, options=self.options)