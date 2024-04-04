import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from typing_extensions import override
from openai import AssistantEventHandler
from . import prompts
from .models import *
from config import ADMIN_ID
from openai import OpenAI, AsyncOpenAI
import time


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
        self.aclient = AsyncOpenAI(api_key=token)

        # self.stop_stream("thread_VwfnpzfxF1oPLtZOOTILAWcs", "run_thWnCrJWQecizkVZBblCXXZO")

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

    async def add_message(self, thread_id, user_question):
        # Create a message inside the thread
        message = await self.aclient.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content= user_question
        )
        return message

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id

    async def get_answer(self, thread_id):
        print("Thinking...")
        # run assistant
        print("Running assistant...")
        run = await self.aclient.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )

        # wait for the run to complete
        while True:
            runInfo = await self.aclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if runInfo.completed_at:
                # elapsed = runInfo.completed_at - runInfo.created_at
                # elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                print(f"Run completed")
                break
            print("Waiting 1sec...")
            time.sleep(1)

        print("All done...")
        # Get messages from the thread
        messages = await self.aclient.beta.threads.messages.list(thread.id)
        message_content = messages.data[0].content[0].text.value
        return message_content

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
