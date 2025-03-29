import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Scrape latest disaster news from a news website
@st.cache_data(ttl=60)
def get_disaster_news():
        url =   "https://feeds.bbci.co.uk/news/world/rss.xml"
        response = requests.get(url)
        if response.status_code !=200:
            return pd.DataFrame([])
        
        soup = BeautifulSoup(response.content, "lxml-xml")
        items = soup.find_all("item")[:5]

        news_data = [{"Title": item.title.text, "URL": item.link.text}for item in items]
        return pd.DataFrame(news_data)
       
   
#Scrape Twitter-like updates from a forum (alternative to Twitter API)
@st.cache_data(ttl=60)
def scrape_forum_updates():
    try:
        url = "https://www.reddit.com/r/disasters/"  
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
             raise Exception(f'failed to fetch data from {url}')


        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("h3")[:5]   
        updates= [{"Update": post.get_text()}for post in posts]

        return pd.DataFrame(updates)if updates else pd.DataFrame([{'update':'No update found'}])
    except Exception as e:
       return pd.DataFrame([{"Update":f"Error fetching updates: {str(e)}"}])
    

# Streamlit UI Dashboard
st.title("Real-Time Disaster Information")
st.caption("Live updates every 60 seconds")

st.subheader("Latest Disaster News")
news_df= get_disaster_news()
if news_df.empty:
     st.write("No Data available at the moment")
else:
     for _, row in news_df.iterrows():
          st.markdown(f"[🔗 {row['Title']}]({row['URL']})")     

st.subheader("Community Updates")
updates_df = scrape_forum_updates()
st.dataframe(updates_df)

#Manual refresh button
if st.button("Refresh Data "):
    get_disaster_news.clear()
    scrape_forum_updates.clear()
    st.rerun()

#refresh every 60 seconds
st_autorefresh(interval=60000, key='data_refresh')