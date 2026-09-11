from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class SearchResult(BaseModel):
    content: str
    score: float

class MultipleChoiceAnswer(BaseModel):
    answer: Literal["A", "B", "C", "D"] = Field(
        description="The correct answer to the question. You must select A, B, C, or D."
    )

class State(BaseModel):
    question: Optional[str] = None
    use_rag: Optional[bool] = None
    use_hybrid: Optional[bool] = None
    use_reranker: Optional[bool] = None
    question_embedding: Optional[List[float]] = None
    search_results: Optional[List[SearchResult]] = None
    reranking_results: Optional[List[SearchResult]] = None
    reference_docs: Optional[List[str]] = None
    input_tokens: Optional[int] = None
    llm_answer: Optional[MultipleChoiceAnswer] = None

class AnswerQuestionRequest(BaseModel):
    question: str 
    use_rag: bool
    use_hybrid: bool 
    use_reranker: bool 

class AnswerQuestionResponse(BaseModel):
    operation_id: str 
    llm_answer: Literal["A", "B", "C", "D"]
    input_tokens: int
    reference_docs: List[str]
