import requests
import json

# query = input("What type of news are you interested in?")
query = "cricket"
query2= "9b998beccf4345609b55031820961f69"
# url =f"https://newsapi.org/v2/everything?q={query}&from=2024-10-09&sortBy=publishedAt&apiKey={query2}"
url =f"https://newsapi.org/v2/everything?q={query}&from=2024-10-10&sortBy=publishedAt&apiKey=9b998beccf4345609b55031820961f69"

r = requests.get(url)
news = json.loads(r.text)
# print(news, type(news))
for article in news["articles"]:
    print(article["title"])
    print(article["description"])
    print("-----------------------------------")