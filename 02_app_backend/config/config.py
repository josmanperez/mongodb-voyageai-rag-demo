import os
from dotenv import load_dotenv

# Take environment variables from .env and load them into os.environ
load_dotenv()

# MongoDB configs
mongodb_conn_str = os.getenv("MONGO_CONN_STR")
mongodb_db_name = "test_voyage_rag"
mongodb_coll_name = "mongodb_search_kb"
mongodb_vector_index_name = "test_voyage_rag_vector"
mongodb_fulltext_index_name = "test_voyage_rag_fulltext"

# Voyage AI configs
voyage_api_key = os.getenv("VOYAGEAI_API_KEY")
voyage_model = "voyage-4"
voyage_dimensions = 1024
voyage_reranker_model = "rerank-2.5"

# if use_local_llm is True, LM Studio is used as LLM provider
# otherwise, Anthropic model is used.
use_local_llm = False

# LM Studio configs
lmstudio_model = "google/gemma-4-e4b"
lmstudio_provider = "openai"
lmstudio_base_url = "http://localhost:1234/v1"
lmstudio_api_key = "lm-studio"
lmstudio_temperature = 0

# LLM configs
anthropic_model_id = "claude-haiku-4-5"
anthropic_version = "2023-06-01"
anthropic_api_url = os.getenv("ANTHROPIC_API_URL")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic_max_tokens = 1000
anthropic_temperature = 0
