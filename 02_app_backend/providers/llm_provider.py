from langchain.chat_models import init_chat_model
from langchain_anthropic import ChatAnthropic

from config import config
from models.models import MultipleChoiceAnswer

class LLMProvider():

    def __init__(self) -> None:
        if config.use_local_llm is True:
            llm = init_chat_model(
                model=config.lmstudio_model,
                model_provider=config.lmstudio_provider,
                base_url= config.lmstudio_base_url,
                api_key=config.lmstudio_api_key,
                temperature=config.lmstudio_temperature,
                # Using chatGPT tokenizer for a ballpark token count estimate
                tiktoken_model_name="gpt-3.5-turbo"
            )
        else:
            llm = ChatAnthropic(
                model=config.anthropic_model_id,
                temperature=config.anthropic_temperature,
                max_tokens=config.anthropic_max_tokens,
                base_url=config.anthropic_api_url,
                api_key=config.anthropic_api_key, 
                default_headers={
                    "api-key": config.anthropic_api_key,
                    "anthropic-version": config.anthropic_version
                }
            )

        self.llm = llm
        self.structured_llm = llm.with_structured_output(MultipleChoiceAnswer)

llm_provider = LLMProvider()
