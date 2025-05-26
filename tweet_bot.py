import os, random, openai, tweepy

# Load credentials
openai.api_key    = os.getenv("OPENAI_API_KEY")
auth = tweepy.OAuth1UserHandler(
    os.getenv("TW_CONSUMER_KEY"),
    os.getenv("TW_CONSUMER_SECRET"),
    os.getenv("TW_ACCESS_TOKEN"),
    os.getenv("TW_ACCESS_SECRET"),
)
api = tweepy.API(auth)

# Fetch top 3 hashtags for a random region
def get_hashtags():
    woeids = [23424977, 23424975, 23424775]  # US, UK, CA
    trends = api.get_place_trends(id=random.choice(woeids))[0]["trends"]
    tags = [t["name"] for t in trends if t["name"].startswith("#")]
    return " ".join(tags[:3])

# Generate tweet and post
def main():
    resp = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role":"user",
                 "content":"Write a concise money-making tip under 280 characters."}]
    )
    text = resp.choices[0].message.content.strip()
    tweet = f"{text}\n\n{get_hashtags()}"
    api.update_status(tweet)
    print("Tweeted:", tweet)

if __name__=="__main__":
    main()
