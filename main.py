# import os
# from dotenv import load_dotenv
# import warnings
# from sqlalchemy.exc import SAWarning
# from langchain_community.utilities import SQLDatabase
# from langchain_groq import ChatGroq
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from langchain_community.agent_toolkits.sql.base import create_sql_agent

# warnings.filterwarnings("ignore", category=SAWarning)

# load_dotenv()

# postgres_uri = os.getenv("POSTGRES_URI")
# groq_api_key = os.getenv("GROQ_API_KEY")

# if not postgres_uri or not groq_api_key:
#     raise ValueError("POSTGRES_URI and GROQ_API_KEY must be set in the .env file")

# db = SQLDatabase.from_uri(postgres_uri)
# llm = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)

# toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=False)

# print("SQL Agent ready. Type your question, or 'exit' to quit.\n")

# while True:
#     question = input("📝 Question: ").strip()
#     if question.lower() in {"exit", "quit"}:
#         print("👋 Goodbye!")
#         break
#     if not question:
#         continue

#     try:
#         result = agent_executor.invoke({"input": question})
#         print(f"Answer: {result['output']}\n")
#     except Exception as e:
#         print(f"⚠️ Error: {e}\n")
import os
import warnings
from dotenv import load_dotenv
from sqlalchemy.exc import SAWarning

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent

from tool import get_custom_sql_tools  # your custom tools

# Load environment variables
load_dotenv()

# Suppress SQLAlchemy warnings
warnings.filterwarnings("ignore", category=SAWarning)

# Read environment variables
POSTGRES_URI = os.getenv("POSTGRES_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not POSTGRES_URI or not GROQ_API_KEY:
    raise ValueError("Both POSTGRES_URI and GROQ_API_KEY must be set in your .env file.")

# Initialize database and LLM
db = SQLDatabase.from_uri(POSTGRES_URI)
llm = ChatGroq(model="llama3-70b-8192", api_key=GROQ_API_KEY)

# Get custom SQL tools
tools = get_custom_sql_tools(db, llm)

# Initialize the agent executor
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=True
)

print("✅ SQL Agent ready. Type your question, or 'exit' to quit.\n")

# Main interactive loop
while True:
    question = input("📝 Question: ").strip()
    if question.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break
    if not question:
        continue

    try:
        result = agent_executor.invoke({"input": question})
        print(f"💡 Answer: {result['output']}\n")
    except Exception as e:
        print(f"⚠️ Error: {e}\n")
