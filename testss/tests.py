import os
import warnings
from dotenv import load_dotenv

from sqlalchemy.exc import SAWarning
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent  # ✅ fixed import

from tool import get_sql_tools

# 🔷 Suppress SQLAlchemy warnings
warnings.filterwarnings("ignore", category=SAWarning)

# 🔷 Load .env variables
load_dotenv()

postgres_uri = os.getenv("POSTGRES_URI")
groq_api_key = os.getenv("GROQ_API_KEY")

if not postgres_uri:
    raise ValueError("POSTGRES_URI not set in your .env file")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not set in your .env file")

# 🔷 Database & LLM
db = SQLDatabase.from_uri(postgres_uri)
llm = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)

def test_tools():
    print("\n🧪 ====== Testing Tools ======\n")
    tools = get_sql_tools(db, llm)

    print("\n▶️ Testing: get_schema")
    schema_result = tools["get_schema"].invoke("emp, dept")
    print(schema_result)

    print("\n▶️ Testing: create_sql_query")
    query_result = tools["create_sql_query"].invoke('SELECT "ENAME" FROM emp LIMIT 5')
    print(query_result)

    print("\n▶️ Testing: execute_sql_query")
    checker_result = tools["execute_sql_query"].invoke('SELECT "ENAME" FROM emp LIMIT 5')
    print(checker_result)

def test_agent():
    print("\n🤖 ====== Testing Agent ======\n")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )

    question = "List all users in the employees database."
    print(f"🧠 Asking: {question}\n")
    response = agent_executor.invoke({"input": question})["output"]  # ✅ .invoke instead of .run
    print(f"\n✅ Answer: {response}")

if __name__ == "__main__":
    test_tools()
    test_agent()
