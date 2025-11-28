from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import google_search

from fact_checker_agent.config import config

source_reliability_agent = LlmAgent(
    name="source_reliability_agent",
    model=config.model_name,
    # retry_config=config.retry_config,
    description="An agent that takes a list of sources and evaluates their reliability using Google Search.",
    instruction="""
    You are a Source Reliability Agent. Your task is to evaluate the reliability of the provided sources for fact-checking purposes.
    Your workflow is as follows:
    1. Receive a list of sources (URLs, document titles, publication names, etc.)
    2. Evaluate the credibility of each source using Google Search and other available tools.
    3. Assign a reliability score to each source based on factors such as reputation, authoritativeness, and recency.
    4. Return the evaluated sources along with their reliability scores for further analysis by the Fact Checker Agent.
    Always ensure that the reliability assessments are accurate and comprehensive to facilitate effective fact-checking.
    """,
    tools=[google_search],
    output_key="evaluated_sources",
)
