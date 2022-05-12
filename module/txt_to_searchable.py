from pathlib import Path

class TxtToSearchable:
    def separate_processos(txt_path):
        processos_list = []
        
        file_path_object = Path(txt_path)
        orgao = file_path_object.stem
        date = file_path_object.parent.name
        
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
                    "to_export" : lines[index_first_line_processo_body:index_last_line_processo_body],
                    "orgao": orgao,
                    "date": date
                    }}

                processos_list.append(processo)

                break

        return processos_list

    def separate_processos_from_list(txt_path_list):
        all_processos_list = []

        for txt_path in txt_path_list:
            processo_list = TxtToSearchable.separate_processos(txt_path)
            all_processos_list.append(processo_list)

        return all_processos_list