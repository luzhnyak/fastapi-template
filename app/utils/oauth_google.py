import requests
from app.core.config import settings


def get_user_info(code, redirect_uri):

    session = requests.Session()
    # session.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0'}
    session.headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # session.headers = {'Host:': 'www.googleapis.com'}
    # POST /oauth2/v4/token HTTP/1.1

    url = "https://www.googleapis.com/oauth2/v4/token"

    params = {
        "client_id": settings.app.OAUTH_CLIENT_ID,
        "client_secret": settings.app.OAUTH_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code": code,
    }

    response = session.post(url, params=params)

    url = "https://www.googleapis.com/oauth2/v1/userinfo"

    params = {
        "access_token": response.json().get("access_token"),
        "fields": "id,name,email",
    }

    response = requests.get(url, params=params)
    return response.json()
