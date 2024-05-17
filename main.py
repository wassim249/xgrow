import datetime
import os
import time

import crewai
from dotenv import load_dotenv
from termcolor import colored

from agents import XAgents
from tasks import XTasks
from tools import XTools
from utils import fetch_news, save_posted_news

load_dotenv()

agents = XAgents()
tasks = XTasks()
copywriter = agents.content_creator()
graphic_designer = agents.graphic_designer()
social_media_poster = agents.social_media_poster()


def init_crew() -> crewai.Crew:
    """
    Description:
    This function initializes the crew for posting news on social media.

    Returns:
        crewai.Crew: The initialized crew for posting news on social media.
    """
    content_creation_task = tasks.content_creation_task(copywriter)
    image_generation_task = tasks.image_generation_task(
        graphic_designer, [XTools.generate_image], content_creation_task
    )

    social_media_post_task = tasks.social_media_post_task(
        social_media_poster,
        [XTools.post_tweet],
        image_generation_task,
        content_creation_task,
    )
    return crewai.Crew(
        agents=[copywriter, graphic_designer, social_media_poster ],
        tasks=[
            content_creation_task,
            image_generation_task,
            social_media_post_task,
        ],
        max_rpm=30,
        verbose=0
    )


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    print(colored(f"[{get_timestamp()}] Starting XPoster...", 'cyan'))
    while True:
        print(colored(f"[{get_timestamp()}] Getting news...", 'yellow'))
        news = fetch_news(os.getenv("X_USERNAME"))

        print(colored(f"[{get_timestamp()}] News fetched successfully!", 'green'))
        if not news:
            print(colored(f"[{get_timestamp()}] No new news to post.", 'red'))
            time.sleep(60 * 60 * 12)
            continue
        crew = init_crew()
        print(colored("\n".join([f'* {news_item["title"]}' for news_item in news]), 'blue'))
        for news_item in news:

            result = crew.kickoff({"news": news_item["content"]})
            print(colored(f"[{get_timestamp()}] Tweet posted successfully: {result}", 'green'))
            save_posted_news(os.getenv("X_USERNAME"), news_item["title"])
            print(colored(f"[{get_timestamp()}] News saved successfully!", 'green'))
        print(colored(f"[{get_timestamp()}] Waiting for 12 hours before fetching new news...", 'yellow'))
        time.sleep(60 * 60 * 12)
