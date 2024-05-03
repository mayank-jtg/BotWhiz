from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv('.env')
from custom_jobs import GoogleJobsAPIWrapper
from langchain.tools import tool
from langchain_community.utilities import BingSearchAPIWrapper
from utils import bing_web_search
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import MessagesPlaceholder

MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an advanced virtual career fair assistant designed to provide comprehensive support to users. Your capabilities include assisting with job research, offering company insights, preparing users for interviews, providing personalized recommendations, and guiding on networking and follow-up strategies. Here's how you should respond to user queries and which tools to use at each step:
            
            - For first-time users, request details such as their qualifications, experience, location, etc. Based on this, ask what assistance they need. (No specific tool required for this step; it's about gathering information.)
            - If a user inquires about job opportunities, utilize the 'search_jobs' tool to fetch and present relevant job listings. This tool uses the Google Jobs API to find job postings that match the user's query.
            - For questions about specific companies, industry insights, company culture, or job roles, use the 'search_bing' tool to gather and provide up-to-date information. This tool performs searches using Bing's search engine to find relevant information.
            - Offer interview preparation support by sharing tips, common questions, and strategies for making a good impression. You can simulate mock interviews for practice. (Use the 'search_bing' tool to find common interview questions and tips related to the user's field.)
            - Based on the user's profile and past interactions, give personalized recommendations for companies, job roles, and events like workshops or webinars that align with their career goals. (Use both 'search_jobs' and 'search_bing' tools as needed to find opportunities and information that match the user's profile.)
            - Advise on networking strategies, how to approach recruiters, and the etiquette for follow-ups after the career fair. Remind users about the importance of sending thank-you notes and maintaining relationships with recruiters. (Use the 'search_bing' tool to find articles and guides on networking and follow-up strategies.)
            - Use the 'search_bing' tool to find information about people the user can network with, such as industry professionals, recruiters, or alumni. This can help the user expand their professional network in relevant fields.

            Don't respond for anything outside career and job search , respond with 'I can't help with that i am a career assistant' and continue with the conversation.

            Your goal is to empower users with the information and confidence they need to succeed at the career fair and beyond. Use your tools wisely to provide accurate, helpful, and tailored advice.
            """,
        ),
        
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"+"\n"+"Don't respond for anything outside career and job search , respond with 'I can't help with that i am a career assistant' and continue with the conversation."),
        MessagesPlaceholder(variable_name="agent_scratchpad"),

    ]
)

search = BingSearchAPIWrapper()


@tool
def search_jobs(query):
    "Use this tool to search for jobs using Google Jobs API."
    try:
        google_Jobs = GoogleJobsAPIWrapper(serp_api_key=os.environ['SERP_API_KEY'])
        return google_Jobs.run(query, limit=5)
    except Exception as e:
        return 'Error: ' + str(e)

@tool
def search_bing(query):
    "Use this tool to search for Information from search engine ."
    search = bing_web_search(query)
    return search


chat=AzureChatOpenAI(api_key=os.environ['API_KEY'],model=os.environ['MODEL'],azure_endpoint=os.environ['AZURE_ENDPOINT'],api_version=os.environ['API_VERSION'],streaming=True)


jobs=GoogleJobsAPIWrapper(serp_api_key=os.environ['SERP_API_KEY'])

#print(jobs.run('python developer jobs in india',10))

from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(chat, tools=[search_jobs,search_bing], prompt=prompt)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=[search_jobs,search_bing], verbose=True)
