:warning: Although the current release of the plugin is working, I'm still testing and figuring some stuff with help from my friends, regarding issues that may arise during instalation! :warning:

# galaxy-integration-steam
My attempt at creating a GOG galaxy steam integration that works by using Steam's Web API [https://steamcommunity.com/dev]

Currently, just the basic plugin with support for logging into your steam account, the retrieval/creation of your Steam Web API key and synchronization of your library and game time.

## How the plugin works
1. When the user connects the plugin, the plugin opens the following url: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey, using the GOG Galaxy built in browser
2. The user is prompted to login into their Steam account
3. Using the established session, the plugin accesses the Steam Web API form page to check if the user already had an wep api token that can be used

   - Each steam user can only have one web api token, all applications that the user wants to give access to their Steam Web API context have to share that one token
   - If the user does not have an API token, the plugin will submit the request form for the user, registering the token with "Created by GOG Galaxy Steam Integration" filled in the "Domain Name" field.

4. Having obtained the Web API token, the plugin implements GOG Galaxy Client methods for obtaining steam's data for the user, library, game time, etc..

With the token, the plugin will only have acess to the information described in the Steam Web API.s documentation: https://developer.valvesoftware.com/wiki/Steam_Web_API

The user can manually go to https://steamcommunity.com/dev/apikey and revoke the Web API token. The plugin will stop working and the GOG Galaxy client will notify the user to connect the plugin again.

## Installation
* Make sure the GOG Galaxy client is closed
* Get the latest release: https://github.com/Novettam/galaxy-integration-steam/releases/latest (download the zip file)
* Create a folder inside the GOG Galaxy plugin lookup folder<br>
`%localappdata%\GOG.com\Galaxy\plugins\installed\`
* Unzip the contents of the zip file into the newly created folder
* Start GOG Galaxy and connect the plugin
* Login into your steam account in the GOG Galaxy integrated browser
* The plugin will start synchronizing your steam game library and related information

## Roadmap
1.  :white_check_mark: Game Library (free games are still missing)
2.  :white_check_mark: Game Time
3.  :white_square_button: Achievements
4.  :white_square_button: Friends list
5. ??

## Contributing
* Clone the repo straight into the GOG Galaxy plugin lookup folder
* Run `pip install -r requirements.txt -t . --implementation cp --python-version 37 --only-binary=:all:` in the project folder
* Open GOG Galaxy, connect and check if everything is working
* Hack away, add new stuff, open a pull request
   
   * Don't commit packages you add, but don't forget to add them to the requirements.txt (still trying to figure ou a better way to manage this, coming from C# (nuget) and JS (npm), how I miss them!!)

### Development notes
You can debug by attaching to the python process, but the galaxy client will kill the process if it doesn't receive a reply after a while, which sucks, still have not found a way to disable that. (launching the client with the --debug=1 flag doesn't help with that)

###
This is a community created GOG Galaxy Steam integration plugin, as such:

It is not affiliated with, endorsed by, sponsored by, or endorsed by Valve Corporation, the owner of the Steam trademark. 

It is not affiliated with, endorsed by, sponsored by, or endorsed by CD PROJEKT S.A, the owner of the GOG and GOG GALAXY trademarks. 
