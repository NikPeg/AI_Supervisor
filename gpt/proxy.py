import openai
from tenacity import retry, stop_after_attempt, wait_fixed

from . import prompts
from .models import *


class GPTProxy:
    def __init__(self, token, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        # results = self.client.files.create(
        #     file=open("gpt/SupervisionKPT.docx", "rb"),
        #     purpose="assistants",
        # )
        # print("upload results: " + str(results) + "\n")
        # print("file_id: " + results.id)
        # file_id = "file-w5QGfWSaEQdwqu2cuWVr7mTm"
        #
        # assistant = self.client.beta.assistants.create(
        #     model=model,
        #     name="frAId supervisor",
        #     tools=[{"type": "retrieval"}],
        #     instructions=prompts.KPT,
        #     file_ids=[file_id],
        # )
        # Assistant(id='asst_xdH2czQtprOprz3AcAr6LNCi', created_at=1712142908, description=None, file_ids=['file-w5QGfWSaEQdwqu2cuWVr7mTm'], instructions='Ты — эксперт-супервизор когнитивно-поведенческой психотерапии. Ответь на запрос психолога, который к тебе обратился. Ты получишь $1000 за хороший ответ.', metadata={}, model='gpt-4-0125-preview', name='frAId supervisor', object='assistant', tools=[RetrievalTool(type='retrieval')])
        # print(assistant)


    @retry(wait=wait_fixed(21), stop=stop_after_attempt(5))
    def ask(self, request, context=None):
        if context is None:
            context = []
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    MessageDTO(Role.SYSTEM, prompts.KPT).as_dict(),
                    *[message.as_dict() for message in context],
                    MessageDTO.from_user(request).as_dict(),
                ]
            )

            return completion.choices[0].message.content
        except Exception as e:
            raise e
