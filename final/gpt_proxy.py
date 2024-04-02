from dataclasses import dataclass, asdict
import enum
import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from prompts import KPT_PROMPT


class Role(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class MessageDTO:
    role: Role
    content: str


class GPTProxy:
    def __init__(self, token, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=token)
        self.model = model

    @retry(wait=wait_fixed(21), stop=stop_after_attempt(5))
    def ask(self, request, context=None):
        if context is None:
            context = []
        print("ASKING")
        print([
            {"role": "system", "content": KPT_PROMPT},
            *[asdict(message) for message in context],
            {"role": "user", "content": f"Ответь на запрос психолога: {request}"}
        ])
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": KPT_PROMPT},
                    *[asdict(message) for message in context],
                    {"role": "user", "content": f"Ответь на запрос психолога: {request}"}
                ]
            )

            return completion.choices[0].message.content
        except Exception as e:
            print(e)
            raise e
