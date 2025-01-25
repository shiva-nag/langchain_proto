from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from third_parties.linkedin_py import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello Langchain")

    summary_template = """
    given the LinkedIn information {information} about a person from, I want you to create:
    1. A Short Summary
    2. A paragraph about why they are an excellent product management leader
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
  #  llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | StrOutputParser()
    linkedin_data = scrape_linkedin_profile(linked_profile_url="https://www.linkedin.com/in/shivashank/")
    res = chain.invoke(input={"information": linkedin_data})

    print(res)
