import voyageai

from config import config
from models.models import SearchResult


class VoyageHandler:
    def __init__(self) -> None:
        self.voyage_client = voyageai.AsyncClient(
            api_key=config.voyage_api_key,
            max_retries=3
        )


    async def get_embeddings(self, input_docs, input_type):
        response = await self.voyage_client.embed(
            input_docs,
            model=config.voyage_model,
            input_type=input_type,
            output_dtype="float",
            output_dimension=config.voyage_dimensions,
        )

        return response.embeddings

    async def get_reranking_result(
        self, query: str, documents: list[str], limit: int = 5
    ) -> list[SearchResult]:
        rerank_output = await self.voyage_client.rerank(
            query, documents, model=config.voyage_reranker_model, top_k=limit
        )
        return [
            SearchResult(content=documents[result.index], score=result.relevance_score)
            for result in rerank_output.results
        ]


voyage_handler = VoyageHandler()
