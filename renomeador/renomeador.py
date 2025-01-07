import os
import re
from pdf2image import convert_from_path
import pytesseract

# Configuração do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\vinicius\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extrair_texto_pdf(caminho_pdf):
    """
    Converte cada página do PDF para uma imagem e usa OCR para extrair o texto.
    """
    imagens = convert_from_path(caminho_pdf, poppler_path=r"C:\poppler\Library\bin")
    texto = ""
    for imagem in imagens:
        texto += pytesseract.image_to_string(imagem, lang="por")
    return texto

def renomear_pdfs(diretorio, padrao):
    """
    Renomeia arquivos PDF no diretório com base no padrão fornecido.
    """
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(diretorio, arquivo)
            
            # Extrai o texto do PDF usando OCR
            texto = extrair_texto_pdf(caminho)
            
            # Busca o número da nota fiscal no texto usando o padrão
            resultado = re.search(padrao, texto)
            if resultado:
                numero_nf = resultado.group(1)
                novo_nome = f"{numero_nf}.pdf"
                novo_caminho = os.path.join(diretorio, novo_nome)
                
                # Renomeia o arquivo
                os.rename(caminho, novo_caminho)
                print(f"Renomeado: {arquivo} -> {novo_nome}")
            else:
                print(f"Número da nota fiscal não encontrado em {arquivo}")

# Exemplo de uso
diretorio_pdfs = r"C:\Users\vinicius\Desktop\renomeador\pdfs"
padrao_nf = r"No\.\s*(\d+)"  # Busca o padrão "No. xxxxxxxxx"
renomear_pdfs(diretorio_pdfs, padrao_nf)
