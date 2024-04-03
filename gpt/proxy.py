import openai
from tenacity import retry, stop_after_attempt, wait_fixed

from . import prompts
from .models import *


class GPTProxy:
    def __init__(self, token, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        results = openai.files.create(
            file=open("gpt/SupervisionKPT.docx", "rb"),
            purpose='assistants'
        )
        print("upload results: " + str(results) + "\n")
        print("file_id: " + results.id)
        results = openai.FineTuningJob.create(training_file=results.id, model=model)
        print("fine-tuning results: " + str(results) + "\n")
        print("\nUse the following command to check the status of your fine-tuning job:")
        print(f"results.id: {results.id}")

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
