def test_llm():
    from agent import llm
    from langchain_core.messages import HumanMessage
    resp = llm([HumanMessage(content="hi")])
    assert resp is not None
    print("✅ LLM working:", resp)

def test_tools():
    from agent import tools
    assert "get_schema" in tools
    result = tools["get_schema"].run("dept")
    assert result is not None
    print("✅ Tools working: get_schema returned:", result)

def test_system_prompt():
    from agent import system_prompt
    assert "{dialect}" not in system_prompt
    assert "PostgreSQL" in system_prompt
    print("✅ System prompt looks good:\n", system_prompt)

def test_agent():
    from agent import agent
    result = agent.invoke("List all departments.")
    assert result is not None
    print("✅ Agent responded:", result)

if __name__ == "__main__":
    test_llm()
    test_tools()
    test_system_prompt()
    test_agent()
