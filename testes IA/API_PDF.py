import openai 
import base64 
import fitz  

# Chave da API
openai.api_key = ""

# Codifica para b64 para que o código seja capaz de ler a imagem
def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Analisa a imagem com IA
def analyze_image_with_openai(image_bytes: bytes) -> dict:
    # Codifica a imagem para Base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data_url = f"data:image/jpeg;base64,{image_base64}"

    # Prompt fixo
    vision_prompt = """
    Você tem a tarefa de analisar uma imagem. Forneça as seguintes informações:
    - Uma breve descrição da imagem.
    - Uma lista dos principais objetos na imagem.

    Retorne o resultado como um objeto JSON no seguinte formato:
    {
        "Descrição_da_imagem": "...",
        "Principais_objetos": ["...", "..."]
    }
    """

    # Chama a API OpenAI com o formato correto
    response = openai.ChatCompletion.create(  # Corrigido para ChatCompletion
        model="gpt-4-turbo",  # Modelo com visão
        messages=[{
            "role": "user", 
            "content": vision_prompt + f"\nImage: {image_data_url}"
        }],
        max_tokens=500,
        temperature=0
    )

    # Retorna o conteúdo gerado pela API
    return response.choices[0].message["content"]

# Função para extrair imagens do PDF
def extract_images_from_pdf(pdf_path: str) -> list:
    images_data = []
    pdf_document = fitz.open(pdf_path)

    for page_number, page in enumerate(pdf_document, start=1):
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            images_data.append({
                "page": page_number,
                "image_bytes": image_bytes
            })

    return images_data

# Processa o PDF e analisa as imagens uma a uma
def process_pdf_and_describe_images(pdf_path: str) -> list:
    extracted_images = extract_images_from_pdf(pdf_path)
    results = []

    for idx, image_data in enumerate(extracted_images):
        print(f"Analisando imagem {idx + 1} na página {image_data['page']}...")
        description = analyze_image_with_openai(image_data["image_bytes"])
        results.append({
            "page": image_data["page"],
            "description": description
        })

    return results

# Analisa uma imagem única
def analyze_single_image(image_path: str) -> dict:
    # Codificar a imagem
    image_bytes = open(image_path, "rb").read()
    description = analyze_image_with_openai(image_bytes)
    return description

# Função principal para processar o PDF e/ou imagem
def analyze_image_or_pdf(input_path: str, is_pdf: bool = False) -> list:
    if is_pdf:
        # Se for um PDF, processa as imagens dentro dele
        return process_pdf_and_describe_images(input_path)
    else:
        # Caso contrário, analisa a imagem única fornecida
        description = analyze_single_image(input_path)
        return [{"page": "N/A", "description": description}]

# Executando 
if __name__ == "__main__":
    input_path = r"pdf\triagem_neonatal_biologica_manual_tecnico.pdf"  # Caminho do arquivo
    is_pdf = False  # True para PDF     e      False para Imagem
    results = analyze_image_or_pdf(input_path, is_pdf)

    #  resultado
    for idx, result in enumerate(results):
        print(f"Resultado da Imagem {idx + 1} (Página {result['page']}):")
        print(result["description"])
        print("-" * 50)
