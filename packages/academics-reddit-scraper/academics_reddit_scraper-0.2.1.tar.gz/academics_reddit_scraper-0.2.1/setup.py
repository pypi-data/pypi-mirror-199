from setuptools import setup, find_packages

setup(
    name="academics_reddit_scraper",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "praw",
        "tqdm",
        "sentiment_analysis",  # Add any other required packages here
    ],
    entry_points={
        "console_scripts": [
            "academics_reddit_scraper = academics_reddit_scraper.reddit_scraper:main",
        ],
    },
    author="Nathan Laundry",
    author_email="nathan@fieldguidetocoding.com",
    description="A Reddit post and comment scraper",
    license="MIT",
    keywords="reddit scraper praw",
    url="https://github.com/yourusername/reddit_scraper",
)