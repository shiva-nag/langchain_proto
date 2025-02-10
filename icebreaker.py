from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from output_parser import summary_parser
#from langchain_ollama import ChatOllama

from third_parties.linkedin_py import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linked_profile_url=linkedin_url, mock=True)

    summary_template = """
        given the LinkedIn information {information} about a person from, I want you to create:
        1. A Short Summary
        2. Two interesting facts about them
        
        \n{format_instructions}
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
 #   llm = ChatOllama(model="llama3")

   # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser
#    linkedin_data = scrape_linkedin_profile(linked_profile_url="https://www.linkedin.com/in/shivashank/")
    res = chain.invoke(input={"information": linkedin_data})

    print(res)


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker")
    ice_break_with(name="Shiva Nagarajan Tekion")


