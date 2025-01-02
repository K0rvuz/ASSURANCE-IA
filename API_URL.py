import openai
import json

openai.api_key = ""

def API_IMG_URL(model_url, prompt_text, image_url, is_url=False, max_tokens=300):
    if not is_url or not image_url:
        return "URL não foi fornecida ou não é válida"

    try:
        response = openai.ChatCompletion.create(
            model=model_url,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )

        message_content = response.choices[0]["message"]["content"]
        return json.loads(json.dumps(message_content, ensure_ascii=False))
    except Exception as e:
        return f"Erro ao criar a conclusão: {e}"



model_url = "gpt-4o-mini"
prompt_text = "Descreva essa imagem"
image_url = ""  # caminho url
is_url = True

resultado = API_IMG_URL(model_url, prompt_text, image_url, is_url)
print(resultado)
