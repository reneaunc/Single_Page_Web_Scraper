import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#Bring in English
headers = {"Accept-languag": "en-US, en;q=0.5"}

#Specify url to grab data from and store in variable
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"

#store get request to url in variable
results = requests.get(url, headers=headers)

#Store BeautifulSoup method return in variable
soup = BeautifulSoup(results.text, "html.parser")

#print structured tree of soup using prettify method
#print(soup.prettify())

#Initialize storage of data from webpage in list
titles = []
years = [] 
time = [] 
imdb_ratings = []
metascores = []
votes = []
us_gross = []

#Tell scraper where to find each listing
movie_div = soup.find_all('div', class_='lister-item mode-advanced')

#Initiate for loop to iterate through every div container in movie_div
for container in movie_div:
    #Name
    name = container.h3.a.text
    titles.append(name)
    #year
    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)
    #time
    runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
    time.append(runtime)
    #IMDB rating
    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)
    #metascore
    m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
    metascores.append(m_score)
    #skip first movie and resume on second
    nv = container.find_all('span', attrs={'name': 'nv'})

    #Filter nv for votes
    vote = nv[0].text
    votes.append(vote)

    #Filter nv for gross
    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

# print(titles)
# print(years)
# print(time)
# print(imdb_ratings)
# print(metascores)
# print(votes)
# print(us_gross)

#Build DataFrame with Pandas
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
})

#Clean dataframe data
#Clean years
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
#Clean time
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
#Clean metascore
movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')
#Cleaning gross data
#Get rid of dollar sign
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
#Convert to floating point
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')

#Save to a CSV 
movies.to_csv('movies.csv')