Twitter Sentiment Analysis
==========================

An example use of sentiment analysis applied to the latest Tweets for given query.

## How to run the UI?

**UNDER CONSTRUCTION**

## How to run the API?

```bash
$ cd ./api
$ virtualenv -p python3.6 venv
$ . venv/bin/activate
(venv) $ pip install tweepy flask-restplus
(venv) $ export CONSUMER_KEY={YOUR_CONSUMER_KEY}
(venv) $ export CONSUMER_SECRET={YOUT_CONSUMER_SECRET}
(venv) $ export ACCESS_TOKEN={YOUR_ACCESS_TOKEN}
(venv) $ export ACCESS_TOKEN_SECRET={YOUR_ACCESS_TOKEN_SECRET}
(venv) $ python main.py
```

### Example API calls

Here you can find some example endpoints that we've prepared:

#### Get Trendings for given country

**NOTE:** Only `UK` and `USA` are supported for now!

`GET` -> `http://127.0.0.1:5000/trending/UK`

```json
[
  {
    "name": "Soulja Boy",
    "query": "%22Soulja+Boy%22",
    "volume": 112724
  },
  {
    "name": "Bielsa",
    "query": "Bielsa",
    "volume": 79883
  },
  {
    "name": "Marcelo",
    "query": "Marcelo",
    "volume": 60846
  },
  {
    "name": "#JuveMilan",
    "query": "%23JuveMilan",
    "volume": 34641
  }
]
```

#### Get Tweets with sentiment analysis

`GET` -> `http://127.0.0.1:5000/tweets?query=hate&size=100`

```json
[
  {
    "text": "I HATE bullies.",
    "sentiment": null
  },
  {
    "text": "i hate the pain i feel in my heart..",
    "sentiment": null
  },
  {
    "text": "I reall hate the fact that R Kelly make some amazing ass music 🤦🏾‍♂️🤦🏾‍♂️🤦🏾‍♂️",
    "sentiment": null
  },
  {
    "text": "RT @pinkypromiseme_: I don't understand where all the hate for the #GilletteAd is coming from? It's just saying don't be an asshole and tre…",
    "sentiment": null
  },
  {
    "text": "RT @Y2SHAF: i hate it when i’m walking on the treadmill and the person next to me starts running like calm down madam",
    "sentiment": null
  }
]
```
