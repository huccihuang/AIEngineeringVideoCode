import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system', "You are a recipe recommendation assistant, you need to recommend suitable dishes and give recipes based on the given food ingredients, which include every step of cooking."),
        ('human', "{ingredients}")
    ]
)

model = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
)

def output_parser(output:str):
    translate_model = ChatOpenAI(
        model="glm-3-turbo",
        temperature = 0.01,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
    )
    message = """You are a translation assistant. No matter what text you receive, translate it into Chinese.
    This is the text you need to translate:`{text}`"""
    return translate_model.invoke(message.format(text=output))

chain = prompt_template | model | output_parser
while True:
    ingredients = input('What ingredients do you have？\n')
    answer = chain.invoke(input = {'ingredients': ingredients})
    print(answer.content)

    next_round = input('Do you have other ingredients?(y/n)\n')
    if next_round.lower() != 'y':
        break