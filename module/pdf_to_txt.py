import fitz
import time
import re
import shutil
import os
from pathlib import Path
from pprint import pprint
from module.addons import Progress_bar
from module.addons import Dirs_files
from io import StringIO

class Pdf_to_txt:

    folder_created_in_this_session = False

    #------------------------------------------------------
    # Generate txt file from pdf path
    #------------------------------------------------------

    def convert(pdf_path):
        start_time_program = time.time()
        pdf = fitz.open(pdf_path)
        pagesCount = pdf.page_count

        txtFilename = Path(pdf_path).stem + ".txt"
        date = Path(pdf_path).parent.name
        path = f'assets\\txt\\dejt\\{date}\\'

        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)

        print(f"- Convertendo {Path(pdf_path).name} para .txt")

        for index, page in enumerate(pdf):
            

            left_side_page = page.get_text(
                clip=fitz.Rect(page.rect.width * 0.04,page.rect.width * 0.09, page.rect.width / 2 , page.rect.height * 0.97),
                flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES
            )
            right_side_page = page.get_text(
                clip=fitz.Rect(page.rect.width * 0.52 , page.rect.width * 0.09, page.rect.width * 0.96 , page.rect.height * 0.97),
                flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES
            )

            string = left_side_page + right_side_page

            Dirs_files.append_new_line(path+txtFilename, string)

            #Progress_bar.print(index + 1, pagesCount, prefix = 'Progress:', suffix = 'Complete', length = 50)

            #print(f"--- {round(time.time() - start_time_scraping,2)} seconds to finish page {index+1}/{pagesCount} ---")

        return os.sep.join([path, txtFilename])

    #------------------------------------------------------
    # Generate txt files from a list of pdf paths
    #------------------------------------------------------

    def convert_from_list(pdf_path_list):
        txt_files = []

        for pdf_path in pdf_path_list:
            txt_file = Pdf_to_txt.convert_better(pdf_path)
            txt_files.append(txt_file)

        return txt_files

    def convert_better(pdf_path):
        start_time_program = time.time()

        pdf = fitz.open(pdf_path)
        pagesCount = pdf.page_count

        txtFilename = Path(pdf_path).stem + ".txt"

        date = Path(pdf_path).parent.name
        path = Path(f'assets\\txt\\dejt\\') / date
        
        if not path.exists():
            Dirs_files.create_folder_if_inexistent(path)            
        
        processoRegex = "^Processo Nº ([a-zA-Z]+)-([0-9]+)-([0-9]+).([0-9]+).([0-9]+).([0-9]+).([0-9]+)$"

        fake_txt_file = StringIO()
        print(f"\n- Convertendo {Path(pdf_path).name} para .txt")

        for index, pageDict in enumerate(pdf):

            left_side_page = pageDict.get_text("dict",
                clip=fitz.Rect(pageDict.rect.width * 0.04,pageDict.rect.width * 0.09, pageDict.rect.width / 2 , pageDict.rect.height * 0.97),
                flags= ~fitz.TEXT_PRESERVE_IMAGES
            )
            right_side_page = pageDict.get_text("dict",
                clip=fitz.Rect(pageDict.rect.width * 0.52 , pageDict.rect.width * 0.09, pageDict.rect.width * 0.96 , pageDict.rect.height * 0.97),
                flags= ~fitz.TEXT_PRESERVE_IMAGES
            )

            

            for block in left_side_page["blocks"]:
                for line in block["lines"]:
                    for span in line["spans"]:
                        string = span["text"] +"\n"
                        if "SUMÁRIO" in string and span["font"] == 'Helvetica-Bold' and span["size"] == 10.0:
                                fake_txt_file.write("---------------------------------------------------------------\n")
                                fake_txt_file.write(string)
                                continue

                        if re.search(processoRegex, span["text"]) and span["font"] == 'Helvetica-Bold':
                                fake_txt_file.write("---------------------------------------------------------------\n")
                                fake_txt_file.write(string)
                                continue
                        fake_txt_file.write(string)

            for block in right_side_page["blocks"]:
                for line in block["lines"]:
                    for span in line["spans"]:
                        string = span["text"] +"\n"
                        if "SUMÁRIO" in string and span["font"] == 'Helvetica-Bold' and span["size"] == 10.0:
                                fake_txt_file.write("---------------------------------------------------------------\n")
                                fake_txt_file.write(string)
                                continue

                        if re.search(processoRegex, span["text"]) and span["font"] == 'Helvetica-Bold':
                                fake_txt_file.write("---------------------------------------------------------------\n")
                                fake_txt_file.write(string)
                                continue

                        fake_txt_file.write(string)
    
            Progress_bar.print(index + 1, pagesCount, prefix = 'Progress:', suffix = 'Complete', length = 50)

        

        #Dirs_files.append_new_line(path+txtFilename, fake_txt_file.getvalue())
        with open(path/txtFilename, 'w',encoding="utf-8") as fd:
            fake_txt_file.seek(0)
            shutil.copyfileobj(fake_txt_file, fd)


            #print(f"--- {round(time.time() - start_time_scraping,2)} seconds to finish page {index+1}/{pagesCount} ---")

        print(f"--- {round(time.time() - start_time_program,2)} seconds to finish the program ---\n")

        return path/txtFilename
