import requests
import re
import os
import shutil
from datetime import datetime
from bs4 import BeautifulSoup

from .addons import Progress_bar
from .config import Config

clear = lambda: print("\033c", end='')

class Dejt:

    CADERNOS = None
    NEWEST_DATE = None
    HEADERS = None
    PAYLOAD = None
    API_ENDPOINT = None

    #------------------------------------------------------
    # Load configs from yaml file
    #------------------------------------------------------

    @staticmethod
    def load_config():
        Dejt.CADERNOS = Config.get('DEJT', 'CADERNOS')
        Dejt.HEADERS = Config.get('DEJT','HEADERS')
        Dejt.API_ENDPOINT = Config.get('DEJT','API_ENDPOINT')
        Dejt.NEWEST_DATE = Dejt.get_notebook_date_now()

    def initiate_session(date):
        
        session = requests.Session()

        try:
            session_get = session.get(Dejt.API_ENDPOINT,headers=Dejt.HEADERS)
        except Exception as e:
            print(e)
            print('Error status code', session_get.status_code, session_get.text)
        
        soup = BeautifulSoup(session_get.content,'html.parser')

        Dejt.PAYLOAD = {
            "corpo:formulario:dataIni": date,
            "corpo:formulario:dataFim": date,
            "corpo:formulario:tipoCaderno": "1",
            "corpo:formulario:tribunal": "",
            "corpo:formulario:ordenacaoPlc": soup.find("input",{"name":"corpo:formulario:ordenacaoPlc"})["value"], 
            "navDe": soup.find("input",{"name":"navDe"})["value"],
            "detCorrPlc": soup.find("input",{"name":"detCorrPlc"})["value"],
            "tabCorrPlc": soup.find("input",{"name":"tabCorrPlc"})["value"],
            "detCorrPlcPaginado": soup.find("input",{"name":"detCorrPlcPaginado"})["value"], 
            "exibeEdDocPlc": soup.find("input",{"name":"exibeEdDocPlc"})["value"],
            "indExcDetPlc": "",
            "org.apache.myfaces.trinidad.faces.FORM": soup.find("input",{"name":"org.apache.myfaces.trinidad.faces.FORM"})["value"],
            "_noJavaScript": soup.find("input",{"name":"_noJavaScript"})["value"],
            "javax.faces.ViewState": soup.find("input",{"name":"javax.faces.ViewState"})["value"],
            "source": "corpo:formulario:botaoAcaoPesquisar",
        }

        post = session.post(Dejt.API_ENDPOINT,data=Dejt.PAYLOAD,headers=Dejt.HEADERS)

        return session

    #------------------------------------------------------
    # Initiate session to get PAYLOAD
    #------------------------------------------------------
    def download_notebooks(date="",*orgaos):


        if date == "":
            date = Dejt.get_notebook_date_now()
            date.replace("/","-")

        print("Iniciando download dos cadernos...")

        session = Dejt.initiate_session(date)

        path = f'assets\\pdf\\dejt\\{date.replace("/","-")}\\'

        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)

        files_path = []
        dict_to_iterate = dict()
        
        if len(orgaos) > 0:
            for key, value in Dejt.CADERNOS.items():
                if key in orgaos:
                    dict_to_iterate[key] = value
            files_path = Dejt.download_pdfs(session,dict_to_iterate,date)
            return files_path

        files_path = Dejt.download_pdfs(session,Dejt.CADERNOS,date)

        return files_path
        
    #------------------------------------------------------
    # Get notebooks date from website
    #------------------------------------------------------

    def get_notebook_date_now():
        try:
            responseHTML = requests.get("https://dejt.jt.jus.br/cadernos/dejt.html")
        except Exception as e:
            print(e)
            print('Error status code', responseHTML.status_code, responseHTML.text)

        match_str = re.search(r'\d{2}/\d{2}/\d{4}', responseHTML.text)

        notebooksDate = datetime.strptime(match_str.group(), '%d/%m/%Y').strftime("%d-%m-%Y")

        return notebooksDate

    #------------------------------------------------------
    # Download pdfs
    #------------------------------------------------------

    def download_pdfs(session,dict,date):
        files_path = []
        path = f'assets\\pdf\\dejt\\{date.replace("/","-")}\\'
        orgaos_count = len(dict)

        for index, orgao in enumerate(dict):
                Dejt.PAYLOAD["source"] = Dejt.CADERNOS[orgao]

                download = session.post(Dejt.API_ENDPOINT,data=Dejt.PAYLOAD,headers=Dejt.HEADERS,stream=True)
                total_length = download.headers.get('content-length')
                
                dl = 0
                total_length = int(total_length)
                path_file = os.sep.join([path, orgao+".pdf"])
                file = open(path_file,'wb')
                path_file_validation = os.sep.join([path, orgao+"-validation.txt"])
                file_validation = open(path_file_validation,'w')
                file_validation.write(str(total_length))
                file_validation.close()
                clear()
                print(f"\nFazendo download ({index+1}/{orgaos_count}) do caderno {orgao} de {date}")
                for data in download.iter_content(chunk_size=1096):
                    dl += len(data)
                    file.write(data)
                    done = int(50 * dl / total_length)

                    Progress_bar.print(dl, total_length, prefix = f'Progresso total:', suffix = f'({round(dl/1024000,2)}mb/{round(total_length/1024000,0)}mb) Completo', length = 50)
                    
                
                file.close()
                if os.path.getsize(f"{path}{orgao}.pdf") == total_length:
                    files_path.append(f"{path}{orgao}.pdf")
                else:
                    print("Erro, peso do PDF não bate com o peso do servidor. Baixe novamente.")
                    exit()

        return files_path