import disoauther.exceptions as exceptions
import requests

__author__ = ["ecriminals", "functionally"]
__version__ = "0.0.1"

class DisOAuther:
    def __init__(
      self, 
      _client_id, 
      _client_secret, 
      _redirect_uri, 
      _guild_id
    ):
        """
        Initiate DisOAuther Client. 
        """
        self._client_id = _client_id
        self._client_secret = _client_secret
        self._redirect_uri = _redirect_uri
        self._guild_id = _guild_id
        self._session = requests.Session()

    def oauth(self, code: str):
        """
        `code`: OAuth Code Used For Obtaining Access Code.
        
        Code Responsible For Getting Access Token Using OAuth Code.
        """
        _res = self._session.post(
            "https://discord.com/api/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self._redirect_uri,
            },
        )
        if "Cloudflare" in _res.text:
            raise exceptions.Cloudflare()
        else:
            return _res.json()["access_token"]

    def guild_pull(self, bot_token: str, user_token: str, user_id: int):
        """
        `bot_token`: The Token Of The Bot Used To Authorize The User.
        
        `user_token`: The Access Token Of The User That You're Trying To Pull.

        `user_id`: The ID/UID Of The User That You're Trying To Pull.
        
        Pull A Member/User Into A Guild Using The Bot Token & User ID.
        """
        _res = self._session.put(
            f"https://discord.com/api/guilds/{self._guild_id}/members/{user_id}",
            headers={
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json",
            },
            json={"access_token": user_token},
        )
        if "Cloudflare" in _res.text:
            raise exceptions.Cloudflare()
        else:
            return _res.json()["access_token"]

    def get_userinfo(self, token: str):
        """
        `token`: The Access Token Of The User You Need To Obtain Information About.

        Obtain Account Information About The User Using Their Access Token.
        """
        _res = self._session.get(
            "https://discord.com/api/users/@me",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        if "Cloudflare" in _res.text:
            raise exceptions.Cloudflare()
        else:
            return _res.json()["access_token"]
