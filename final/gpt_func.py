from openai import OpenAI

from config import GPT_TOKEN


def gpt_ask_func(req_mess):
    client = OpenAI(api_key=GPT_TOKEN)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты — эксперт-супервизор когнитивно-поведенческой психотерапии"},
            {"role": "user", "content": f"Ответь на запрос психолога: {req_mess}"}
        ]
    )
    return completion.choices[0].message.content
