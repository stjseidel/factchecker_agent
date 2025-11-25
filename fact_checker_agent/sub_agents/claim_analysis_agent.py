from google.adk.agents import Agent

from fact_checker_agent.config import config

claim_analysis_agent = Agent(
    name="claim_analysis_agent",
    model=config.model_name,
    # retry_config=config.retry_config,
    description="An agent that reads a text and identifies the main claims that need to be verified.",
    instruction="""
    You are a Claim Analysis Agent. Your task is to extract relevant claims from the provided text for fact-checking purposes.
    Your workflow is as follows:
    1. Receive a source input text string
    2. Identify and extract the main claims that require verification.
    3. Clean and format the extracted claims to ensure readability and coherence.
    4. Return the extracted claims for further analysis by the Fact Checker Agent.
    Always ensure that the extracted claims are accurate and complete to facilitate effective fact-checking.
    Make sure the extracted claims are a list of strings.
    """,
    output_key="extracted_claims",
)