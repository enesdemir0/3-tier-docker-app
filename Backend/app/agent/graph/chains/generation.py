from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize Groq LLM
# We use a slightly higher temperature (0.1 or 0.2) to make the text feel more natural
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. The Professional RAG Prompt
template = """You are a highly professional AI Research Assistant. 
Your goal is to provide a clean, expert-level answer based ONLY on the provided context.

Context: 
{context}

Question: 
{question}

Instructions:
1. Use a professional and academic tone.
2. If the context doesn't contain the answer, say you don't know.
3. Do not mention "Based on the documents provided" - just give the answer.
4. If there is messy data or JSON in the context, ignore the code and focus only on the meaning.

Expert Answer:"""
prompt = ChatPromptTemplate.from_template(template)

# 3. Create the Chain
# StrOutputParser just ensures the output is a clean string
generation_chain = prompt | llm | StrOutputParser()