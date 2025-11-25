import os
from dataclasses import dataclass

from google.genai import types
import google.auth

# To use AI Studio credentials:
# 1. Create a .env file in the /app directory with:
#    GOOGLE_GENAI_USE_VERTEXAI=FALSE
#    GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
# 2. This will override the default Vertex AI configuration
_, quota_project_id = google.auth.default()
quota_project_id = 'gen-lang-client-0588241039'
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", quota_project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

@dataclass
class FactCheckerAgentConfig:
    """Configuration for the Fact Checker Agent.
    
    Attributes:
        model_name (str): The name of the language model to use.
        retry_config (types.HttpRetryOptions): Configuration for HTTP retries.
    """
    model_name: str = "gemini-2.5-flash"
    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )


config = FactCheckerAgentConfig()
