import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from typing_extensions import override
from openai import AssistantEventHandler
from . import prompts
from .models import *
from config import ADMIN_ID


class EventHandler(AssistantEventHandler):
    def __init__(self, bot):
        self.bot = bot

    @override
    def on_text_created(self, text) -> None:
        self.bot.send_message(ADMIN_ID, f"\nassistant > ")
        # print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.bot.send_message(ADMIN_ID, delta.value)
        print(delta.value, end="", flush=True)


class GPTProxy:
    def __init__(self, token, model="gpt-3.5-turbo", bot=None):
        self.client = openai.OpenAI(api_key=token)
        self.model = model
        self.assistant_id = "asst_L31dnMUHlUaK60KRxZWfh1ug"
        self.bot = bot

        self.stop_stream("thread_VwfnpzfxF1oPLtZOOTILAWcs", "run_thWnCrJWQecizkVZBblCXXZO")

    def upload_file(self, path, purpose="assistants"):
        result = self.client.files.create(
            file=open(path, "rb"),
            purpose=purpose,
        )
        # file_id = "file-w5QGfWSaEQdwqu2cuWVr7mTm"
        return result.id

    def create_assistant(self, name, instructions, file_ids):
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            tools=[{"type": "retrieval"}],
            instructions=instructions,
            file_ids=file_ids,
        )
        # assistant_id = "asst_L31dnMUHlUaK60KRxZWfh1ug"
        return assistant.id

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id

    def add_message(self, thread_id, message):
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )
        return message

    def run_stream(self, thread_id):
        print("!!!run_stream!!!")
        with self.client.beta.threads.runs.stream(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                instructions=prompts.BIG_KPT,
                event_handler=EventHandler(self.bot),
        ) as stream:
            stream.until_done()

    def stop_stream(self, thread_id, run_id):
        self.client.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run_id,
        )

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
