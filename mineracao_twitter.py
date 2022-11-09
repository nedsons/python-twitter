import tweepy


def conecta_tweepy():
    print("Conectando no Twitter...")
    API_KEY = ''
    API_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET, ACCESS_TOKEN)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if not api:
        print("Can't Authenticate")
        sys.exit(-1)
    else:
        print("Conexão estabelecida!")
        return api


def coleta_tweets(searchQuery, max_tweets):
	tweepy_api = conecta_tweepy()
    tweetsPerQry = 100  # this is the max the API permits

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    while tweetCount < max_tweets:
        try:
            if max_id <= 0:
                if not sinceId:
                    new_tweets = tweepy_api.search(searchQuery, count=tweetsPerQry,
                                                   lang='pt', tweet_mode="extended")
                else:
                    new_tweets = tweepy_api.search(searchQuery, count=tweetsPerQry,
                                                   since_id=sinceId, lang='pt', tweet_mode="extended")
            else:
                if not sinceId:
                    new_tweets = tweepy_api.search(searchQuery, count=tweetsPerQry,
                                                   max_id=str(max_id - 1), lang='pt', tweet_mode="extended")
                else:
                    new_tweets = tweepy_api.search(searchQuery, count=tweetsPerQry,
                                                   max_id=str(max_id - 1),
                                                   since_id=sinceId, lang='pt', tweet_mode="extended")
            if not new_tweets:
                print("Não foi encontrado mais nenhum tweet")
                break
            for tweet in new_tweets:
                try:
                    f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                            '\n')
                except(RuntimeError, TypeError, NameError, Exception) as e:
                    logging.error(e)
                    pass
            tweetCount += len(new_tweets)
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            logging.error(e)
            # print("some error : " + str(e))
            break
    print("Downloaded {} tweets".format(tweetCount))
