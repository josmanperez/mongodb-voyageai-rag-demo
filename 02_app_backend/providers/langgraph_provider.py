from langgraph.graph import END, START, StateGraph

from models.models import State
from utils import langgraph_nodes

class LangGraphProvider:

    def __init__(self) -> None:
        builder = StateGraph(State)

        # add graph nodes
        builder.add_node("get_question_embedding", langgraph_nodes.get_question_embedding)
        builder.add_node("run_search", langgraph_nodes.run_search)
        builder.add_node("rerank_results", langgraph_nodes.rerank_results)
        builder.add_node("get_answer_from_llm", langgraph_nodes.get_answer_from_llm)

        # add graph edges
        builder.add_edge(START, "get_question_embedding")
        builder.add_edge("get_question_embedding", "run_search")
        builder.add_edge("run_search", "rerank_results")
        builder.add_edge("rerank_results", "get_answer_from_llm")
        builder.add_edge("get_answer_from_llm", END)

        self.graph = builder.compile()


    async def answer_question(self, question:str, use_rag:bool, use_hybrid:bool, use_reranker:bool) -> State:
        initial_state = State(
            question = question,
            use_rag=use_rag,
            use_hybrid=use_hybrid,
            use_reranker=use_reranker
        )
        result_state = await self.graph.ainvoke(initial_state)
        result_state_obj = State( **result_state )

        return result_state_obj


langgraph_provider = LangGraphProvider()
