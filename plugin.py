import sys
import logging
from typing import Any

from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import Platform
from galaxy.api.types import (
    NextStep,
    Game,
    LicenseInfo,
    LicenseType,
    GameTime,
)
import constants
import authentication
import backend

class SteamIntegrationPlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(
            Platform.Steam,  # choose platform from available list
            "1.0.2",  # version
            reader,
            writer,
            token,
        )

    # authenticate user with steam
    async def authenticate(self, stored_credentials=None):
        if not stored_credentials:
            return NextStep(
                "web_session", constants.STEAM_LOGIN_WINDOW_PARAMS, constants.STEAM_LOGIN_REJECT_COOKIES_COOKIE
            )  # steamcommunity login page, with redirect to api page
        self.stored_credentials = stored_credentials
        # validate stored credentials and return authentication
        return authentication.validate_credentials(stored_credentials)

    # second authentication step to setup the steam web api key
    async def pass_login_credentials(self, step, credentials, cookies):
        return authentication.get_steamid_and_web_api_key(self, cookies)

    # required
    async def get_owned_games(self):
        steam_owned_game_list = backend.get_steam_owned_games(self.stored_credentials, True)
        #logging.log(logging.DEBUG,"get_owned_games")
        game_list = []

        for game in steam_owned_game_list.get("response").get("games"):
            game_list.append(
                Game(
                    str(game.get("appid")),
                    game.get("name"),
                    None,
                    LicenseInfo(LicenseType.SinglePurchase),
                )
            )

        return game_list

    async def prepare_game_times_context(self, game_ids) -> Any:
        return await backend.get_steam_game_times(self.stored_credentials, game_ids)

    async def get_game_time(self, game_id, context) -> GameTime:
        game_time = context.get(game_id)
        logging.debug(f"Updating time for game_id: {game_id}")
        logging.debug("game_id: "+str(game_time.game_id))
        logging.debug("time_played: "+str(game_time.time_played))
        logging.debug("last_played_time: "+str(game_time.last_played_time))
        return game_time
        #return GameTime(game_id=game_id, time_played=game_time.get("time_played"), last_played_time=game_time.get("last_played_time"))
    
            
def main():
    create_and_run_plugin(SteamIntegrationPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()
