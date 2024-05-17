# XGrow Twitter Bot

This project automates posting tweets on Twitter about AI news articles. The bot scrapes AI news articles, generates tweets, creates related images, and posts the tweets. The process is repeated periodically to ensure the latest AI news is posted.

## Features

- Scrape AI news articles
- Generate tweet content from news articles
- Generate a related thumbnail image for each tweet
- Post tweets on Twitter
- Repeat the process for new AI news

## How it works

1. The bot scrapes the featured AI news articles from https://www.artificialintelligence-news.com/.
   * Example: 
   ```json
    {
         "title": "GPT-4o delivers human-like AI interaction with text, audio, and vision integration",
         "link": "https://www.artificialintelligence-news.com/2024/05/14/gpt-4o-human-like-ai-interaction-text-audio-vision-integration/",
         "content": "OpenAI has launched its new flagship model, GPT-4o, which seamlessly integrates text, audio, and visual inputs and outputs, promising to enhance the naturalness of machine interactions..."
    }
    ```
2. Then,this article content will be sent to Crew that uses Llama-3-70b from Groq to generate a tweet.
   * Example:
   <em> Meet GPT-4o, the game-changing AI model that combines text, audio, and vision integration for human-like interactions! 🤖?💻 Response times as quick as 232ms, mirroring human conversational speed. A new era of natural machine interactions has begun! #GPT4o #AI #OmniModal 📚 </em>

3. The generated tweet will be feed again to an agent to generate a thumbnail image using HuggingFace Stable diffusion Xl model.
<br>
Example:

* <img src="assets/example.jpg" style="height: 300px;"/>

4. The tweet and the image will be posted on Twitter.

### **Scraping AI news articles -> Generating tweet content -> Generating a related thumbnail image -> Posting the tweet on Twitter**
   

## Technologies Used

- Python
- Stable Diffusion Xl (using HuggingFace serverless API)
- Selenium
- BeautifulSoup
- Langchain
- Groq Llama-3-70b free tier
- CrewAI

## Installation

### Using Docker

1. Clone the repository:
   ```sh
   git clone https://github.com/wassim249/xgrow
   cd xgrow
   ```
2. Create a `.env` file in the root directory and add the following environment variables:
   ```sh
   X_USERNAME= #Twitter username
   X_PASSWORD= #Twitter password
   GROQ_API_KEY= #Groq API key
   HF_API_KEY= #HuggingFace API key
   ```
3. Build the Docker image:
   ```sh
    docker build -t xgrow .
    ```
4. Run the Docker container:
    ```sh
     docker run -it xgrow --env-file .env -v xgrow:/app/data --name xgrow
     ```
### Without Docker

1. Clone the repository:
   ```sh
   git clone https://github.com/wassim249/xgrow
   cd xgrow
    ```
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the root directory and add the environment variables (see step 2 in the Docker installation).
4. Run the bot:
    ```sh
    python main.py
    ```
   
## Usage
*  Ensure your '.env' file is correctly set up with the required environment variables.
* The bot is using selenium to access to your X account, please take responsibility for its usage.
* You don't need to pay for anything,it's totally free.

## Contact
- [wassim.elbakkouri@ahoo.com](wassim.elbakkouri@ahoo.com)
   