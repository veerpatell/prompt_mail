#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from promptmail.crew import Promptmail

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

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
