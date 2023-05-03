from galaxy.api.types import (
   Cookie
)

ACTION_REVOKE_KEY_URL = "https://steamcommunity.com/dev/revokekey"
ACTION_REGISTER_KEY_URL = "https://steamcommunity.com/dev/registerkey"


STEAM_LOGIN_WINDOW_PARAMS = {
    "window_title": "Login to platform",
    "window_width": 800,
    "window_height": 650,
    "start_uri": "https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey",
    "end_uri_regex": r"^https://steamcommunity.com/dev/apikey",
}

STEAM_LOGIN_REJECT_COOKIES_COOKIE = [
    Cookie(
        "cookieSettings",
        "%7B%22version%22%3A1%2C%22preference_state%22%3A2%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D",
        "steamcommunity.com",
    )
]

STORED_CREDENTIAL_WEBPAPIKEY_KEY = "webapikey"
STORED_CREDENTIAL_STEAMID_KEY = "steamid"


STEAM_API_BASE_URL = "http://api.steampowered.com"

STEAM_API_GET_OWNED_GAMES_URL = f"{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
STEAM_API_GET_PAYER_SUMMARIES_URL = f"{STEAM_API_BASE_URL}/ISteamUser/GetPlayerSummaries/v0002/"

STEAM_API_OK_HTTP_CODES = [200]
STEAM_API_NOK_HTTP_CODES = [401, 403]


STEAM_API_BEGINNING_OF_TIME = 86400