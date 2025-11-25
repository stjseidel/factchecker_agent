from google.adk.agents import Agent

from fact_checker_agent.config import config

claim_check_agent = Agent(
    name="claim_check_agent",
    model=config.model_name,
    # retry_config=config.retry_config,
    description="An agent that uses the list of claims and the research findings to verify the accuracy of each claim.",
    instruction="""
    You are a Claim Check Agent. Your task is to compare the main findings from your research with the original claims.
    Your workflow is as follows:
    1. Receive a list of claims and the research findings for each claim.
    2. For each claim, compare the research findings with the original statement to determine its accuracy.
    3. Classify each claim as True, False, Misleading, or Unverifiable based on the evidence gathered.
    4. Provide a brief explanation for each classification, citing the sources used in your research.
    5. Return the verified claims along with their classifications and explanations for further analysis by the Fact Checker Agent.
    Always ensure that your verifications are thorough and based on credible evidence to facilitate effective fact-checking.
    """,
    output_key="extracted_text",
)