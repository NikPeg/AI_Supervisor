import openai
from tenacity import retry, stop_after_attempt, wait_fixed

from . import prompts
from .models import *


class GPTProxy:
    def __init__(self, token, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        self.assistant = self.create_assistant("frAId", prompts.BIG_KPT, ["file-w5QGfWSaEQdwqu2cuWVr7mTm"])
        print("ASSISTENT:", self.assistant.id)

    def upload_file(self, path, purpose="assistants"):
        result = self.client.files.create(
            file=open(path, "rb"),
            purpose=purpose,
        )
        file_id = "file-w5QGfWSaEQdwqu2cuWVr7mTm"
        return result.id

    def create_assistant(self, name, instructions, file_ids):
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            tools=[{"type": "retrieval"}],
            instructions=instructions,
            file_ids=file_ids,
        )
        id = 'asst_xdH2czQtprOprz3AcAr6LNCi'
        return assistant.id


    @retry(wait=wait_fixed(21), stop=stop_after_attempt(5))
    def ask(self, request, context=None):
        if context is None:
            context = []
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    MessageDTO(Role.SYSTEM, prompts.BIG_KPT).as_dict(),
                    *[message.as_dict() for message in context],
                    MessageDTO.from_user(request).as_dict(),
                ]
            )

            return completion.choices[0].message.content
        except Exception as e:
            raise e
