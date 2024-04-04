import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import time
from config import GPT_TOKEN

# env variables
load_dotenv()
my_key = GPT_TOKEN

# OpenAI API
client = AsyncOpenAI(api_key=my_key)


async def create_assistant():
    # Create the assistant
    assistant = "asst_L31dnMUHlUaK60KRxZWfh1ug"

    return assistant


async def add_message_to_thread(thread_id, user_question):
    # Create a message inside the thread
    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= user_question
    )
    return message


async def get_answer(assistant_id, thread):
    print("Thinking...")
    # run assistant
    print("Running assistant...")
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if runInfo.completed_at:
            # elapsed = runInfo.completed_at - runInfo.created_at
            # elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            print(f"Run completed")
            break
        print("Waiting 1sec...")
        time.sleep(1)

    print("All done...")
    # Get messages from the thread
    messages = await client.beta.threads.messages.list(thread.id)
    message_content = messages.data[0].content[0].text.value
    return message_content


if __name__ == "__main__":
    async def main():
        # Colour to print
        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'

        # Create assistant and thread before entering the loop
        assistant_id = await create_assistant()
        print("Created assistant with id:" , f"{bcolors.HEADER}{assistant_id}{bcolors.ENDC}")
        thread = await client.beta.threads.create()
        print("Created thread with id:" , f"{bcolors.HEADER}{thread.id}{bcolors.ENDC}")
        while True:
            question = input("How may I help you today? \n")
            if "exit" in question.lower():
                break

            # Add message to thread
            await add_message_to_thread(thread.id, question)
            message_content = await get_answer(assistant_id, thread)
            print(f"FYI, your thread is: , {bcolors.HEADER}{thread.id}{bcolors.ENDC}")
            print(f"FYI, your assistant is: , {bcolors.HEADER}{assistant_id}{bcolors.ENDC}")
            print(message_content)
        print(f"{bcolors.OKGREEN}Thanks and happy to serve you{bcolors.ENDC}")
    asyncio.run(main())