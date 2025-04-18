from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Process, Task, LLM
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
import os
import yaml # Replace with actual embedder class
import os
import openai
from embedchain import App
from crewai_tools import SerperDevTool, PDFSearchTool, TXTSearchTool, CSVSearchTool
import os
from pydantic import SkipValidation
from promptmail.tools import ALL_TOOLS
from promptmail import ALL_TOOLS

   #     search_tool : SerperDevTool(),
    #    pdf_tool: PDFSearchTool(),
     #   txt_tool: TXTSearchTool(),
      #  csv_tool: CSVSearchTool(),
       # scrape_tool : ScrapeWebsiteTool()
    


os.environ["OPENAI_API_KEY"] = 'OPENAI_API_KEY'
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

llm = LLM(
    model="mistral/mistral-large-latest",
    temperature=0.7
)

llmG = LLM(
    model="gemini/gemini-2.0-pro-latest",
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

@CrewBase
class Promptmail:
    agents_config_path = 'config/agents.yaml'
    tasks_config_path = 'config/tasks.yaml'

    @agent
    def client_service_executive(self) -> Agent:
        return Agent(
            config=self.agents_config_path,
            id="client_service_executive",
            verbose=True,
            llm=llmG,
            memory=True,
            long_term_memory=ltm

        )
    
    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config_path,
            id="manager",
            verbose=True,
            llm=llmG,
            memory=True,
            tools=[ALL_TOOLS["search_tool"]],
            long_term_memory=ltm

        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config_path,
            id="researcher",
            verbose=True,
            llm=llmG,
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
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config_path,
            id="email_writer",
            verbose=True,
            llm=llm,
            memory=True,
            long_term_memory=ltm
        )
    @agent
    def scheduler(self) -> Agent:
        return Agent(
            config=self.agents_config_path,
            id="scheduler",
            verbose=True,
            llm=llm,
            memory=True,
            
        )
    @task
    def client_engagement_task(self) -> Task:
        return Task(
            config=self.tasks_config_path,
            id="client_engagement_task"
        )
    
    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config_path,
            id="manager_task"
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config_path,
            id="research_task"
        )

    @task
    def writer_task(self) -> Task:
        return Task(
            config=self.tasks_config_path,
            id="writer_task"
        )
    @task
    def scheduler_task(self) -> Task:
        return Task(
            config=self.tasks_config_path,
            id="scheduler_task"
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
            agents=[self.client_service_executive(), self.manager(), self.researcher(), self.writer(), self.scheduler()],
            tasks=[self.client_engagement_task(), self.research_task(), self.writer_task(), self.scheduler_task()],
            process=Process.hierarchical,
            llm=llmG,
            memory=True,
            long_term_memory=ltm,
            knowledge_sources=sources,
            verbose=True,
            tools = ALL_TOOLS
        )