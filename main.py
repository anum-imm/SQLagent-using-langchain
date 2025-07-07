import os
from dotenv import load_dotenv
import warnings
from sqlalchemy.exc import SAWarning
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

warnings.filterwarnings("ignore", category=SAWarning)

load_dotenv()

postgres_uri = os.getenv("POSTGRES_URI")
groq_api_key = os.getenv("GROQ_API_KEY")

if not postgres_uri or not groq_api_key:
    raise ValueError("POSTGRES_URI and GROQ_API_KEY must be set in the .env file")

db = SQLDatabase.from_uri(postgres_uri)
llm = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=False)

print("SQL Agent ready. Type your question, or 'exit' to quit.\n")

while True:
    question = input("📝 Question: ").strip()
    if question.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break
    if not question:
        continue

    try:
        result = agent_executor.invoke({"input": question})
        print(f"Answer: {result['output']}\n")
    except Exception as e:
        print(f"⚠️ Error: {e}\n")
