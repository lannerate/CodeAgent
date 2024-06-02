import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process

os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] ='codestral:latest'  # Adjust based on available model
os.environ["OPENAI_API_KEY"] ='ollama'

game = input("What is the game you would like to build? What will be the mechanics?\n")

senior_engineer_agent = Agent(
    role='Senior Software Engineer',
    goal='Create software as needed',
    backstory=dedent("""\Instructions
                        You are a Senior Software Engineer at a leading tech think tank.
                        Your expertise in programming in python. and do your best to
                        produce perfect code"""),
    allow_delegation=False,
    verbose=True
)

qa_engineer_agent = Agent(
    role='Software Quality Control Engineer',
    goal='create prefect code, by analizing the code that is given for errors',
    backstory=dedent("""\
                        You are a software engineer that specializes in checking code
                        for errors. You have an eye for detail and a knack for finding
                        hidden bugs.
                        You check for missing imports, variable declarations, mismatched
                        brackets and syntax errors.
                        You also check for security vulnerabilities, and logic errors"""),
    allow_delegation=False,
    verbose=True
)

chief_qa_engineer_agent = Agent(
    role='Chief Software Quality Control Engineer',
    goal='Ensure that the code does the job that it is supposed to do',
    backstory=dedent("""\
                        You feel that programmers always do only half the job, so you are
                        super dedicate to make high quality code."""),
    allow_delegation=True,
    verbose=True
)

code_task = Task(
    description=dedent(f"""You will create a game using python, these are the instructions:

                            Instructions
                            ------------
                        {game}

                            Your Final answer must be the full python code, only the python code and nothing else.
  			        """),
    expected_output="A complete Python game code implementing all specified mechanics, fully functional and commented.",
    agent=senior_engineer_agent
)

review_task = Task(
    description=dedent(f"""\
                            You are helping create a game using python, these are the instructions:

                            Instructions
                            ------------
                            {game}

                            Using the code you got, check for errors. Check for logic errors,
                            syntax errors, missing imports, variable declarations, mismatched brackets,
                            and security vulnerabilities.

                            Your Final answer must be the full python code, only the python code and nothing else.
  			        """),
    expected_output="An error-checked and corrected Python game code, ensuring no syntax, logical, or security flaws are present.",
    agent=qa_engineer_agent
)

evaluate_task = Task(
    description=dedent(f"""\
                            You are helping create a game using python, these are the instructions:

                            Instructions
                            ------------
                            {game}

                            You will look over the code to insure that it is complete and
                            does the job that it is supposed to do.

                            Your Final answer must be the full python code, only the python code and nothing else.
			            """),
    expected_output="A finalized Python game code that is reviewed for completeness, functionality, and optimization.",
    agent=chief_qa_engineer_agent
)

crew = Crew(
  agents=[senior_engineer_agent, qa_engineer_agent,chief_qa_engineer_agent],
  tasks=[code_task, review_task,evaluate_task],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

game = crew.kickoff()

print("\n\n########################")
print("## Here is the result")
print("########################\n")
print("final code for the game:")
print(game)
