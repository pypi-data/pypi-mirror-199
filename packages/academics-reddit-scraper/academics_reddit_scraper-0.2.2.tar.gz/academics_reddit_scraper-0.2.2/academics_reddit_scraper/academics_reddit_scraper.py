import os
import praw
import csv
from typing import List, Dict, Tuple
import argparse
from .sentiment_analysis import analyze_sentiment
from tqdm import tqdm

def create_reddit_instance():
    """
    Create a Reddit API instance using environment variables for authentication.

    :return: A Reddit API instance.
    """
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent="reddit-scraper",
        # username=os.environ["REDDIT_USERNAME"],
        # password=os.environ["REDDIT_PASSWORD"],
    )

def scrape_posts(reddit, subreddit_name: str, num_posts: int) -> List[Dict]:
    """
    Scrape posts from a subreddit using the Reddit API.

    :param reddit: A Reddit API instance.
    :param subreddit_name: The name of the subreddit to scrape.
    :param num_posts: The number of posts to scrape.
    :return: A list of dictionaries containing post data.
    """
    print("Scraping posts...")
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    for post in tqdm(subreddit.hot(limit=num_posts), total=num_posts):
        post_data = {
            "post_title": post.title,
            "post_id": post.id,
            "num_upvotes": post.score,
            "tags": post.link_flair_text,
            "post_content": post.selftext,
            "post_sentiment": analyze_sentiment(post.selftext),
        }
        posts_data.append(post_data)

    return posts_data

def scrape_comments(reddit, post_ids: List[str], num_comments: int) -> List[Dict]:
    """
    Scrape comments from a list of Reddit posts.

    :param reddit: A Reddit API instance.
    :param post_ids: A list of post IDs to scrape comments from.
    :param num_comments: The number of comments to scrape per post.
    :return: A list of dictionaries containing comment data.
    """
    print("Scraping comments...")
    comments_data = []

    for post_id in tqdm(post_ids, desc="Posts"):
        post = reddit.submission(id=post_id)

        post.comments.replace_more(limit=None)
        for comment in tqdm(post.comments.list()[:num_comments], total=num_comments, desc="Comments"):
            comment_data = {
                "post_title": post.title,
                "post_id": post_id,
                "commenter_name": comment.author.name,
                "comment_body": comment.body,
                "num_upvotes": comment.score,
                "comment_sentiment": analyze_sentiment(comment.body),
            }
            comments_data.append(comment_data)

    return comments_data

def export_to_csv(data: List[Dict], filename: str):
    """
    Export a list of dictionaries to a CSV file.

    :param data: A list of dictionaries containing data to export.
    :param filename: The name of the CSV file to create.
    """
    print(f"Exporting data to {filename}...")
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def parse_args() -> Tuple[str, int, int]:
    """
    Parse command-line arguments.

    :return: A tuple containing the subreddit name, number of posts, and number of comments.
    """
    parser = argparse.ArgumentParser(description="Reddit post and comment scraper.")
    parser.add_argument("subreddit", type=str, help="Subreddit name")
    parser.add_argument("num_posts", type=int, help="Number of posts to scrape")
    parser.add_argument("num_comments", type=int, help="Number of comments to scrape")
    args = parser.parse_args()
    
    return args.subreddit, args.num_posts, args.num_comments

def gather_data(reddit, subreddit: str, num_posts: int, num_comments: int) -> Tuple[List[Dict], List[Dict]]:
    """
    Gather post and comment data from a subreddit.

    :param reddit: A Reddit API instance.
    :param subreddit: The subreddit name to scrape.
    :param num_posts: The number of posts to scrape.
    :param num_comments: The number of comments to scrape per post.
    :return: A tuple containing lists of post and comment data dictionaries.
    """
    posts = scrape_posts(reddit, subreddit, num_posts)
    comments = scrape_comments(reddit, [post["post_id"] for post in posts], num_comments)
    return posts, comments

def export_data(posts: List[Dict], comments: List[Dict]):
    """
    Export post and comment data to separate CSV files.

    :param posts: A list of dictionaries containing post data.
    :param comments: A list of dictionaries containing comment data.
    """
    export_to_csv(posts, "posts.csv")
    export_to_csv(comments, "comments.csv")

def main():
    """
    Main function for the Reddit post and comment scraper script.
    """
    subreddit, num_posts, num_comments = parse_args()
    reddit = create_reddit_instance()
    posts, comments = gather_data(reddit, subreddit, num_posts, num_comments)
    export_data(posts, comments)
    print("Done.")

def scrape_reddit(subreddit, num_posts, num_comments):
    reddit = create_reddit_instance()
    posts, comments = gather_data(reddit, subreddit, num_posts, num_comments)
    export_data(posts, comments)
    print("Done.")


if __name__ == "__main__":
    main()