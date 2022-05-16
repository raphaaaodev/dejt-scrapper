from concurrent.futures import process
from pprint import pprint
from pathlib import Path
import os
from time import sleep
from io import StringIO
import shutil
import time

from .addons import Dirs_files
from .addons import Progress_bar

clear = lambda: print("\033c", end='')
class Search():

    #def export_needed_processos(processos_dictionary, txt_file_with_laywers):
    def export_needed_processos(txt_files, txt_file_with_laywers):
        
        
        with open(txt_file_with_laywers,"r",encoding="utf-8") as f:
            lines = f.readlines()
            lawyers_names = [line.rstrip() for line in lines]

        lawyers_count = len(lawyers_names)

        txt_path = Path(txt_files[0])
        date = txt_path.parent.name
        print(date)

        export_search_path = Path(f'assets\\processos-exportados\\{date}')
        export_search_path.mkdir(parents=True, exist_ok=True)

        summary_txt = export_search_path / "!sumario.txt"
        summary_txt_fake = StringIO()
        if (summary_txt.exists()):
            summary_txt.unlink()
        
        total_processos = 0
        total_unique_processos = 0

        export_lawyers_folders = []    

        for index, lawyer_name in enumerate(lawyers_names):
            ticLaywer = time.perf_counter()
            search = lawyer_name.lower().replace(" ","")
            
            lawyer_name = lawyer_name.title()

            lawyer_name_for_path = lawyer_name.replace(" ","-").title()
            
            export_lawyer_path = export_search_path / lawyer_name_for_path
            export_lawyer_path.mkdir(exist_ok=True)
            
            processos_names_lawyer_txt = Path(export_lawyer_path) / "!Todos-os-processos.txt"

            if (processos_names_lawyer_txt.exists()):
                processos_names_lawyer_txt.unlink()

            processos_names_lawyer = []

            clear()
            print(f"\nColetando dados do {lawyer_name} ({index+1}/{lawyers_count})")
            Progress_bar.print(index + 1, lawyers_count, prefix = 'Progress:', suffix = 'Complete', length = 50)

            processos_names_txt_fake = StringIO()

            for txt_file in txt_files:
                
                txt_path = Path(txt_file)
                
                orgao = txt_path.stem
                search_found_flag = False
                
                export_orgao_path = export_lawyer_path / date / orgao
                if (export_orgao_path.exists()):
                    shutil.rmtree(export_orgao_path)
                
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
                            if search_found_flag == False:
                                search_found_flag = True
                                processos_names_txt_fake.write(f"\t{orgao}\n")
                            processo_name = lines[index_processo_title].rstrip().replace("Processo Nº ","")
                            processos_names_txt_fake.write(f"\t\t{processo_name}\n")

                            processo_txt_path = export_lawyer_path / f"{processo_name}.txt"

                            processos_names_lawyer.append(processo_name+"\n")
                            #Dirs_files.append_new_line(everything_txt,f"\t{processo_name}")

                            if (processo_txt_path.exists()):
                                processo_txt_path.unlink()

                            with open(processo_txt_path, "w",encoding='utf-8') as file_object:
                                file_object.writelines(lines[index_first_line_processo_body:index_last_line_processo_body])
                                
                
                        # ---------------------------------
                        # CLOSING txt_file
                        # ---------------------------------
                    #-------------------------------------------------tocCloseTxt_file----------------------------------------------------------------
            # ---------------------------------
            # FIM ITERAÇÃO NOS CADERNOS
            # ---------------------------------

            if len(processos_names_lawyer)==0:
                shutil.rmtree(export_lawyer_path)
                del processos_names_txt_fake
                continue

            export_lawyers_folders.append(export_lawyer_path)
            total_processos += len(processos_names_lawyer)
            unique_processos = set(processos_names_lawyer)
            total_unique_processos += len(unique_processos)

            processos_names_txt_fake.seek(0)
            lines_fake = processos_names_txt_fake.readlines()

            with open(processos_names_lawyer_txt, "a+",encoding='utf-8') as file_object:
                file_object.write(f"{lawyer_name} (Total: {len(processos_names_lawyer)}, Unicos: {len(unique_processos)})\n")
                file_object.writelines(lines_fake)

            summary_txt_fake.write(f"{lawyer_name} (Total: {len(processos_names_lawyer)}, Unicos: {len(unique_processos)})\n")
            summary_txt_fake.writelines(lines_fake)
        # ---------------------------------
        # FIM ITERAÇÃO DOS ADVOGADOS
        # ---------------------------------
        summary_txt_fake.seek(0)
        lines_fake = summary_txt_fake.readlines()

        with open(summary_txt, "w",encoding='utf-8') as file_object:
                file_object.write(f"Total de processos: {total_processos}\n\n")
                file_object.write(f"Total processos unicos: {total_unique_processos}\n\n")
                file_object.writelines(lines_fake)
        return export_lawyers_folders
