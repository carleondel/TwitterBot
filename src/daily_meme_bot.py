# PURPOSE - ORCHESTRATOR

'''Orchestrator Script: Create a script (daily_meme_bot.py) that will call both retrieve_daily_memes.py and post_memes_to_twitter.py sequentially. The order will be:

    First, call retrieve_daily_memes.py to fetch new memes.
    Then, call post_memes_to_twitter.py to post the memes throughout the day. '''

import subprocess
import time

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running {script_name}: {result.stderr}")

if __name__ == "__main__":
    # Fetch daily memes
    run_script('src/retrieve_daily_memes.py')

    # Wait for 5 seconds to ensure memes are downloaded
    time.sleep(5)
    
    # Post memes to Twitter
    run_script('src/post_memes_to_twitter.py')

