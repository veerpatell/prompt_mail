from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Process, Task, LLM
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
import os
import yaml
import os
import openai
from embedchain import App
from crewai_tools import SerperDevTool, PDFSearchTool, TXTSearchTool, CSVSearchTool
import os
from pydantic import SkipValidation
from promptmail.tools import ALL_TOOLS
from promptmail import ALL_TOOLS



#os.environ["OPENAI_API_KEY"] = 'OPENAI_API_KEY'
os.environ['MISTRAL_API_KEY'] = 'c1w0IxaIrpg5q65Zq9pX5vMcTc2lJxMp'


llm = LLM(
    model="mistral/mistral-large-latest",
    temperature=0.7
)

llmG = LLM(
    model="gemini/gemini-1.5-pro",
    temperature=0.7,
)

ltm = LongTermMemory(
    storage=LTMSQLiteStorage(db_path="./memory.db")
)

short_term_memory = ShortTermMemory(
        storage = RAGStorage(
                embedder_config={
                    "provider": "openai",
                    "config": {
                        "model": 'text-embedding-3-small'
                    }
                },
                type="short_term",
                path="/knowledge/"
            )
        )

entity_memory = EntityMemory(
        storage=RAGStorage(
            embedder_config={
                "provider": "openai",
                "config": {
                    "model": 'text-embedding-3-small'
                }
            },
            type="short_term",
            path="/knowledge/"
        )
    )

with open('src/promptmail/config/agents.yaml', 'r') as a_file:
    AGENTS_CONFIG = yaml.safe_load(a_file)

with open('src/promptmail/config/tasks.yaml', 'r') as t_file:
    TASKS_CONFIG = yaml.safe_load(t_file)

@CrewBase
class Promptmail:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config['manager'],
            verbose=True,
            llm=llm,
            human_imput = True,
            memory=True,
            long_term_memory=ltm
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            llm=llm,
            memory=True,
            long_term_memory=ltm,
            tools = [
            ALL_TOOLS["search_tool"],
            ALL_TOOLS["pdf_tool"],
            ALL_TOOLS["txt_tool"],
            ALL_TOOLS["csv_tool"]
            ]
        )


    @agent
    def email_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['email_writer'],
            verbose=True,
            llm=llm,
            memory=True,
            long_term_memory=ltm
        )
    @agent
    def scheduler(self) -> Agent:
        return Agent(
            config= self.agents_config['scheduler'],
            verbose=True,
            llm=llm,
            memory=True
            
        )

    @task
    def manager_delegation_task(self) -> Task:
        return Task(
            config=self.tasks_config['manager_delegation_task']
        )
    
    @task
    def researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config['researcher_task']
        )

    @task
    def writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['writer_task']
        )
    @task
    def scheduler_task(self) -> Task:
        return Task(
            config=self.tasks_config['scheduler_task']
        )
    
    @crew
    def crew(self, inputs=None) -> Crew:
        sources = []
        if inputs:
            if inputs.get("pdf_files"):
                sources.append(PDFKnowledgeSource(file_paths=inputs["pdf_files"]))
            if inputs.get("csv_files"):
                sources.append(CSVKnowledgeSource(file_paths=inputs["csv_files"]))

        return Crew(
            agents=[ self.researcher(), self.email_writer(), self.scheduler()],
            tasks=[self.manager_delegation_task(), self.researcher_task(), self.writer_task(), self.scheduler_task()],
            process=Process.hierarchical,
            manager_agent= self.manager(),
            llm=llm,
            memory=True,
            long_term_memory=ltm,
            knowledge_sources=sources,
            verbose=True,
            tools = ALL_TOOLS
        )