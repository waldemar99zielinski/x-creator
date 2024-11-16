from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from tools.browser_tool import BrowserTools
from crews.types.post_types import PostOutline

@CrewBase
class PostOutlinerCrew():
	"""PostOutliner crew"""

	browser_tools = BrowserTools()

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	research_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
	outliner_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

	@agent
	def researcher(self) -> Agent:
		return Agent(
			llm=self.research_llm,
			config=self.agents_config['researcher'],
			tools=[
				*self.browser_tools.get_all_tools(),
			],
			verbose=True
		)

	@agent
	def outliner(self) -> Agent:
		return Agent(
			llm=self.outliner_llm,
			config=self.agents_config['outliner'],
			
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task 
	def outline_task(self) -> Task:
		return Task(
			config=self.tasks_config['outline_task'],
			output_pydantic=PostOutline
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PostOutliner crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)