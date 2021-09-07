"""
Usage:
  newsbot.py fetch [options]

Options:
  -h --help          Show this screen.
  --version          Show version.
  --news-query=<query>    News Query for the news API [default: happy]
  --type=<type>          Type of speech recognition [default: sr_google]
  --news-apikey=<news_api_key>   News API Key
  --ibm-username=<ibm_username> IBM Username for Watson Speech Recognition
  --ibm-password=<ibm_password> IBM Password for Watson Speech Recognition
  --ibm-apikey=<ibm_api_key>   IBM API Key for Watson IAM Authentication
  --ibm-apiurl=<ibm_api_url>   IBM API URL for Watson Speech Recognition [default: https://api.us-east.speech-to-text.watson.cloud.ibm.com]
"""

import sys
from docopt import docopt
from model.jarvis import Jarvis

def handle_fetch(arguments):
  news_query   = arguments['--news-query']
  sr_type      = arguments['--type']
  news_api_key = arguments['--news-apikey']
  ibm_password = arguments['--ibm-username']
  ibm_username = arguments['--ibm-password']
  ibm_api_key  = arguments['--ibm-apikey']
  ibm_api_url  = arguments['--ibm-apiurl']
  jarvis = Jarvis(
    news_api_key,
    ibm_username = ibm_username,
    ibm_password = ibm_password,
    ibm_api_key  = ibm_api_key,
    ibm_api_url  = ibm_api_url,
    recognizer_type = sr_type
  )

  jarvis.act()
  # if (sr_type == 'sr_google') or (sr_type == 'sr_watson'):
  #   jarvis.act()
  # elif (sr_type == 'ws_watson'):
  #   jarvis.act_ibm_websockets()
  # else:
  #   print("UNRECOGNIZED")
  
def main():
    arguments = docopt(__doc__, version='NewsBot 0.1.0')
    if (arguments['fetch']):
      handle_fetch(arguments)

if __name__ == "__main__":
    main()