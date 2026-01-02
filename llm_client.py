import os
from groq import Groq
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"  
class GroqLlamaClient:
    """
    Thin wrapper around Groq chat.completions API for LLaMA.
    """

    def __init__(self, api_key: str | None = None):
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment.")
        self.client = Groq(api_key=api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 512,
    ) -> str:
        """
        Send chat completion request and return assistant content.
        """
        completion = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content.strip()
