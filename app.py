import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Scrape latest disaster news from a news website
def scrape_disaster_news():
    url = "https://www.bbc.com/news/topics/c50znx8v132t/natural-disasters" 
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_data = []
    articles = soup.find_all("a", class_="gs-c-promo-heading")[:5]  
    for article in articles:
        title = article.get_text()
        link = "https://www.bbc.com" + article["href"]
        news_data.append({"Title": title, "URL": link})

    return pd.DataFrame(news_data)

# Scrape Twitter-like updates from a forum (alternative to Twitter API)
def scrape_forum_updates():
    url = "https://www.reddit.com/r/disasters/"  
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    updates = []
    posts = soup.find_all("h3")[:5]  
    for post in posts:
        updates.append({"Update": post.get_text()})

    return pd.DataFrame(updates)

# Streamlit UI Dashboard
st.title("Real-Time Disaster Information")
st.subheader("Latest Disaster News")
st.dataframe(scrape_disaster_news())

st.subheader("Community Updates")
st.dataframe(scrape_forum_updates())
