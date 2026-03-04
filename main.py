from langchain_ollama import ChatOllama
#from langchain_core.messages, import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="minimax-m2.5:cloud",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","you are expert at {topic}, give course, answer question, explain concept"),
        ("human","{question}")
    ]
)
chain = prompt | llm | StrOutputParser()
#messages=[
    #SystemMessage(content="You are a helpful assistant that translates English to French."),
    #HumanMessage(content="Translate the following English text to French: 'Hello, how are you]

for chunk in chain.stream({"topic": "AI", "question": "What is AI?"}):
    print(chunk, end="", flush=True )
