# Reddit-Scraper
A simple reddit comment scraper


To perform sentiment analysis, we'll use the popular `nltk` library along with its `VADER` sentiment analysis module. First, install the `nltk` package:

```
pip install nltk
```

Then, download the VADER sentiment analysis data:

```python
import nltk
nltk.download('vader_lexicon')
```