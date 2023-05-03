import requests
from bs4 import BeautifulSoup
import constants
from galaxy.api.types import (
    Authentication
)

import backend



def convertCookieListToDict(lst):
    res_dict = {}
    for i in range(0, len(lst)):
        if lst[i]["domain"] == "steamcommunity.com":
            res_dict[lst[i]["name"]] = lst[i]["value"]
    return res_dict


def add_credential_to_url(str, stored_credentials):
    return str+"&key="+stored_credentials.get(constants.STORED_CREDENTIAL_WEBPAPIKEY_KEY)

# validate steam api key by calling GetPlayerSummaries for the user's steamid 
def validate_credentials(stored_credentials):
    player_summaries_response = backend.get_player_summaries(stored_credentials)
   
    steamid = player_summaries_response.get("response").get("players")[0].get("steamid")   
    name = player_summaries_response.get("response").get("players")[0].get("personaname") 

    return Authentication(steamid, name)

def get_steamid_and_web_api_key(plugin, cookies):
    #get captured steamcomunity cookies for use in the api key form requests
    cookies_dict = convertCookieListToDict(cookies)
    keyText = ""

    # get steamID from cookievalue
    cookie_value = cookies_dict["steamLoginSecure"]
    steamID = cookie_value[: cookie_value.find("%7C%7C")]
    # get sessionid from cookievalue, in case we need it to submit the api key form
    sessionid = cookies_dict["sessionid"]

    print(f"steamID: {steamID}")
    print(f"sessionID: {sessionid}")

    # access the web api form
    api_form_response = requests.get("https://steamcommunity.com/dev/apikey", cookies=cookies_dict)

    # parse the reponse
    api_form_soup = BeautifulSoup(api_form_response.text, "html.parser")
    form_action = api_form_soup.find("form", id="editForm").get("action")

    # find out if the user already has a key, based on the form action
    # if the action is to revoke, the user already has a key setup and we can use it
    # if the action is to register, them we register one for them
    if form_action == constants.ACTION_REVOKE_KEY_URL:  # got the key, extract it
        print("Already has a key")
        paragraphText = api_form_soup.find("div", id="bodyContents_ex").p.string
        keyText = paragraphText[paragraphText.find(": ") + 2 :]

    elif form_action == constants.ACTION_REGISTER_KEY_URL:  # doesn't have a key, create a new one
        print("Needs a key")

        # build formdata
        form_data = {
            'domain': 'Created by GOG Galaxy Steam Integration',
            'agreeToTerms':'agreed', #valve is going to kill me because of this
            'sessionid':sessionid,
            'Submit':'Register'
        }

        # submit key request form
        register_response = requests.post(constants.ACTION_REGISTER_KEY_URL, data=form_data, cookies=cookies_dict)

        # parse response and extract the key
        register_soup = BeautifulSoup(register_response.text, "html.parser")
        paragraphText = register_soup.find("div", id="bodyContents_ex").p.string
        keyText = paragraphText[paragraphText.find(": ") + 2 :]

    print(f"keyText: {keyText}")

    credentials = {
        constants.STORED_CREDENTIAL_STEAMID_KEY: steamID,
        constants.STORED_CREDENTIAL_WEBPAPIKEY_KEY: keyText
    }

    plugin.store_credentials(credentials)

    plugin.stored_credentials = credentials

    return validate_credentials(plugin.stored_credentials)
