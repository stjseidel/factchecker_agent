#!/usr/bin/env python3
"""Helper script to run adk web with the correct session service URI."""
import subprocess

from fact_checker_agent import session_service_uri

print("Starting adk web with session persistence...")
print(f"Session service URI: {session_service_uri}")
print(f"Database will be stored at: {session_service_uri.replace('sqlite:///', '')}")
print()

cmd = ["adk", "web", "--session_service_uri", session_service_uri]
print(f"Running: {' '.join(cmd)}")
print()

subprocess.run(cmd)
