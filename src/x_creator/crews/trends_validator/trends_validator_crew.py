from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from crews.types.topic_types import SelectedTopic
from tools.browser_tool import BrowserTools

@CrewBase
class TrendsValidatorCrew():
	"""TrendsValidator crew"""

	browser_tools = BrowserTools()

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

	@agent
	def trends_analyst(self) -> Agent:
		return Agent(
			llm=self.llm,
			config=self.agents_config['trends_analyst'],
			tools=[
				*self.browser_tools.get_all_tools(),
			],
			verbose=True
		)

	@task
	def trends_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['trends_analyst_task'],
			output_pydantic=SelectedTopic
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TrendsValidator crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)