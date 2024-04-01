from config import GPT_TOKEN
import openai
from tenacity import retry, wait_fixed, stop_after_attempt


class GPTProxy:
    def __init__(self, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=GPT_TOKEN)
        self.model = model

    @retry(wait=wait_fixed(21), stop=stop_after_attempt(10))
    def ask(self, request):
        try:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты — эксперт-супервизор когнитивно-поведенческой психотерапии."},
                    {"role": "user", "content": f"Ответь на запрос психолога: {request}"}
                ]
            )

            return completion.choices[0].message.content
        except Exception as e:
            print(e)
            raise e
