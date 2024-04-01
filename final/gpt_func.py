from config import GPT_TOKEN


# import openai
#
# openai.api_key = GPT_TOKEN


# async def gpt_ask_func(message):
#     print('starting')
#     try:
#         completion = openai.Completion.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": f"Ты — эксперт-супервизор когнитивно-поведенческой психотерапии. Ответь на запрос психолога:{message}",
#                 }
#             ],
#             model="gpt-3.5-turbo",
#             temperature=0
#         )
#         print(completion)
#         print(completion.choices[0].message.content)
#         return completion.choices[0].message.content
#     except Exception as e:
#         print(e)
#         raise e


def gpt_ask_func(req_mess):
    print('starting')
    from openai import OpenAI
    client = OpenAI(api_key=GPT_TOKEN)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты — эксперт-супервизор когнитивно-поведенческой психотерапии"},
            {"role": "user", "content": f"Ответь на запрос психолога: {req_mess}"}
        ]
    )
    return completion.choices[0].message.content

# def gpt_aask_func(req_mess):
#     print('starting')
#     time.sleep(3)
#     return 'GOOD'
