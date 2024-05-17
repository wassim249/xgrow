import os
from textwrap import dedent

from crewai import Agent
from langchain_groq import ChatGroq

from tools import XTools


class XAgents:
    """
    Description:
    This class is responsible for creating crewai agents.
    """

    def __init__(self):
        self.main_llm = ChatGroq(model_name="llama3-70b-8192",
                                 groq_api_key=os.getenv("GROQ_API_KEY"),
                                 temperature=1)
        self.verifier_llm = ChatGroq(model_name="llama3-70b-8192",
                                        groq_api_key=os.getenv("GROQ_API_KEY"),
                                        temperature=0)

    def content_creator(self) -> Agent:
        """
        Description:
        The content creator agent is responsible for creating the tweet based on the provided information.
        Returns:
        Agent: The content creator agent
        """
        return Agent(
            role="Creative Content Creator",
            goal=dedent("""\
                Craft clear, engaging, and informative copy based on research
                findings ,The result should be full of information's ,and avoid motivational and non sense content"""),
            backstory=dedent("""\Crafting compelling narratives for social media, you turn dry data into engaging stories that captivate"
                            and inform the digital audience."""),
            llm=self.main_llm,
            allow_delegation=False,
            verbose=False,

        )

    def social_media_poster(self) -> Agent:
        """
        Description:
        The social media poster agent is responsible for posting the final tweet and image to Twitter efficiently.
        """
        return Agent(
            role="Social Media Poster",
            goal="Post the final tweet and image to Twitter efficiently",
            backstory=(
                "In charge of managing social media posts, you ensure that all content is uploaded promptly and accurately"
                "to maximize reach and engagement."
            ),
            tools=[
                XTools.post_tweet
            ],
            llm=self.main_llm,
            allow_delegation=False,
            verbose=False,

        )

    def graphic_designer(self) -> Agent:
        """
        Description:
        The graphic designer agent is responsible for generating the tweet image based on the generated tweet.
        Returns:
        Agent: The graphic designer agent
        """
        return Agent(
            role='Graphic Designer',
            goal='Create visually appealing images to complement tweets',
            backstory=(
                "With a keen eye for design, you produce striking visuals that enhance the impact of digital content,"
                "making each tweet visually engaging and more likely to capture attention."
            ),
            tools=[
                XTools.generate_image
            ],
            llm=self.main_llm,
            allow_delegation=False,
            max_iter=3,
            verbose=False,

        )
    #agent responsible for verifying and reviewing the generated content
    def verifier(self) -> Agent:
        """
        Description:
        The verifier agent is responsible for verifying and reviewing the generated content.
        Returns:
        Agent: The verifier agent
        """
        return Agent(
            role='Content quality assurance specialist',
            goal='Verify and review the generated content,to ensure it meets the required quality,and guarantee high engagement',
            backstory=(
                "With a critical eye for detail, you review and verify the generated content to ensure it meets the"
                "required quality standards and is engaging for the audience. Your feedback helps improve the overall"
            ),
            llm=self.verifier_llm,
            allow_delegation=False,
            verbose=False,
        )
