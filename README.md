# <img src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" alt="X Icon" width="30"/> Twitter Bot for Memes 

This project aims to develop a Twitter bot that automatically posts memes using images from a local folder and Reddit posts. Long-term goals include automation in meme generation and deployment on cloud services.

## Project Goals

1. **Twitter Meme Posting**:
   - Tweet random images from a local folder.
   - Tweet a specific image at scheduled intervals.
   - Daily fetch and tweet the top Reddit meme posts.

2. **Automation and Deployment**:
   - Create Docker images for the bot.
   - Deploy and run Docker images on AWS for automation.

3. **Long-term Goals**:
   - Daily posting of Reddit images on Twitter.
   - Generate and post AI images with specific themes.
   - Build a large database of memes and rotate them regularly, similar to what [@esnupicore](https://twitter.com/esnupicore) does on Twitter.

4. **Personal Objectives**:
   - Work with APIs.
   - Improve Python skills.
   - Create effective automations.
   - Enhance knowledge in Docker and cloud services like AWS.

## Project Structure

The project consists of several scripts:

1. **`random_number_tweet.py`**: Tweets a random number.
2. **`scheduled_random_meme_tweet.py`**: Posts the memes randomly from the `memes` folder without tweeting the same meme consecutively.
3. **`retrieve_daily_mathmemes.py`**: Retrieves the top daily memes from Reddit’s `surrealmemes` subreddit, filtering for those with a score of at least 150, and saves them to the `surrealmemes` folder.
4. **`post_mathmemes_to_twitter.py`**: Posts the saved memes from the previous day sequentially on Twitter, one per hour, using captions from `captions.txt`. During trials, it posts the memes instantly, followed by each subsequent meme every minute.

5. **`daily_meme_bot.py`**: **Orchestrator Script** that calls both `retrieve_daily_memes.py` and `post_memes_to_twitter.py` sequentially. The flow is as follows:
   - First, it calls `retrieve_daily_memes.py` to fetch new memes from Reddit.
   - Then, after a short delay, it calls `post_memes_to_twitter.py` to post the memes throughout the day on Twitter.

## Requirements

- Python 3.x
- Python Libraries:
  - `praw` for interacting with the Reddit API.
  - `tweepy` for interacting with the Twitter API.
  - `schedule` for scheduling tasks.
  - `python-dotenv` for managing environment variables.

Install the dependencies with:

```bash
pip install praw tweepy schedule python-dotenv
