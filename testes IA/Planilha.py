import openai
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring

# API
openai.api_key = ''

# PLANILHA
def load_spreadsheet(file_path: str) -> pd.DataFrame:
    # Carrega a planilha usando o pandas
    return pd.read_excel(file_path)

# FORMATA PLANILHA PRA IA
def format_spreadsheet_for_gpt(df: pd.DataFrame) -> str:
    # Converte os dados da planilha em formato de texto para ser lido pelo GPT
    formatted_text = "Aqui estão os dados da planilha:\n"
    formatted_text += df.to_string(index=False)  # Remove os índices da tabela
    return formatted_text

# PERGUNTA PRA IA
def ask_question_about_spreadsheet(question: str, formatted_data: str) -> str:
    # Monta o prompt para enviar para a IA (GPT)
    prompt = f"Você tem os seguintes dados de uma planilha:\n{formatted_data}\n\nPergunta: {question}\nResposta:"

    # Chama API
    response = openai.ChatCompletion.create(  
        model="gpt-4-turbo",  # modelo do chat gpt com visual 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150, #quantidade de token
        temperature=0.5 #acertividade 
    )

    # resposta
    return response.choices[0].message["content"].strip()

# abre para selecionar o arquivo e depois para fazer a pergunta
def main():
    # Abrir uma janela para selecionar a planilha
    Tk().withdraw()  # tira a janela de prompt do windows
    file_path = askopenfilename(title="Selecione a Planilha", filetypes=[("Excel Files", "*.xlsx;*.xls;*.csv")])

    if not file_path:  # Se não for selecionado nenhum arquivo
        print("Nenhum arquivo selecionado.")
        return

    # Carrega a planilha
    df = load_spreadsheet(file_path)
    
    # Formatar a planilha para ser entendida pela IA
    formatted_data = format_spreadsheet_for_gpt(df)

    # Perguntar ao usuário qual a dúvida sobre a planilha
    question = askstring("Pergunta", "Digite a dúvida sobre a planilha:")

    if not question:  # Se o usuário não digitar uma pergunta
        print("Nenhuma pergunta fornecida.")
        return

    # Perguntar para a IA
    answer = ask_question_about_spreadsheet(question, formatted_data)
    
    # Exibir a resposta
    print("Resposta da IA:", answer)

# Executando o código
if __name__ == "__main__":
    main()
