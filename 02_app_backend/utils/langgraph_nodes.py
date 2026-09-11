from langchain_core.messages import HumanMessage, SystemMessage

from providers.llm_provider import llm_provider
from providers.voyage_handler import voyage_handler
from providers.mongo_handler import mongo_handler

from models.models import State
from config.logger import logger

import textwrap
import time

async def get_question_embedding(state: State) -> State:
    # To prevent errors in case the required inputs are undefined
    if state.question is None or state.use_rag is None:
        return State()

    if state.use_rag is False:
        return State()

    embedding_result = await voyage_handler.get_embeddings(
        input_docs = [state.question], 
        input_type = "query"
    )

    return State(question_embedding=embedding_result[0])


async def run_search(state: State) -> State:
    # To prevent errors in case the required inputs are undefined
    if state.question is None or state.question_embedding is None or state.use_hybrid is None or state.use_reranker is None:
        return State()

    num_results = 10
    if state.use_reranker is True:
        # Higher number of search results.
        # Results will be filtered by the reranker later in the pipeline.
        num_results = 25

    search_results = await mongo_handler.search_chunks(
        plaintext_query = state.question,
        query_embedding = state.question_embedding,
        use_hybrid = state.use_hybrid,
        limit=num_results
    )

    reference_docs = [x.content for x in search_results]

    return State(
        search_results=search_results,
        reference_docs=reference_docs
    )


async def rerank_results(state: State) -> State:
    # To prevent errors in case the required inputs are undefined
    if state.question is None or state.reference_docs is None or state.use_reranker is None:
        return State()

    if state.use_reranker is False:
        return State()

    search_results = await voyage_handler.get_reranking_result(
        query = state.question,
        documents = state.reference_docs,
        limit = 5
    )

    reference_docs = [x.content for x in search_results]

    return State(
        reranking_results=search_results,
        reference_docs=reference_docs
    )


async def get_answer_from_llm(state: State) -> State:

    # To prevent errors in case the question is undefined
    if state.question is None:
        return State()

    system_prompt = ""

    if state.reference_docs is not None:
        if len(state.reference_docs) > 0:
            system_prompt = textwrap.dedent(f"""
                Answer the question using the following reference material and picking the correct answer among the proposed alternatives.
    
                REFERENCE MATERIALS:
                {"\n\n".join(state.reference_docs)}
            """)

    if len(system_prompt)==0:
        system_prompt = "Answer the question to the best of your knowledge, picking the correct answer among the proposed alternatives."
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state.question)
    ]

    input_tokens = llm_provider.llm.get_num_tokens_from_messages(messages)

    start_time = time.perf_counter()
    llm_output = await llm_provider.structured_llm.ainvoke(messages)  
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    logger.info(f"LLM call returned in {execution_time:.4f} seconds")
    return State(input_tokens=input_tokens, llm_answer=llm_output)

