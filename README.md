Twitter Sentiment Analysis
==========================

An example use of sentiment analysis applied to the latest Tweets. Application uses LSTM with
 Attention layer to draw between positive and negative feeback from a given Tweet. Also, it
 can show which words were most impactful during analysis based on internal attention values.

## How to run web-app?

```bash
$ cd ./web-app
$ npm install
$ npm start
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

**NOTE:** This repository already contains pretrained model weights and tokenizer, so feel free to use it!

To run the API, use below series of commands:

```bash
$ cd ./api
$ virtualenv -p python3.6 venv
$ . venv/bin/activate
(venv) $ pip install tweepy flask-restplus flask-cors keras tensorflow nltk
(venv) $ export CONSUMER_KEY={YOUR_CONSUMER_KEY}
(venv) $ export CONSUMER_SECRET={YOUT_CONSUMER_SECRET}
(venv) $ export ACCESS_TOKEN={YOUR_ACCESS_TOKEN}
(venv) $ export ACCESS_TOKEN_SECRET={YOUR_ACCESS_TOKEN_SECRET}
(venv) $ export NLTK_DATA=./nltk/
(venv) $ python main.py
```

Open your browser and visit Swagger page under [http://127.0.0.1:5000](http://127.0.0.1:5000).

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

`GET` -> `http://127.0.0.1:5000/tweets?query=hate&size=3`

```json
[
  {
    "text": "i hate people",
    "sentiment": "NEGATIVE",
    "attention": [
      0.2035791277885437,
      1,
      1
    ],
    "fullname": "jen",
    "nickname": "iamabandito",
    "created": "2019-01-22T20:32:39",
    "photo_url": "http://pbs.twimg.com/profile_images/1086319779382743040/MhRt4ims_normal.jpg"
  },
  {
    "text": "I hate that being a “morning person” is seen as being the most productive. I work better at night, I work better when I’ve slept in, I enjoy leisure mornings. I am not a morning person period.",
    "sentiment": "NEUTRAL",
    "attention": [
      0.018304800614714622,
      0.1260768324136734,
      0.08547406643629074,
      0.018965071067214012,
      0.019448567181825638,
      0.11604408919811249,
      0.07898149639368057,
      0.025163527578115463,
      0.1264631301164627,
      0.04651867225766182,
      0.03077707439661026,
      0.01897846907377243,
      0.025690194219350815,
      0.11794410645961761,
      0.031303856521844864,
      0.12673059105873108,
      0.12484921514987946,
      0.056624606251716614,
      0.07170872390270233,
      0.058482199907302856,
      0.12674853205680847,
      0.1258183866739273,
      0.1265796571969986,
      0.041735485196113586,
      0.05405481904745102,
      0.02129172533750534,
      0.03456570953130722,
      0.1267087459564209,
      0.12296092510223389,
      0.0811547040939331,
      0.07187405973672867,
      0.11625345051288605,
      0.12675505876541138,
      0.12675221264362335,
      0.12490260601043701,
      0.12324085831642151,
      0.12407350540161133
    ],
    "fullname": "c",
    "nickname": "cxxlvndivvxx",
    "created": "2019-01-22T20:36:31",
    "photo_url": "http://pbs.twimg.com/profile_images/1074561986774544384/o3qw24Ve_normal.jpg"
  },
  {
    "text": "I love your voice but I hate when you speak",
    "sentiment": "NEGATIVE",
    "attention": [
      0.04843185096979141,
      0.33358097076416016,
      0.3353733420372009,
      0.3245925009250641,
      0.3353455066680908,
      0.33492520451545715,
      0.33537527918815613,
      0.33537524938583374,
      0.3348485231399536,
      0.2821515202522278
    ],
    "fullname": "𝐤𝐠 ¡𝐭𝐨𝐦𝐨𝐫𝐫𝐨𝐰!",
    "nickname": "theblcony",
    "created": "2019-01-22T20:36:30",
    "photo_url": "http://pbs.twimg.com/profile_images/1086472744513011712/u44lGkLA_normal.jpg"
  }
]
```
