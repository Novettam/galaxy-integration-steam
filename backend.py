import constants
import requests
import json
import logging
from typing import Dict

from galaxy.api.errors import (
    InvalidCredentials
)
from galaxy.api.types import (
    GameTime
)

def get_method_params(method_name, stored_credentials):
    params = {
        "format": "json",
        "key": stored_credentials.get(constants.STORED_CREDENTIAL_WEBPAPIKEY_KEY)
        }

    if method_name == "GetPlayerSummaries":
        params["steamids"] = stored_credentials.get(constants.STORED_CREDENTIAL_STEAMID_KEY)
    elif method_name == "GetOwnedGames":
        params["steamid"] = stored_credentials.get(constants.STORED_CREDENTIAL_STEAMID_KEY)
    return params


def get_player_summaries(stored_credentials):
    # get params
    payload = get_method_params("GetPlayerSummaries", stored_credentials)

    # call method
    get_players_summaries_response = requests.get(constants.STEAM_API_GET_PAYER_SUMMARIES_URL, params=payload)

    if get_players_summaries_response.status_code in constants.STEAM_API_OK_HTTP_CODES:
        return get_players_summaries_response.json()
    elif get_players_summaries_response.status_code in constants.STEAM_API_NOK_HTTP_CODES:
        raise InvalidCredentials()

def get_steam_owned_games(stored_credentials, appinfo=False, appids_filter=[]):
    logging.debug("get_steam_owned_games")
    # get params
    payload = get_method_params("GetOwnedGames", stored_credentials)

    if appinfo:
        payload["include_appinfo"] = "true" 

    # TODO: filter by ids appids_filter, https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_.28v0001.29
    # JSON: "appids_filter: [ 440, 500, 550 ]" )
    if appids_filter:
        integer_appids_filter = list(map(int, appids_filter))
        payload["input_json"] = "{ \"steamid\": "+ stored_credentials.get("steamid") + ", \"appids_filter\": "+json.dumps(integer_appids_filter)+"}"
        logging.debug("appids_filter")
        


    owned_games_response = requests.get(constants.STEAM_API_GET_OWNED_GAMES_URL, params=payload)

    if owned_games_response.status_code in constants.STEAM_API_OK_HTTP_CODES:
        return owned_games_response.json()
    elif owned_games_response.status_code in constants.STEAM_API_NOK_HTTP_CODES:
        raise InvalidCredentials()
    
async def get_steam_game_times(stored_credentials, game_ids) -> Dict[str, GameTime]:
    steam_owned_game_list = get_steam_owned_games(stored_credentials, appids_filter=game_ids).get("response").get("games")

    context = {}

    for game in steam_owned_game_list:
        game_id = str(game.get("appid"))
        context[game_id] = GameTime(
            game_id,
            game.get("playtime_forever") if game.get("playtime_forever") > 0 else None,
            game.get("rtime_last_played") if game.get("rtime_last_played") > constants.STEAM_API_BEGINNING_OF_TIME else None
            )
        
        logging.debug(f"Caching time for game_id: {game_id}")
        logging.debug("game_id: "+str(context[game_id].game_id))
        logging.debug("time_played: "+str(context[game_id].time_played))
        logging.debug("last_played_time: "+str(context[game_id].last_played_time))


    return context
