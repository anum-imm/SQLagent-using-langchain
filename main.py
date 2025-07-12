import os
from dotenv import load_dotenv
import warnings
from sqlalchemy.exc import SAWarning
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit


warnings.filterwarnings("ignore", category=SAWarning)

load_dotenv()

postgres_uri = os.getenv("POSTGRES_URI")
groq_api_key = os.getenv("GROQ_API_KEY")

if not postgres_uri or not groq_api_key:
    raise ValueError("POSTGRES_URI and GROQ_API_KEY must be set in the .env file")

db = SQLDatabase.from_uri(postgres_uri)
llm = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key)

from sqlagent import create_agent
from langchain_community.utilities import SQLDatabase



# Create the SQL Agent
agent = create_agent(db, llm)

print("✅ SQL Agent created successfully.")
print("👉 Starting test query…\n")
while True:
    # Take question from user
    question = input("\n📝 Enter your question (or type 'exit' to quit): ").strip()
    
    # Exit condition
    if question.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break

    # Run the agent with streaming & pretty print
    print(f"\n🤖 Answering: {question}\n")
    for step in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
