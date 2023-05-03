# galaxy-integration-steam
My attempt at creating a GOG galaxy steam integration that works by using Steam's Web API [https://steamcommunity.com/dev]

Currently, just the basic plugin with support for logging into your steam account, the retrieval/creation of your Steam Web API key and synchronization of your library and game time.

## The plugin works in the follwing maner:
1. When the user connects the plugin, the plugin opens the following url: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey" using the GOG Galaxy built in browser
2. The user is prompted to login
3. Using the established session, the plugin acesses the Steam Web API to check if the user already had an wep api token that can be used

   - Each steam user can only have one web api token, all applications that the user wants to give access to their Steam Web API context have to share that one tokem
   - If the user does not have an API token, the plugin will submit the request form for the user, registering the token with "Created by GOG Galaxy Steam Integration" filled in the "Domain Name" field.

4. Having obtained the Web API token, the plugin implements GOG Galaxy Client methods for obtaining steam's data for the user, library, game time, etc..

With the token, the plugin will only have acess to the information described in the Steam Web API.s documentation: https://developer.valvesoftware.com/wiki/Steam_Web_API

The user can manually go to https://steamcommunity.com/dev/apikey and revoke the Web API token. The plugin will stop working and the GOG Galaxy client will notify the user to connect the plugin again.





## Roadmap
1.  :white_check_mark: Game Library
2.  :white_check_mark: Game Time
3.  :white_square_button: Achievements
4.  :white_square_button: Friends list
5. ??
