from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize Groq LLM
# We use a slightly higher temperature (0.1 or 0.2) to make the text feel more natural
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
template = """You are a highly professional AI Research Assistant.

Context: 
{context}

Question: 
{question}

Instructions:
1. Only provide factual information. 
2. If the context contains social media posts (like Facebook or Reddit), treat them with caution. 
3. Do not report rumors or obvious jokes (like "Skynet") as facts.
4. If you don't find a clear, factual answer, just say you don't know.

Expert Answer:"""
prompt = ChatPromptTemplate.from_template(template)

# 3. Create the Chain
# StrOutputParser just ensures the output is a clean string
generation_chain = prompt | llm | StrOutputParser()