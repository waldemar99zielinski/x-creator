from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from tools.browser_tool import BrowserTools

from crews.types.topic_types import TopicProposalList

@CrewBase
class TopicResearchCrew():
	"""TopicResearch crew"""

	browser_tools = BrowserTools()

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

	@agent
	def researcher(self) -> Agent:
		return Agent(
			llm=self.llm,
			config=self.agents_config['researcher'],
			tools=self.browser_tools.get_all_tools(),
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_pydantic=TopicProposalList
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TopicResearch crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)