Twitter Sentiment Analysis
==========================

An example use of sentiment analysis applied to the latest Tweets. Application uses LSTM with
 Attention layer to draw between positive and negative feeback from a given Tweet. Also, it
 can show which words were most impactful during analysis based on internal attention values.

## How to run web-app?

```bash
$ cd ./web-app
$ npm install
$ npm run dev
```

Need more info about web-app project? Check out [general project info](/web-app/README.md).

## How to train the model?

To train your model, please follow below commands:

```bash
$ cd ./training
$ virtualenv -p python3.6 venv
$ . venv/bin/activate
(venv) $ pip install pandas keras tensorflow sklearn nltk swifter
(venv) $ cd ./dataset && wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip
(venv) $ unzip trainingandtestdata.zip
(venv) $ cd ..
(venv) $ export NLTK_DATA=./nltk/
(venv) $ python prepare_dataset.py
(venv) $ python train.py
```

## How to run the API?

At first copy your model from above training together with `tokenizer.pickle` to the `./api/model_data` directory.
 Remember to change the name of you model to `weights.h5`! Folder should look like this:

```
$ ls ./api/model_data/
-rw-r--r--  1 owner  owner   5.9K Jan 18 00:09 tokenizer.pickle
-rw-r--r--  1 owner  owner    13M Jan 18 00:10 weights.h5
```

To run the API, use below series of commands:

```bash
$ cd ./api
$ virtualenv -p python3.6 venv
$ . venv/bin/activate
(venv) $ pip install tweepy flask-restplus keras tensorflow nltk
(venv) $ export CONSUMER_KEY={YOUR_CONSUMER_KEY}
(venv) $ export CONSUMER_SECRET={YOUT_CONSUMER_SECRET}
(venv) $ export ACCESS_TOKEN={YOUR_ACCESS_TOKEN}
(venv) $ export ACCESS_TOKEN_SECRET={YOUR_ACCESS_TOKEN_SECRET}
(venv) $ export NLTK_DATA=./nltk/
(venv) $ python main.py
```

## Example API calls

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

`GET` -> `http://127.0.0.1:5000/tweets?query=uber&size=3`

```json
[
  {
    "text": "Uber/Lyft drivers be rappin like shit",
    "sentiment": "NEGATIVE",
    "attention": [
      -0.009645622223615646,
      0.00724678672850132,
      0,
      0.07018525898456573,
      0.017534570768475533,
      0.008581627160310745
    ]
  },
  {
    "text": "Scariest story in 1 sentence:\n\"Why don't you come sit up front?\" smiled the Uber driver.",
    "sentiment": "POSITIVE",
    "attention": [
      -0.08198671787977219,
      0.03467215970158577,
      0,
      0.07736007124185562,
      -0.07715171575546265,
      -0.048132121562957764,
      0,
      0.0553499199450016,
      0.02649160847067833,
      0,
      -0.0034008703660219908,
      0.0691278949379921,
      0,
      -0.02065562643110752,
      0.03373348340392113
    ]
  },
  {
    "text": "I fell asleep while this Uber driver was talking to me for what I thought was the rest of the fucking trip but when I woke up he was still talking , I’m tight.",
    "sentiment": "NEGATIVE",
    "attention": [
      0,
      -0.04436713457107544,
      -0.009265453554689884,
      0,
      0,
      -0.1607808917760849,
      0.07840242981910706,
      0,
      0.1551399677991867,
      0,
      0,
      0,
      0,
      0,
      0.019089631736278534,
      0,
      0,
      0.04676656424999237,
      0,
      0,
      -0.19999167323112488,
      0.009048397652804852,
      0,
      0,
      0,
      -0.0031136013567447662,
      0,
      0,
      0,
      0.015796182677149773,
      0.11989317834377289,
      0.06898099929094315,
      -0.13893665373325348
    ]
  }
]
```
