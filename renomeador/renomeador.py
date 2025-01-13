import os
import re
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np

# Configuração do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\vinicius\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def melhorar_imagem(img):
    """
    Aplica processamento para melhorar a qualidade da imagem.
    """
    # Converte para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplica binarização
    _, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    
    # Remove ruídos com operações morfológicas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    img_morph = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)
    
    # Aumenta a imagem
    scale_percent = 200  # Aumentar 200%
    width = int(img_morph.shape[1] * scale_percent / 100)
    height = int(img_morph.shape[0] * scale_percent / 100)
    img_resized = cv2.resize(img_morph, (width, height), interpolation=cv2.INTER_CUBIC)
    
    return img_resized

def extrair_texto_pdf(caminho_pdf):
    """
    Converte cada página do PDF para uma imagem e usa OCR para extrair o texto.
    """
    imagens = convert_from_path(caminho_pdf, poppler_path=r"C:\poppler\Library\bin")
    texto = ""
    for imagem in imagens:
        # Converte a imagem PIL para formato OpenCV
        img_cv = np.array(imagem)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
        
        # Aplica melhorias na imagem
        img_processada = melhorar_imagem(img_cv)
        
        # Extrai texto com OCR
        texto += pytesseract.image_to_string(img_processada, lang="por")
    return texto

def renomear_pdfs(diretorio, padroes):
    """
    Renomeia arquivos PDF no diretório com base nos padrões fornecidos.
    """
    contador = 1
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(diretorio, arquivo)
            
            # Extrai o texto do PDF usando OCR
            texto = extrair_texto_pdf(caminho)
            
            # Tenta encontrar o número da nota fiscal em sequência nos padrões fornecidos
            numero_nf = None
            for padrao in padroes:
                resultado = re.search(padrao, texto)
                if resultado:
                    numero_nf = resultado.group(1)
                    break
            
            # Renomeia o arquivo ou usa um contador
            if numero_nf:
                novo_nome = f"{numero_nf}.pdf"
            else:
                novo_nome = f"NF_{contador}.pdf"
                contador += 1

            novo_caminho = os.path.join(diretorio, novo_nome)
            os.rename(caminho, novo_caminho)
            print(f"Renomeado: {arquivo} -> {novo_nome}")

# Exemplo de uso
diretorio_pdfs = r"C:\Users\vinicius\Desktop\renomeador\pdfs"
padroes_nf = [
    r"Nº\s*(\d{3}\.\d{3}\.\d{3})",  # "Nº xxx.xxx.xxx"
    r"No\.\s*(\d+)",                # "No. xxxxxxxxx"
    r"Nº\s*(\d+)",                  # "Nº xxxxxxxxx"
]
renomear_pdfs(diretorio_pdfs, padroes_nf)
