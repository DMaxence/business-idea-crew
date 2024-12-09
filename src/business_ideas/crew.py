from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
# Uncomment the following line to use an example of a custom tool
# from business_ideas.tools.custom_tool import MyCustomTool
# Uncomment the following line to use an example of a knowledge source
# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool

@CrewBase
class BusinessIdeas():
	"""BusinessIdeas crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def pull_data_example(self, inputs):
		# Example of pulling data from an external API, dynamically changing the inputs
		inputs['extra_data'] = "This is extra data"
		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def create_business_ideator(self) -> Agent:
		return Agent(
			config=self.agents_config['business_ideator'],
			tools=[SerperDevTool()],
			verbose=True,
			allow_delegation=False,
			llm_config={
				"temperature": 0.7,
				"request_timeout": 120
			}
		)

	@agent
	def create_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['market_analyst'],
			verbose=True,
			tools=[SerperDevTool()],
			allow_delegation=False,
            llm_config={
                "temperature": 0.3,  # Lower temperature for more analytical responses
                "request_timeout": 180
            }
		)

	@agent
	def create_project_coordinator(self) -> Agent:
		return Agent(
			config=self.agents_config['project_coordinator'],
			tools=[SerperDevTool()],
			verbose=True,
            allow_delegation=True,  # This agent needs to delegate to others
            llm_config={
                "temperature": 0.5,
                "request_timeout": 120
            }
		)

	@agent
	def create_prd_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['prd_specialist'],
			tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False,
            llm_config={
                "temperature": 0.4,
                "request_timeout": 150
            }
		)

	@agent
	def create_marketing_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['marketing_strategist'],
			tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False,
            llm_config={
                "temperature": 0.6,
                "request_timeout": 120
            }
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the BusinessIdeas crew"""
		# You can add knowledge sources here
		# knowledge_path = "user_preference.txt"
		# sources = [
		# 	TextFileKnowledgeSource(
		# 		file_path="knowledge/user_preference.txt",
		# 		metadata={"preference": "personal"}
		# 	),
		# ]

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			# knowledge_sources=sources, # In the case you want to add knowledge sources
		)
