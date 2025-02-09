from beyondllm.llms.base import BaseLLMModel, ModelConfig
from typing import Any, Dict
from dataclasses import dataclass, field
import os

@dataclass
class CohereModel:
    """
    Class representing a Language Model (LLM) model using Cohere.

    Example:
    ```
    >>> llm = CohereModel(api_key="<your_api_key>", model_kwargs={"temperature": 0.5})
    ```
    or
    ```
    >>> import os
    >>> os.environ['COHERE_API_KEY'] = "***********" #replace with your key
    >>> llm = CohereModel()
    ```
    """
    api_key: str =" "
    model_name: str = "command-r-plus-08-2024"
    model_kwargs: dict = field(default_factory=lambda: {
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 2048,
    })
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv('COHERE_API_KEY')
            if not self.api_key:
                raise ValueError("COHERE_API_KEY is not provided and not found in environment variables.")
        self.load_llm()

    def load_llm(self):
        try:
            import cohere
        except ImportError:
            print("The cohere module is not installed. Please install it with 'pip install cohere'.")
        
        try:
            self.client = cohere.ClientV2(api_key=self.api_key)
        except Exception as e:
            raise Exception(f"Failed to initialize Cohere client: {str(e)}")

    def predict(self, prompt: Any) -> str:
        try:
            response = self.client.chat(
                model=self.model_name, 
                messages=[{"role": "user", "content": prompt}]
            )
            return response.message.content[0].text
        except Exception as e:
            raise Exception(f"Failed to generate prediction: {str(e)}")

    @staticmethod
    def load_from_kwargs(self, kwargs: Dict):
        model_config = ModelConfig(**kwargs)
        self.config = model_config
        self.load_llm()
        
