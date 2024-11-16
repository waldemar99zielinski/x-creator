from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from crews.types.post_types import PostChapter

@CrewBase
class PostWriterCrew():
	"""PostWriter crew"""

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	research_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
	writer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

	@agent
	def researcher(self) -> Agent:
		return Agent(
			llm=self.research_llm,
			config=self.agents_config['researcher'],
			verbose=True
		)

	@agent
	def writer(self) -> Agent:
		return Agent(
			llm=self.writer_llm,
			config=self.agents_config['writer'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writer_task'],
			output_pydantic=PostChapter
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PostWriter crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)