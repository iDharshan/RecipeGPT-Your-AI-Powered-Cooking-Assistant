import os
from constants import azure_openai_api_key, azure_openai_endpoint
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains import LLMChain
import streamlit as st

os.environ['AZURE_OPENAI_API_KEY'] = azure_openai_api_key
os.environ['OPENAI_API_VERSION'] = "2023-03-15-preview"
os.environ['AZURE_OPENAI_ENDPOINT'] = azure_openai_endpoint

st.title("RecipeGPT: Your AI-Powered Cooking Assistant")
user_input = st.chat_input("Enter the ingredients you have")


first_input_prompt = PromptTemplate(
    input_variables=["ingredients"],
    template= "What recipe can I make with these {ingredients}. just provide the recipe name."
)
second_input_prompt = PromptTemplate(
    input_variables=["recipe"],
    template= "Provide a step-by-step cooking guide to make {recipe}."
)

llm = AzureChatOpenAI(
    azure_deployment="openai_langchain",
    temperature=0.8
)

chain = LLMChain(llm=llm, prompt=first_input_prompt,verbose=True,output_key='recipe')
chain2 = LLMChain(llm=llm, prompt=second_input_prompt,verbose=True,output_key='guide')

parent_chain = SequentialChain(chains=[chain,chain2],input_variables=["ingredients"],output_variables=["recipe","guide"],verbose=True)

if user_input:

    st.chat_message('user').write(user_input)

    response = parent_chain.invoke({"ingredients": user_input})
    recipe = response['recipe']
    guide = response['guide']

    st.chat_message('assistant').write(f"Here is a recipe you can make with {user_input}: {recipe}")
    st.chat_message('assistant').write(f"Here is a step-by-step guide to make {recipe}: {guide}")

