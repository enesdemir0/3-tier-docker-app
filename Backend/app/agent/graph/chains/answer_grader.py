from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq # Swapped from OpenAI
from pydantic import BaseModel, Field
import os


class GradeAnswer(BaseModel):
    # KEEP THIS AS BOOL (as you requested)
    binary_score: bool = Field(
        description="Answer addresses the question, Use true or false" # Updated description
    )


llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """You are a grader assessing whether an answer addresses / resolves a question. \n 
     Give a binary score 'true' or 'false'. 
     'true' means that the answer resolves the question. 
     'false' means it does not."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader