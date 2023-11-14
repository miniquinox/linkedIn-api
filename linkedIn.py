import logging
from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Define your LinkedIn application credentials
client_id = '86xzkc4jw7qcjh'
client_secret = 'rpQNeH4C6hvjxstO'
redirect_uri = 'http://127.0.0.1:5000/callback'
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
state = '123456'  # This should be a randomly generated value in production!

@app.route('/')
def login():
    try:
        # Step 1: Redirect the user to LinkedIn's OAuth 2.0 authorization page to get the authorization code.
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': state,
            'scope': 'openid profile w_member_social email',
        }

        auth_url = requests.Request('GET', authorization_base_url, params=params).prepare().url
        return redirect(auth_url)
    except Exception as e:
        app.logger.error('An error occurred during the login process: %s', e)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/callback')
def callback():
    # Step 2: Capture the code parameter LinkedIn sends to our callback URL
    code = request.args.get('code')
    returned_state = request.args.get('state')

    # Check if the state matches to prevent CSRF attacks
    if returned_state != state:
        return "Error: State value did not match. Possible CSRF attack.", 400

    if not code:
        return "Error: No code parameter provided by LinkedIn. Check your application settings.", 400

    # Step 3: Exchange the authorization code for an access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if 'access_token' not in token_json:
        return f"Error obtaining access token. {token_json.get('error_description')}", 400

    access_token = token_json['access_token']

    # At this point, you have the access token and can make authenticated LinkedIn API calls.
    # Example: Fetching profile details (just for demonstration)
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
    return profile_response.json()

if __name__ == '__main__':
    app.run(debug=True)