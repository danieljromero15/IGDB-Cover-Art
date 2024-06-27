import os
import webbrowser

import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

global access_token

protocol = "https"
base_url = "api.igdb.com/v4"

headers = {
    "Client-ID": os.getenv('CLIENT_ID')
}


def login():
    global access_token
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    response = requests.post(
        f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type"
        f"=client_credentials"
    )
    headers['Authorization'] = "Bearer " + response.json()['access_token']


def search_games(name):
    response = requests.post(
        f"{protocol}://{base_url}/games",
        headers=headers,
        data=f"search \"{name}\"; fields name, cover, first_release_date;"
    )
    return response.json()


def get_cover_url(selected_game):
    cover_id = selected_game['cover']
    # print(cover_id)
    response = requests.post(
        f"{protocol}://{base_url}/covers",
        headers=headers,
        data=f"fields game,url; where id={cover_id};"
    )
    thumb_url = "https:" + response.json()[0]["url"]
    url = thumb_url.replace("t_thumb", "t_1080p")
    return url


def open_url(url):
    webbrowser.open(url, new=0, autoraise=True)


if __name__ == '__main__':
    while True:
        login()

        game_name = input('Enter game name: ')

        # games = search_games("BitBurner")
        games = search_games(game_name)
        # print(json.dumps(games, indent=4))
        if len(games) == 0:
            print("No games found.")
            exit(0)
        elif len(games) == 1:
            game = games[0]
        else:
            print("Multiple games found.")
            for i, game in enumerate(games):
                try:
                    print(f"{i + 1}. {game['name']} ({str(datetime.fromtimestamp(int(game['first_release_date'])))[:4]})")
                except KeyError:
                    print(f"{i + 1}. {game['name']}")
            choose_game = int(input("Which game would you like to choose? ")) - 1
            game = games[choose_game]

        cover_url = get_cover_url(game)

        open_url(cover_url)
