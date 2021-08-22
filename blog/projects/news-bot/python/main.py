"""
Usage:
  newsbot.py (stop|start|cycle) <host> <user> [options]

Options:
  -h --help               Show this screen.
  --version               Show version.
"""
import sys
import docopt
from model.jarvis import Jarvis

def main():
    try:
        news_api_key = os.environ["NEWS_API_KEY"] 
    except KeyError:
        print("Please export the NEWS_API_KEY evironment variable before running!")
        sys.exit(1)
    jarvis = Jarvis(news_api_key)
    jarvis.act()

if __name__ == "__main__":
    main()