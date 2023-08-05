from typing import Union
from pathlib import Path
import PyPDF2


class FileReader:
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path
        self.text = ""

    def read_textfile(self) -> str:
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            text = file.read()
            return text

    def read_pdf(self) -> str:
        with open(self.file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page_num).extractText()
            return text

    def read(self) -> str:
        if self.file_path.lower().endswith(".pdf"):
            self.text = self.read_pdf()
        else:
            self.text = self.read_textfile()
        return self.text



