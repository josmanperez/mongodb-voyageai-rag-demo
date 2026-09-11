from fastapi import FastAPI, HTTPException
import uuid
import logging

from providers.langgraph_provider import langgraph_provider
from models.models import AnswerQuestionRequest, AnswerQuestionResponse

app = FastAPI()

@app.get("/healthcheck")
async def health():
    return {"status":"OK"}

@app.post("/answer_question")
async def answer_question(request: AnswerQuestionRequest) -> AnswerQuestionResponse:    
    operation_id = str(uuid.uuid4())

    agent_result_status = await langgraph_provider.answer_question(
        question=request.question,
        use_rag=request.use_rag,
        use_hybrid=request.use_hybrid,
        use_reranker=request.use_reranker
    )
    
    return AnswerQuestionResponse(
        operation_id = operation_id,
        llm_answer = agent_result_status.llm_answer.answer,
        input_tokens = agent_result_status.input_tokens,
        reference_docs = agent_result_status.reference_docs or []
    )
