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
        file_id = "file-w5QGfWSaEQdwqu2cuWVr7mTm"
        results = self.client.fine_tuning.jobs.create(training_file=file_id, model=model)
        print("fine-tuning results: " + str(results) + "\n")
        print("jobs: ", self.client.fine_tuning.jobs.list(limit=10))
        # client.fine_tuning.jobs.retrieve("ftjob-abc123")
        #
        # # Cancel a job
        # client.fine_tuning.jobs.cancel("ftjob-abc123")
        #
        # # List up to 10 events from a fine-tuning job
        # client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-abc123", limit=10)


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
