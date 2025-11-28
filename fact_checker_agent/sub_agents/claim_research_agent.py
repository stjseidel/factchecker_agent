from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import google_search

from fact_checker_agent.config import config

claim_research_agent = LlmAgent(
    name="claim_research_agent",
    model=config.model_name,
    # retry_config=config.retry_config,
    description="An agent that takes a list of claims and researches them online using Google Search.",
    instruction="""
    You are a Claim Analysis Agent. Your task is to extract relevant claims from the provided text for fact-checking purposes.
    Your workflow is as follows:
    1. Receive a source input text string
    2. Identify and extract the main claims that require verification.
    3. Clean and format the extracted claims to ensure readability and coherence.
    4. Return the extracted claims for further analysis by the Fact Checker Agent.
    Always ensure that the extracted claims are accurate and complete to facilitate effective fact-checking.
    """,
    tools=[google_search],
    output_key="researched_claims",
)