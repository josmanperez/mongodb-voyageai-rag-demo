import logging

from pymongo import AsyncMongoClient

from config import config
from models.models import SearchResult

logger = logging.getLogger(__name__)


class MongoHandler:
    def __init__(self) -> None:
        self.client = AsyncMongoClient(config.mongodb_conn_str)
        db = self.client[config.mongodb_db_name]
        self.chunks_coll = db[config.mongodb_coll_name]


    async def search_chunks(self, plaintext_query: str, query_embedding: list[float], use_hybrid:bool, limit: int = 10) -> list[SearchResult]:
        """Hybrid search on chunk text."""

        intermediate_stage_limit = limit*2

        # when setting numCandidates, we follow the best practices described here:
        # https://www.mongodb.com/docs/vector-search/query/aggregation-stages/vector-search-stage/?deployment-type=atlas&embedding=byo&interface=driver&language=python#fields
        vector_stage_num_candidates = min(1000, 20*intermediate_stage_limit)

        vector_search_stage = {
            "$vectorSearch": {
                "index": "test_voyage_rag_vector",
                "path": "voyage4-float",
                "queryVector": query_embedding,
                "numCandidates": vector_stage_num_candidates,
                "limit": intermediate_stage_limit
            }
        }

        vector_search_pipeline = [ vector_search_stage ]

        fulltext_search_pipeline = [
            {
                "$search": {
                    "index": "test_voyage_rag_fulltext",
                    "text": {
                    "query": plaintext_query,
                    "path": "content"
                    }
                }
            },
            { 
                "$limit": intermediate_stage_limit
            }
        ]

        hybrid_search_stage = {
            "$scoreFusion": {
                "input": {
                    "pipelines": {
                        "vectorPipeline": vector_search_pipeline,
                        "fullTextPipeline": fulltext_search_pipeline
                    },
                    "normalization": "minMaxScaler"
                },
                "combination": {
                    "weights": {
                        "vectorPipeline": 1,
                        "fullTextPipeline": 1
                    }
                },
                "scoreDetails": True
            }
        }

        final_project_stage = {
            "$project": {
                "_id": 0,
                "content": 1,
                "score": {"$meta": "score"}
            }
        }

        if use_hybrid is True:
            pipeline = [
                hybrid_search_stage,
                final_project_stage,
                { 
                    "$limit": limit
                }
            ]
        else:
            pipeline = [
                vector_search_stage,
                final_project_stage,
                { 
                    "$limit": limit
                }
            ]

        cursor = await self.chunks_coll.aggregate(pipeline)

        results_list = []
        async for temp_result in cursor:
            results_list.append(SearchResult(**temp_result))

        return results_list


mongo_handler = MongoHandler()
