import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from base.models import Scrapnews


class Command(BaseCommand):
    help = "Scrape news"

    def handle(self, *args, **kwargs):

        url = "https://ekantipur.com/news"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        titles = soup.find_all("h2")

        for title in titles:
            link_tag = title.find("a")

            Scrapnews.objects.get_or_create(
                title=title.get_text(strip=True),
                link=link_tag["href"]
            )

        print("News scraped successfully")