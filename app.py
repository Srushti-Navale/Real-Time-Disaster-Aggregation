import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time

# Scrape latest disaster news from a news website
@st.cache_data(ttl=60)
def scrape_disaster_news():
    try:
        url = "https://www.bbc.com/news/topics/c50znx8v132t/natural-disasters" 
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers={"Accept":"application/json"})
        print(response.text[:1000])
        soup = BeautifulSoup(response.text, "html.parser")

        news_data = []
        articles = soup.find_all("a", class_="gs-c-promo-heading")[:5]  
        for article in articles:
          title = article.get_text()
          link = "https://www.bbc.com" + article["href"]
          news_data.append({"Title": title, "URL": link})

        return pd.DataFrame(news_data)if news_data else pd.DataFrame([{'Title':'No news found', 'URL':''}])
    except Exception as e:
        return pd.DataFrame([{"Update":"Error fetching updated: " + str(e)}])
   
#Scrape Twitter-like updates from a forum (alternative to Twitter API)
@st.cache_data(ttl=60)
def scrape_forum_updates():
    try:
        url = "https://www.reddit.com/r/disasters/"  
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:raise Exception(f'failed to fetch data from {url}')


        soup = BeautifulSoup(response.text, "html.parser")

        updates = []
        posts = soup.find_all("h3")[:5]  
        for post in posts:
           
            updates.append({"Update": post.get_text()})

        return pd.DataFrame(updates)if updates else pd.DataFrame([{'update':'No update found'}])
    except Exception as e:
        return pd.DataFrame([{"Update":"Error fetching updates: "+ str(e)}])
    

# Streamlit UI Dashboard
st.title("Real-Time Disaster Information")
st.caption("Live updates every 60 seconds")

st.subheader("Latest Disaster News")
news_df= scrape_disaster_news()
st.dataframe(news_df)

st.subheader("Community Updates")
updates_df = scrape_forum_updates()
st.dataframe(updates_df)

#Manual refresh button
if st.button("Refresh Data "):
    scrape_disaster_news.clear()
    scrape_forum_updates.clear()
    st.rerun()

#refresh every 60 seconds
st_autorefresh(interval=60000, key='dataframe_refresh')