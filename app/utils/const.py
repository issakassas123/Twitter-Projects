from .colors import GREEN, YELLOW, RESET
from .user import check_version

PATH = r"chrome\chromedriver.exe"

URL = "https://twitter.com/i/flow/login"

VERSION = '1.13.0'

FIRST_PAGE = (
    f'{GREEN}Created by Maxime Dréan.'
    f'\n\nVersion {VERSION} - 2024, 06 February.{RESET}'
    f'{check_version(VERSION)}'  # Check for a new update of the bot.
    '\n\nIf you face any problem, please open an issue.')

ENTER = '\nPRESS [ENTER] TO CONTINUE. '

SECOND_PAGE = f'{GREEN}Created by Maxime Dréan.'

USERNAME = "@gmail.com"

PASSWORD = ""

ALL_DONE = f'\n{GREEN}All done!{RESET}'

# create a list of the values we want to assign for each condition
VALUES = ['Negative', 'Neutral', 'Positive']

API_KEY = "kCkIHQLtALj9FSoJpjOcBsy5S"

API_KEY_SECRET = "ys4iEfCO236Iq87NSbLTc2XyqU60Q0OUATibkMFMcByhb1CO2o"

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEyhsQEAAAAArdkDIjGz9TGDujc%2BD9IyksZNN%2BM%3DrA6hmv1RsT6hp7ys9FGJO1iqQlJIk242n7HBqCGC0PaPZ3No98"

ACCESS_TOKEN = "1590665202881683456-I5zJ3Zq4lOCer2OJHNhVRrBs6OSJgw"

ACCESS_TOKEN_SECRET = "AFpffBbmTQWuhgmYpa1rCkpfb7sbU8isb4qxxGqOYy6lP"

CLIENT_ID = "NXR6ME1WczY5NHNfOGp1dWdDcGs6MTpjaQ"

CLIENT_SECRET = "c1rmCh5xKmQT5UN-RjvrXDquBWfi1s90e7dJzJJ0L1PnSCPSo3"
