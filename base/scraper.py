import requests
from bs4 import BeautifulSoup

url = "https://ekantipur.com/news"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("a")

for title in titles:
    
    print(title.text)
    print(title["href"])
    print("------------------")