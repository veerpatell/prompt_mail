#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from promptmail.crew import Promptmail
from promptmail.tools import search_tool, pdf_tool, txt_tool, csv_tool, scrape_tool 
import pydantic
import os
from pydantic import BaseModel
from typing import List

class PromptMailState(BaseModel):
    industry: str = ""
    companies: List[str] = []
    email_format: str = ""

 
class MyModel(pydantic.BaseModel):
    class Config:
        validation = False
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# flows/promptmail_flow.py
from crewai.flow.flow import Flow, start, listen


class PromptMailFlow(Flow[PromptMailState]):

    @start()
    def ask_industry(self):
        return "Hi there! 👋 To get started, is there a **specific industry** you'd like to target (e.g., logistics, manufacturing, healthcare)? Or should I suggest some based on common automation needs?"

    @listen(ask_industry)
    def ask_companies(self):
        return "Great! Do you have **specific companies** in mind you'd like to target? If not, I can research leads in your chosen industry."

    @listen(ask_companies)
    def ask_email_format(self):
        return (
            "Do you have a **preferred format** for your outreach emails?\n\n"
            "You can pick from these frameworks:\n"
            "- PAS (Problem-Agitate-Solution)\n"
            "- AIDA (Attention-Interest-Desire-Action)\n"
            "- Demo pitch format\n\n"
            "Or feel free to share an example/template if you already use one."
        )

    @listen(ask_email_format)
    def confirm_all_inputs(self):
        return (
            "Awesome — here's a quick recap of what I gathered:\n"
            f"- Industry: {{ state.industry }}\n"
            f"- Companies: {{ state.companies }}\n"
            f"- Email Format: {{ state.email_format }}\n\n"
            "Shall I go ahead and delegate tasks to the Researcher and Writer agents to get your campaign started?"
        )


def run():
    """Run the full PromptMail crew from beginning (starts with Client Service Executive)."""
    try:
        Promptmail().crew().kickoff(inputs={})
    except Exception as e:
        print(f"❌ Error while running PromptMail: {e}")


def train():
    """Train PromptMail agents using CLI arguments."""
    if len(sys.argv) < 4:
        print("Usage: python main.py train <iterations> <filename>")
        return
    try:
        Promptmail().crew().train(
            n_iterations=int(sys.argv[2]),
            filename=sys.argv[3],
            inputs={}
        )
    except Exception as e:
        print(f"❌ Error while training: {e}")

def replay():
    """Replay PromptMail from a task ID."""
    if len(sys.argv) < 3:
        print("Usage: python main.py replay <task_id>")
        return
    try:
        Promptmail().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        print(f"❌ Error while replaying: {e}")

def test():
    """
    Test PromptMail crew execution with a dynamic topic.
    Usage: python main.py test <iterations> <model_name> <topic>
    """
    if len(sys.argv) < 5:
        print("Usage: python main.py test <iterations> <model_name> <topic>")
        return

    try:
        n_iterations = int(sys.argv[2])
        model_name = sys.argv[3]
        topic = sys.argv[4]

        Promptmail().crew().test(
            n_iterations=n_iterations,
            model_name=model_name,  # <-- Renamed for general use
            inputs={"topic": topic}
        )
    except Exception as e:
        print(f"❌ Error while testing PromptMail: {e}")
