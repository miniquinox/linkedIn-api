# LinkedIn Posts and Comments Fetcher

## Overview
This project contains Python scripts to fetch and process LinkedIn posts and comments. It utilizes the `linkedin_api` package to interact with LinkedIn's API. The scripts are designed to retrieve posts from a specific LinkedIn user's profile and comments on a specific post, and then process this data into a more readable and structured format.

## Features
- Fetching LinkedIn posts for a specified user.
- Fetching comments for a specific LinkedIn post.
- Formatting the fetched data into structured JSON.
- Saving the formatted data into JSON files.
- Credentials management through a `credentials.txt` file.

## Requirements
- Python 3
- `linkedin_api` package

## Setup
1. Clone or download this repository to your local machine.
2. Install the required Python package: `pip install linkedin_api`.
3. Create a `credentials.txt` file in the same directory as the scripts with your LinkedIn login credentials.

## `credentials.txt` File
This file should contain your LinkedIn username and password in the following format:

```
username:your_email@example.com
password:your_password
```

**Note**: Ensure that `credentials.txt` is secure and not exposed publicly.

## Usage
To run the scripts, use the following commands in your terminal:

### Fetching LinkedIn Posts
```bash
python final_posts.py
```

### Fetching LinkedIn Comments
```bash
python final_comments.py
```

## Output
The scripts will output formatted LinkedIn posts and comments data into JSON files in a `temp` directory.