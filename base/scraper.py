import requests
from bs4 import BeautifulSoup

url = "https://ekantipur.com/news"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("h2")

for title in titles:
    
    # print(title.text)
    # print(title["href"])
    # print("------------------")
    print(f"Heading: {title.get_text(strip=True)}")
    
    # 2. Look for a link INSIDE the h2
    link_tag = title.find("a")
    if link_tag and link_tag.has_attr('href'):
        print(f"Link: {link_tag["href"]}")
    else:
        print("No link found in this heading.")
        
    print("------------------")