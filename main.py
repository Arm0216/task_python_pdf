from pypdf import PdfReader


class PdfFile:
    def __init__(self, file, reference_file):
        self.file = file
        self.reference_file = reference_file

    def get_content_with_map(self):
        reader = PdfReader(self.file)
        my_map = {}
        for page in reader.pages:
            arr = page.extract_text().split('\n')
            prev_key = ''

            for i in arr:
                first_index = i.find(':')
                last_index = i.rfind(':')

                if first_index == -1:
                    if prev_key:
                        my_map[prev_key] = i
                        prev_key = ''
                    else:
                        my_map[i] = ''
                    continue

                if last_index == first_index:
                    key = i[:first_index].strip()
                    value = i[first_index + 1:].strip()
                    my_map[key] = value
                    continue

                first_key = i[:first_index].strip()
                other_part = i[first_index + 1:last_index].strip()
                second_key = other_part.split(' ')[-1]
                first_value = other_part[:other_part.index(second_key)].strip()
                second_value = i[last_index + 1:].strip()

                my_map[first_key] = first_value

                if len(second_value) == 0:
                    prev_key = second_key
                else:
                    my_map[second_key] = second_value
        return my_map

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
pdf_file.compare_pdfs()
print(pdf_file.get_content_with_map())
