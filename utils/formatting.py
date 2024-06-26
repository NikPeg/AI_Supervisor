import re


def markdown_to_html(s):
    # Сначала заменяем **жирный** текст
    s = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", s)

    # Затем заменяем *курсивный* текст
    s = re.sub(r"\*(.*?)\*", r"<i>\1</i>", s)

    # Заменяем заголовки
    s = re.sub(r"^### (.*?)\n", r"<b>\1</b>\n", s)
    s = re.sub(r"\n### (.*?)\n", r"\n<b>\1</b>\n", s)
    s = re.sub(r"\n### (.*?)\n", r"\n<b>\1</b>\n", s)
    s = re.sub(r"\n### (.*?)$", r"\n<b>\1</b>", s)
    return s
