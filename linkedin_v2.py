from flask import Flask, request, redirect, jsonify, url_for
import requests
import logging

app = Flask(__name__)

# Configure your LinkedIn credentials
CLIENT_ID = '86xzkc4jw7qcjh'
CLIENT_SECRET = 'rpQNeH4C6hvjxstO'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
# This should match the Authorized Redirect URL in your LinkedIn app settings

# Set up basic logging to stdout which might help in debugging
logging.basicConfig(level=logging.DEBUG)


def get_access_token(code):
    auth_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    auth_payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(auth_url, data=auth_payload, headers=headers)
    if response.status_code != 200:
        app.logger.error(f'Failed to get access token: {response.text}')
    response.raise_for_status()  # Raise an exception for HTTP error codes
    return response.json()['access_token']


def get_last_10_posts(access_token, organization_urn):
    api_url = f'https://api.linkedin.com/v2/shares?q=organization&organization={organization_urn}&count=10&sortBy=LAST_MODIFIED'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        app.logger.error(f'Failed to get posts: {response.text}')
    response.raise_for_status()
    return response.json().get('elements')


@app.route('/login')
def login():
    # Redirect the user to LinkedIn for authentication
    linkedin_auth_url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code'
    linkedin_auth_full_url = f'{linkedin_auth_url}&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=r_liteprofile%20r_emailaddress%20w_member_social'
    return redirect(linkedin_auth_full_url)


@app.route('/callback')
def callback():
    try:
        code = request.args.get('code')
        app.logger.debug(f'Code received: {code}')
        access_token = get_access_token(code)
        app.logger.debug(f'Access token: {access_token}')
        # For example, let's assume Microsoft's LinkedIn page URN is 'urn:li:organization:1035'
        posts = get_last_10_posts(access_token, 'urn:li:organization:1035')
        return jsonify(posts)
    except Exception as e:
        app.logger.error(f'An error occurred: {e}')
        # Return a generic error message
        return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
