import certifi
import requests
import os

class SSLCert:

    def verify_SSLCerts():
        # add first the main certificate X.509 base 64 (*.cer), and run. Do the same for the children.
        # from https://appdividend.com/2022/01/29/python-certifi/

        API_ENDPOINT = "https://dejt.jt.jus.br/dejt/f/n/diariocon"

        try:
            print('Checking connection to website...')
            test = requests.head(API_ENDPOINT)
            print('Connection to the website OK.')
        except requests.exceptions.SSLError as err:
            print('Erro SSL. Adicionando certificados personalizados.')
            SSLCert.fix_SSLCerts()
            
    def fix_SSLCerts():
        dir_with_certs = r".\assets\dejt-certification"

        files = os.listdir(dir_with_certs)

        files_certs = [certificate for certificate in files if certificate.endswith('.cer')]

        cafile = certifi.where()
        outfile = open(cafile, 'ab')
        for cert_file in files_certs:
            path_file = os.sep.join([dir_with_certs, cert_file])
            with open(path_file, 'rb') as infile:
                custom_ca = infile.read()
                infile.close()
            outfile.write(custom_ca)
        outfile.close()

        print('Problema provavelmente resolvido!')