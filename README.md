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

1. **`trials.py`**: Tweets a random number.
2. **`images.py`**: Tweets a specific image from a local folder.
3. **`scheduled_img.py`**: Automatically tweets an image from the folder at regular intervals.
4. **`rmathmemes.py`**: Fetches the top Reddit meme posts and tweets them with their captions.

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
