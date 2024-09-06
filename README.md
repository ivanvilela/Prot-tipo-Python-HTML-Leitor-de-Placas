# Teste Leitor de Placas

Este projeto é um protótipo de um leitor de placas de veículos utilizando Python e Tesseract OCR.

## Instruções de Uso

1. **Instalar o Tesseract OCR:**
   - Baixe e instale o Tesseract OCR a partir do seguinte link: [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
   - Certifique-se de instalar todas as linguagens disponíveis para evitar erros durante o reconhecimento de texto.

2. **Baixar o Código:**
   - Faça o download do código-fonte disponível neste repositório.

3. **Instalar as Dependências:**
   - Abra o terminal no Visual Studio Code ou em seu ambiente preferido.
   - Execute o comando abaixo para instalar todas as bibliotecas necessárias:
     ```bash
     pip install Flask opencv-python numpy imutils pytesseract
     ```

4. **Executar o Código:**
   - Execute o script principal com o seguinte comando:
     ```bash
     python app.py
     ```
     

   **Caso ocorrer este erro: "error: pytesseract.pytesseract.TesseractError: (1, 'Error opening data file tessdata/eng.traineddata Please make sure the TESSDATA_PREFIX environment variable is set to your "tessdata" directory. Failed loading language \'eng\' Tesseract couldn\'t load any languages! Could not initialize tesseract.')"**
   - Abra o terminal no Visual Studio Code e execute os seguintes comandos:
     ```bash
     mkdir tessdata
     wget -O ./tessdata/por.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata?raw=true
     wget -O ./tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata?raw=true
     ```
   - Certifique-se de que a pasta `tessdata` no diretório do projeto contém os arquivos `por.traineddata` e `eng.traineddata`.
   - Se o erro persistir adicione PREFIX_DATA como variável ambiente de sistema:
     1. Pressione a tecla Windows e busque por "Editar variáveis ambiente de sistema".
     2. Clique em "Variáveis de Ambiente" no canto inferior direito.
     3. No painel "Variáveis do Sistema", clique em "Novo".
     4. Defina o nome da variável como `TESSDATA_PREFIX`.
     5. Clicar em "Novo"
     6. Nome da variável: TESSDATA_PREFIX
     7. Defina o valor da variável como o caminho onde o Tesseract está instalado, por exemplo: `C:\Program Files\Tesseract-OCR`.
    
   - Certifique-se de reiniciar o terminal ou o ambiente de desenvolvimento após adicionar a variável de ambiente para que as mudanças tenham efeito.

