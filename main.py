from pypdf import PdfReader


class PdfFile:
    def __init__(self, file, reference_file):
        self.file = file
        self.reference_file = reference_file

    def read_pdf_file(self):
        pdf_text = ""
        reader = PdfReader(self.file)
        for page in reader.pages:
            pdf_text += page.extract_text()
        return pdf_text

    def compare_pdfs(self):
        reference_file = PdfReader(self.reference_file)
        input_file = PdfReader(self.file)

        assert len(reference_file.pages) == len(input_file.pages)

        for page in range(len(reference_file.pages)):
            reference_page = reference_file.pages[page]
            input_page = input_file.pages[page]

            assert reference_page.extract_text() == input_page.extract_text()
            assert reference_page.mediabox == input_page.mediabox


task_pdf = './files/test_task.pdf'
reference_pdf = './files/reference_file.pdf'

pdf_file = PdfFile(task_pdf, reference_pdf)
print(pdf_file.read_pdf_file())
pdf_file.compare_pdfs()
