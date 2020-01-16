# candidate-twitter-account

# Why
I want to automatically collect candidates for hiring.  

# What
This program will collect Twitter user accounts that are likely to be hiring candidates with the Twitter API
and output them to Google Spread Sheet.

# Environments
Python 3.7

Check file requirements.txt if you want to know other libraries and versions of them.

# How to use
- Make the necessary settings to use the Sheet API and Twitter API.
  - cf. https://developers.google.com/sheets/api
  - cf. https://developer.twitter.com/en/docs/ads/general/guides/getting-started
- Create a Spread Sheet and tailor it in a specific format.
  - TODO
- Create file 「.env」
  - Write following values ​​as credentials in the file.（Sheet API and Twitter API）
    - SHEET_PROJECT_ID=xxx
    - SHEET_PRIVATE_KEY_ID=xxx
    - SHEET_PRIVATE_KEY=xxx
    - SHEET_CLIENT_EMAIL=xxx
    - SHEET_CLIENT_ID=xxx
    - SHEET_CLIENT_X509_CERT_URL=xxx
    - ACCESS_TOKEN=xxx
    - ACCESS_TOKEN_SECRET=xxx
    - CONSUMER_KEY=xxx
    - CONSUMER_SECRET=xxx 
    - ANTISOCIAL_WORDS=xxx
      - Write the words you do not want to collect without space. （ex. f◯ck,kill you,xxx）
- Type `$ pip install -r requirements.txt` command to load the required library.
- Type `$ brew install forego` command to load the library that can read authentication information from .env file.
- Type `$ forego run python batch.py` command to run the program.
  - Replace `GID` written in the file 「collect_new_graduate_designers.py」and「collect_new_graduate_engineers.py」 with the ID of the Spread Sheet prepared by you. 
