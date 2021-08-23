from newsapi import NewsApiClient
import random
import requests

class NewsApiImpl(NewsApiClient):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.random_words = self.init_random_words()
        self.happy_words = ["happy", "joy", "good", "fun", "laugh"]

    def init_random_words(self):
        word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_url)
        words = [word.decode('utf-8') for word in response.content.splitlines()]
        return words
    
    def get_happy_news(self):
        query_param = self.get_random_word(self.happy_words)
        print(f"My random word is... {query_param}")
        return self.get_news(query_param)

    def get_random_article(self):
        query_param = self.get_random_word(self.random_words)
        print(f"My random word is... {query_param}")
        return self.get_news(query_param)

    def get_news(self, query_param):
        print(query_param)
        top_headlines = self.get_everything(
            q=query_param,
            language='en',
            sort_by='relevancy'
        )
        if (top_headlines['totalResults'] > 0):
            print(top_headlines)
            print(top_headlines['articles'][0]['description'])
            return top_headlines['articles'][0]['description']
        else:
            return(f"No Headlines found for {query_param}")

    def get_random_word(self, word_list):
        
        random_index = random.randint(
            0, 
            len(word_list) - 1
        )

        return word_list[random_index]