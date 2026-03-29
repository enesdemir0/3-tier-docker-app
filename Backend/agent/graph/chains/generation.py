from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize Groq LLM
# We use a slightly higher temperature (0.1 or 0.2) to make the text feel more natural
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. The Professional RAG Prompt
template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Question: {question} 
Context: {context} 
Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# 3. Create the Chain
# StrOutputParser just ensures the output is a clean string
generation_chain = prompt | llm | StrOutputParser()