# Author:  Ali Kolenovic

#  youtube_data.py searches YouTube for a number of videos that match a keyterms, both number and keyterm is provided by the user.

# To run from terminal window:   python3 youtube_data.py 

from googleapiclient.discovery import build      # use build function to create a service object
import csv
import pandas as pd
import unidecode

# put your API key into the API_KEY field below, in quotes
API_KEY = ""

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

#  function youtube_search retrieves the YouTube records

def youtube_search(s_term, s_max):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

    search_data = youtube.search().list(q=s_term, part="id,snippet", maxResults=s_max).execute()
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Published_At', 'Title', 'Duration', 'View_Count', 'Like_Count'])
    # search for videos matching search term;
    for search_instance in search_data.get("items", []):
        if search_instance["id"]["kind"] == "youtube#video":
        
            videoId = search_instance["id"]["videoId"]  
            title = unidecode.unidecode(search_instance["snippet"]["title"])
            publishAt = search_instance["snippet"]["publishedAt"]
            
                      
                  
            video_data = youtube.videos().list(id=videoId,part="contentDetails,statistics").execute()
            for video_instance in video_data.get("items",[]):
                viewCount = video_instance["statistics"]["viewCount"]
                duration = video_instance["contentDetails"]["duration"]

                if 'likeCount' not in video_instance["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_instance["statistics"]["likeCount"]
            # Write the data to a csv file in  the respective order
            with open('output.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([videoId, publishAt, title, duration, viewCount, likeCount])    
# main routine
search_term = input("Enter in a search. ")
search_max = input("Enter in max search results. ")
print("\nSearching YouTube with keyword " + search_term + "...")
print("Done! Displaying " + search_max + " results.")

youtube_search('fornite', int(search_max))
pd.set_option('display.max_rows', None)
df = pd.read_csv('output.csv')
# Convert time to pandas time in order to sort.
df['Published_At'] = pd.to_datetime(df.Published_At)

# Print analysis 1 by sorting by newest videos first.
analysis1 = (df[['Title', 'ID', 'Published_At', 'Duration']]).sort_values(by='Published_At', ascending=False)
print("\nYouTube searches sorted by newest first")
print(analysis1)
# Print analysis 2 by sorting by view count.
analysis2 = (df[['Title', 'ID', 'Published_At', 'Duration', 'View_Count']]).sort_values(by='View_Count', ascending=False)
print("\nYouTube searches sorted by view count. (Top 5)")
print(analysis2.head())
# Create a new column to calculate the percentage of likes.
df['Percentage_of_Likes'] = df['Like_Count'] / df['View_Count']
#Print analysis 3 by sorting by percentage of likes.
analysis3 = (df[['Title', 'ID', 'Percentage_of_Likes', 'View_Count', 'Like_Count', 'Published_At', 'Duration']]).sort_values(by='Percentage_of_Likes', ascending=False)
print("\nYouTube searches sorted by percentage of likes. (Top 5)")
print(analysis3.head())

