from concurrent.futures import process
from pprint import pprint
import os


class Search():
    def separate_processos(txt_path):
        processos_list = []
        with open(txt_path,"rt",encoding="utf-8") as txt_file:
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


                processo = {lines[index_processo_title].rstrip():{
                    "to_search" : string,
                    "to_export" : lines[index_first_line_processo_body:index_last_line_processo_body]
                }}

                processos_list.append(processo)

        return processos_list

    #def export_needed_processos(processos_dictionary, txt_file_with_laywers):
    def export_needed_processos(processos_list):
        search = "MAXIMILIANO NAGL GARCEZ".lower().replace(" ","")
        processos_of_search = {}
        processos_found = []

        txt_folder_path = os.sep.join(['assets\\processos-coletados', search.replace(" ","-")])

        for processo in processos_list:
            processo_key = next(iter(processo))
            
            text = processo[processo_key]['to_search']
            if search in text:
                processo_name = processo_key.replace("Processo Nº ","")
                print(processo_name)
                processos_found.append(processo_name)

        print(len(processos_found))

        
        #return txt_path

                            
    def separate_processos_from_list(txt_path_list):
        txt_files = []

        for txt_path in txt_path_list:
            txt_file = Search.separate_processos(txt_path)
            txt_files.append(txt_file)

        return txt_files