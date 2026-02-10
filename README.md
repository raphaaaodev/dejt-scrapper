# DEJT Scrapper

Script em Python para baixar cadernos do **DEJT (Diário Eletrônico da Justiça do Trabalho)**, converter os PDFs para texto e filtrar processos por lista de advogados.

## Funcionalidades

- Download de cadernos (TST/TRTs) direto do portal DEJT.
- Conversão dos PDFs em `.txt` com separação de processos.
- Busca de nomes de advogados dentro dos processos.
- Exportação dos processos encontrados por advogado.
- Geração de arquivo de sumário com totais.

## Requisitos

- Python 3.9+
- Dependências do `requirements.txt`

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

## Configuração

O projeto usa `config.yaml` para parâmetros do DEJT:

- `DEJT.CADERNOS`: mapeamento dos cadernos disponíveis (TST-00, TRT-01 ... TRT-24)
- `DEJT.HEADERS`: cabeçalhos HTTP
- `DEJT.API_ENDPOINT`: endpoint de consulta

> O arquivo já vem preenchido com os cadernos e endpoint padrão.

## Estrutura esperada

Após execução, os artefatos são gravados em:

- `assets/pdf/dejt/<data>/` → PDFs baixados
- `assets/txt/dejt/<data>/` → TXT convertidos
- `assets/processos-exportados/<data>/` → resultados por advogado

## Fluxo de uso (exemplo)

Como o `main.py` está vazio, o uso atual é via chamadas diretas dos módulos.

```python
from module.config import Config
from module.validation import SSLCert
from module.dejt import Dejt
from module.pdf_to_txt import Pdf_to_txt
from module.search import Search

# 1) Carrega configuração
Config.load_config("config.yaml")

# 2) (Opcional) valida certificados SSL
SSLCert.verify_SSLCerts()

# 3) Inicializa configurações do DEJT
Dejt.load_config()

# 4) Baixa os cadernos da data mais recente
pdfs = Dejt.download_notebooks()

# ou para órgãos específicos:
# pdfs = Dejt.download_notebooks("01-01-2025", "TRT-02", "TRT-15")

# 5) Converte PDFs para TXT
txts = Pdf_to_txt.convert_from_list(pdfs)

# 6) Busca processos por advogados
# arquivo com 1 nome por linha
pastas_exportadas = Search.export_needed_processos(
    txts,
    "advogados.txt"
)
```

## Formato do arquivo de advogados

Crie um arquivo `.txt` com um nome por linha, por exemplo:

```txt
Maria Silva
João Pereira
Carlos Souza
```

A busca normaliza o texto para minúsculas e remove espaços antes da comparação.

## Observações

- A data usada nos métodos deve seguir o formato `dd-mm-aaaa`.
- Em caso de erro SSL, adicione certificados `.cer` em `assets/dejt-certification` e rode `SSLCert.verify_SSLCerts()` novamente.
- O código usa separadores de caminho no estilo Windows em alguns pontos; em Linux, prefira validar os diretórios gerados após execução.

## Dependências principais

- `requests`
- `beautifulsoup4`
- `PyMuPDF` (`fitz`)
- `PyYAML`

## Licença

Sem licença definida no repositório até o momento.
