from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from crews.types.post_types import PostTeaser

@CrewBase
class PostTeaserWriterCrew():
	"""PostTeaserWriter crew"""

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	writer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=True
		)

	@task
	def write_post_teaser(self) -> Task:
		return Task(
			config=self.tasks_config['write_teaser'],
			output_pydantic=PostTeaser
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PostTeaserWriter crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
