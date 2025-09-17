import os
import praw
import random
import subprocess
import argparse

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    user_agent=os.getenv("USER_AGENT", "ContainerQuestBot v1.0"),
)

SUBREDDIT_NAME = "ContainerQuest"

story_zones = [
    "The Forgotten Dockyards",
    "The Container Wastes",
    "The Rusted Citadel",
    "The Deep Harbor",
    "The Final Kernel"
]

story_events = [
    "A shadowy figure appears from the misty crates.",
    "You pry open a container glowing faintly with blue light.",
    "A rival coder challenges you to a deploy duel!",
    "A swarm of corrupted packets blocks your path.",
    "The ground trembles as the Daemon awakens..."
]

def play_game(command: str, user: str):
    zone = random.choice(story_zones)
    event = random.choice(story_events)
    build_speed = random.randint(1, 20)
    creativity = random.randint(0, 10)
    trap = random.choice([0, 5, 10])
    total = build_speed + creativity - trap
    total = max(0, total)
    health_remaining = 100 - trap
    result = f"""
📜 Zone: {zone}
⚔️ Event: {event}

🎮 Player: {user}
👉 Command: {command}

⚡ Build Speed: {build_speed} pts
🎨 Creativity: {creativity} pts
💀 Trap Damage: -{trap} pts

👉 Final Score: {total} pts
❤️ Health Remaining: {health_remaining}

✅ Progress saved!
"""
    return result.strip()

def dry_run(command: str, user: str):
    print("----- DRY RUN -----")
    print(play_game(command, user))
    print("-------------------")

def post_play(command: str, user: str):
    output = play_game(command, user)
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    title = f"⚔️ {user} ventured into ContainerQuest!"
    body = f"```\n{output}\n```"
    subreddit.submit(title, selftext=body)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=str, required=True)
    parser.add_argument("--user", type=str, default="guest")
    parser.add_argument("--post", action="store_true")
    args = parser.parse_args()
    if args.post:
        post_play(args.command, args.user)
    else:
        dry_run(args.command, args.user)
