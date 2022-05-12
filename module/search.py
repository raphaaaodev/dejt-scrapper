from concurrent.futures import process
from pprint import pprint
from pathlib import Path
import os
from time import sleep

from .addons import Dirs_files


class Search():

    #def export_needed_processos(processos_dictionary, txt_file_with_laywers):
    def export_needed_processos(txt_files):
        name = "MAXIMILIANO NAGL GARCEZ"
        search = name.lower().replace(" ","")

        everything_txt_creation_flag = False

        export_folders = []

        #Dirs_files.append_new_line(everything_txt,name)
        

        for txt_file in txt_files:
            
            txt_path = Path(txt_file)
            orgao = txt_path.stem
            date = txt_path.parent.name
            lawyer_name = name.replace(" ","-").title()

            exported_search_path = Path(f'assets\\processos-exportados\\{lawyer_name}\\{date}\\{orgao}')

            processos_names_txt = Path(exported_search_path) / "!Todos-os-processos.txt"
            processos_names = []

            if (processos_names_txt.exists()):
                processos_names_txt.unlink()

            export_folders.append(exported_search_path)

            isExist = os.path.exists(exported_search_path)
            if not isExist:
                os.makedirs(exported_search_path)

            with open(txt_file,"rt",encoding="utf-8") as txt_file:
                lines = txt_file.readlines()
                processo_separators = [index for index, line in enumerate(lines) if "--------------" in line]

                for index, separator in enumerate(processo_separators):
                    if index == len(processo_separators)-1:
                        continue

                    index_processo_title = separator+1
                    index_first_line_processo_body = separator+2
                    index_last_line_processo_body = processo_separators[index+1]-1

                    string = ""

                    for line in lines[index_first_line_processo_body:index_last_line_processo_body]:
                        string += line.rstrip().lower().replace(" ","")

                    if search in string:
                        processo_name = lines[index_processo_title].rstrip().replace("Processo Nº ","")
                        processo_txt_path = Path(exported_search_path) / f"{processo_name}.txt"
                        
                        processos_names.append(processo_name+"\n")
                        #Dirs_files.append_new_line(everything_txt,f"\t{processo_name}")

                        print(processo_name)

                        if (processo_txt_path.exists()):
                            processo_txt_path.unlink()

                        with open(processo_txt_path, "w",encoding='utf-8') as file_object:
                            file_object.writelines(lines[index_first_line_processo_body:index_last_line_processo_body])

            if len(processos_names)==0:
                exported_search_path.rmdir()
                continue

            #Dirs_files.append_new_line(everything_txt,f"\n")

            with open(processos_names_txt, "w",encoding='utf-8') as file_object:
                file_object.write(f"Total: {len(processos_names)}\n")
                file_object.writelines(processos_names)

        return export_folders