import logging
from pathlib import Path

from google.adk.agents import SequentialAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.models import Gemini
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer

from fact_checker_agent.config import config

from fact_checker_agent.sub_agents import (
    claim_text_extractor_agent,
    claim_analysis_agent,
    claim_research_agent,
    source_reliability_agent,
    claim_check_agent
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# from fact_checker_agent.tools import save_fact_check_to_file

fact_checker_agent = SequentialAgent(
    name="fact_checker_agent",
    # model=config.model_name,
    description="An agent that verifies facts using reliable sources.",
    # instruction="""
    # You are a Fact Checker Agent. Your task is to verify the accuracy of statements by consulting reliable sources.
    
    # Your workflow is as follows:
    # 1. claim_text_extractor_agent: Receive a statement or link so a source (text, pdf, social media post, video, ...) that needs fact-checking.
    # 2. claim_analysis_agent: Analyze the text to identify the main claims that need verification.
    # 3. claim_research_agent: research each claim using trusted databases, official reports, and credible news outlets.
    # 4. source_reliability_agent: Assign a reliability score to each source you use based on its credibility.
    # 5. claim_check_agent: Compare the main findings from your research with the original claims.
    # 6. Generate a detailed report that includes:
    #     - The original claims.
    #     - The evidence found for or against each claim.
    #     - The reliability scores of the sources used.
    #     - A final verdict on the accuracy of each claim (True, False, Misleading, etc.).
    #     Always prioritize accuracy and reliability in your assessments.
    # In general, follow the workflow, and refrain from asking questions. The purpose is to take the statement or text, find claims, research them, evaluate sources, and verify claims.
    # Follow the entire workflow step-by-step to ensure thorough fact-checking. The only step you may skip is the claim_text_extractor_agent if the input is already plain text containing claims.
    # """,
    sub_agents=[
        claim_text_extractor_agent,
        claim_analysis_agent,
        claim_research_agent,
        source_reliability_agent,
        claim_check_agent,

    ],
    # tools=[
    #     FunctionTool(save_fact_check_to_file),
    # ],
    # output_key="result",
    # retry_config=config.retry_config,
)

# 2. Create a summarizer with a specific model for compaction.
# This model will be used to summarize the events.
compaction_summarizer = LlmEventSummarizer(
    llm=Gemini(model=config.model_name) # Or another model of your choice
)

# Configure the app with compaction settings
app = App(
    name='fact_checker_agent',
    root_agent=fact_checker_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Trigger compaction every 3 new invocations.
        overlap_size=1,          # Include last invocation from the previous window.
        summarizer=compaction_summarizer
    ),
)

# Database configuration for session persistence
# Note: When using 'adk web', pass the --session_service_uri flag to specify the database
# Example: adk web --session_service_uri "sqlite:///./fact_checker_sessions.db"
# For programmatic use with create_runner(), we use the async driver:
repo_root = Path(__file__).resolve().parents[1]
db_path = repo_root / "fact_checker_sessions.db"
db_url = f"sqlite:///{db_path.as_posix()}"  # For programmatic use (async)
session_service_uri = f"sqlite:///{db_path.as_posix()}"  # For adk web (sync)


def create_runner():
    """Create a runner with session persistence for standalone/programmatic use."""
    try:
        session_service = DatabaseSessionService(db_url)
        logging.info("Successfully created DatabaseSessionService with URL: %s", db_url)
        return Runner(app=app, session_service=session_service)
    except Exception as e:
        logging.warning("Failed to create database engine for URL '%s' (%s). Falling back to runner without persistence.", db_url, e)
        return Runner(app=app)


# Export the agent for adk web and other uses
# adk web will use the 'app' if it exists, otherwise just the root_agent
root_agent = fact_checker_agent
