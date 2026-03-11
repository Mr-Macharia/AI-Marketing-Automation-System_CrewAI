import os
from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import TavilySearchTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()


os.environ["CREWAI_TELEMETRY_DISABLED"] = "true"


llm=LLM(
    model=os.environ["MODEL"],
    base_url=os.environ["AZURE_API_BASE"],
    api_key=os.environ["AZURE_API_KEY"],
    api_version=os.environ["AZURE_API_VERSION"],
    temperature=0.8
)

_tools = [
    DirectoryReadTool(directory='resources/drafts'),
    FileReadTool(),
    FileWriterTool(),
    TavilySearchTool(),
    ScrapeWebsiteTool(),
]

# llm=LLM(
#     model="cerebras/llama-3.3-70b",
#     temperature=0.8

# )

class Content(BaseModel):
    content_type: str = Field(...,description="The type of content to be created (e.g., blog post, social media post, video)")
    topic:str = Field(..., description="The topic of the content")
    target_audience:str = Field(..., description="The target audience for the content")
    tags: List[str] = Field(..., description="Tags to be used for the content")
    content: str = Field(..., description="The content itself")

@CrewBase
class MarketingCrew:
    """
    The marketing crew is responsible for creating and executing marketing strategies,content creation,and managing marketing campaigns.
    """
    agents_config="config/agents.yaml"
    tasks_config="config/tasks.yaml"

    @agent
    def head_of_marketing(self) -> Agent:
        return Agent(
            config=self.agents_config['head_of_marketing'],     # type: ignore[index]
            tools=_tools,
            llm=llm,
        )

    @agent
    def content_creator_social_media(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator_social_media'],      # type: ignore[index]
            llm=llm,
            tools=_tools
        )

    @agent
    def content_writer_blogs(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer_blogs'],      # type: ignore[index]
            llm=llm,
            tools=_tools
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],        # type: ignore[index]
            llm=llm,
            tools=_tools
        )

    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config['market_research']     # type: ignore[index]
        )

    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_marketing_strategy']          # type: ignore[index]
        )

    @task
    def create_content_calendar(self) -> Task:
        return Task(
            config=self.tasks_config['create_content_calendar']         # type: ignore[index]
        )

    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_post_drafts'] # type: ignore[index]        
            #output_json=Content
        )

    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_scripts_for_reels']           # type: ignore[index]
            #output_json=Content
        )

    @task
    def content_research_for_blogs(self) -> Task:
        return Task(
            config=self.tasks_config['content_research_for_blogs']          # type: ignore[index]
        )

    @task
    def draft_blogs(self) -> Task:
        return Task(
            config=self.tasks_config['draft_blogs']         # type: ignore[index]
            #output_json=Content
        )

    @task
    def seo_optimization(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization']            # type: ignore[index]
            #output_json=Content
        )

    @crew
    def marketing_crew(self) -> Crew:
        """Creates the Marketing Crew"""
        return Crew(
            agents=self.agents,     # type: ignore[attr-defined]
            tasks=self.tasks,       # type: ignore[attr-defined]
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,
            max_rpm=2
        )

if __name__ == '__main__':

    """REQUIRED_DIRS = [
        "resources/drafts",
        "resources/drafts/posts",
        "resources/drafts/reels",
    ]

    for d in REQUIRED_DIRS:
        os.makedirs(d, exist_ok=True)"""

    inputs={
        "product_name": "AI Tech Influencer",
        "target_audience": "Tech and Programming Enthusiasts",
        "product_description": "An AI Agent or Identity that creates awareness who you can talk to and chat with online.",
        "budget": "Ksh. 100,000",
    }
    crew=MarketingCrew()
    crew.marketing_crew().kickoff(inputs=inputs)            # type: ignore[attr-defined]
    print("Marketing Crew successfully created and run.")