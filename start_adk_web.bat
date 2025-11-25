@echo off
REM Helper script to start adk web with session persistence
echo Starting adk web with session persistence...
adk web --session_service_uri "sqlite:///D:/OneDrive/OneDrive/projects/agentic_ai/factchecker_agent/fact_checker_sessions.db"
