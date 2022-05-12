from concurrent.futures import process
from pprint import pprint
import os


class Search():

    #def export_needed_processos(processos_dictionary, txt_file_with_laywers):
    def export_needed_processos(all_processos_list):
        name = "MAXIMILIANO NAGL GARCEZ"
        search = "MAXIMILIANO NAGL GARCEZ".lower().replace(" ","")
        processos_found = []
        print("export_needed_processos")
        print(all_processos_list)
        txt_folder_path = os.sep.join([f'assets\\{all_processos_list[0][0]["date"]}', search.replace(" ","-").title()])

        for processos_list in all_processos_list:
            for processo in processos_list:
                processo_key = next(iter(processo))
                
                text = processo[processo_key]['to_search']
                if search in text:
                    processo_name = processo_key.replace("Processo Nº ","")
                    print(processo_name)
                    processos_found.append(processo_name)

        print(len(processos_found))

        return processos_found