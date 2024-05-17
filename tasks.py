from crewai import Task, Agent
from langchain.tools.base import Tool


class XTasks:
    """
    Description:
    This class is responsible for creating crewai tasks.
    """

    @staticmethod
    def content_creation_task(agent: Agent) -> Task:
        """
        Description:
        This function is responsible for creating a task for the content creation agent.
        Args:
            agent (Agent): The content creation agent
            news (str): The news content
        Returns:
            Task: The content creation task
        """
        return Task(
            description="""Create an engaging tweet content that encapsulates key insights.
            MAX CHARACTERS 280 including hashtags and emojis.
            Examples of good tweet content:
            - "I pretty much only trust two LLM evals right now:Chatbot Arena and Locallama 🤖🦙 #LLM #chatbot"
            - "xLSTM is out -- putting  LSTM networks on steroids to become a more than serious LLM competitor. 🚀🧠 #AI #ML"
            - "it's cool how every google search now starts with a wall of LLM slop that is completely useless and takes up half the screen 🤦‍♂️ #LLM #search"
            -  "A new mysterious LLM model has been released, it's called GPT-2, and it's said to be the most powerful LLM model ever created. 🧙‍♂️🔮 #LLM #AI"
            
            News:
            ```
            {news}
            ```
            REMEMBER MAX CHARACTERS 280 including hashtags and emojis!!
            Make Sure to choose the right trending hashtags and emojis to make the tweet more engaging.
            """,
            expected_output="Well-crafted tweet text ready for posting.",
            agent=agent,
        )

    @staticmethod
    def image_generation_task(agent: Agent, tools: list[Tool], post_content: str) -> Task:
        """
        Description:
        This function is responsible for creating a task for the image generation agent.
        Args:
            agent (Agent): The image generation agent
            tools (list): The list of tools
            post_content (str): The tweet content
        Returns:
            Task: The image generation task
        """
        return Task(
            description=f"""Generate an image that complements the tweet content and create the image.The image should be abstract or has a related character to the tweet content.
        
            Good image prompts:
            - Rocket launch in meeting room
            - A llama wearing sunglasses and a bowtie
            - 2 Elephants cartoon sitting inside a huge skate shoe,passing through a street
            - A cat wearing a VR headset and working on a laptop
            
            ** Don't use Robots in your prompt **
            
            Try to be creative and unique,without making the prompt too complex.
            ** You don't have to use the exact prompt, you can use a similar prompt to generate the image. **
            News Content:
            ```	
            {post_content}
            ```
            """,
            expected_output="The full generated image path so it can be uploaded to twitter",
            agent=agent,
            tools=tools,
            context=[post_content]
        )

    @staticmethod
    def social_media_post_task(agent: Agent, tools: list[Tool], image_path: str, post_content: str) -> Task:
        """
        Description:
        This function is responsible for creating a task for the social media poster agent.
        Args:
            agent (Agent): The social media poster agent
            tools (list): The list of tools
            image_path (str): The image path
            post_content (str): The tweet content
        Returns:
            Task: The social media post task
        """
        return Task(
            description=f"""Post the tweet and image to Twitter.
            Tweet:
            ```
            {post_content}
            ```
            Image Path:
            ```
            {image_path}
            ```
            """,
            expected_output="The tweet content that you posted",
            agent=agent,
            tools=tools,
            context=[image_path, post_content]
        )

    @staticmethod
    def verify_tweet_content_task(agent: Agent, tools: list[Tool], tweet: str) -> Task:
        """
        Description:
        This function is responsible for creating a task for the verifier agent.
        Args:
            agent (Agent): The verifier agent
            tools (list): The list of tools
            tweet (str): The tweet content
        Returns:
            Task: The verify tweet content task
        """
        return Task(
            description=f"""Verify and correct the tweet content by making sure it's respects the following criteria:
            - The tweet content should be engaging and informative.
            - The tweet content should be free of grammatical errors.
            - The tweet doesn't use complex words or jargon.
            - The tweet length should not exceed 280 characters (including hashtags and emojis),use the provided tool to verify the tweet length.
            - It should be free of hallucinations or misinformation.
            Tweet:
            ```
            {tweet}
            ```
            """,
            expected_output="Corrected tweet content that meets the mentioned criteria.",
            agent=agent,
            tools=tools,
            context=[tweet]
        )
