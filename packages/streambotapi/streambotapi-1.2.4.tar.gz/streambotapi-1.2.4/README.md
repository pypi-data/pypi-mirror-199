# StreamBotAPI
StreamBotAPI is a Python package that provides a simple Flask-based API for interacting with the StreamBot which is a wrapper of OpenAI's ChatGPT.

## Installation
StreamBotAPI can be installed using pip:

```shell
pip install streambot-api
```

## Usage
To use StreamBotAPI, first initialize an instance of the StreamBot class from the [streambot](https://pypi.org/project/streambot) package:

```python
from streambot import StreamBot

streambot = StreamBot(
    openai_key='your_openai_key',
    bot_name='your_bot_name',
    genesis_prompt='You are a helpful translator.'
)
```

You can then create an instance of the StreamBotAPI class by passing in the initialized StreamBot object:

```python
from streambot_api import StreamBotAPI

server = StreamBotAPI(streambot, host='127.0.0.1', port=8080, origins=['http://localhost:3000', 'https://myapp.com'])
server.start()
```

This will start the Flask app with the specified configuration options and routes.

## Configuration Options
The StreamBotAPI class takes the following configuration options:

* streambot: An instance of the StreamBot class from the streambot package.
* host: The hostname to listen on. Defaults to 0.0.0.0.
* port: The port of the web server. Defaults to 80.
* origins: A list of allowed origins for CORS. Defaults to ['*'].

## Routes
The following routes are available:

### GET /api/getmessages/<user_id>
Returns a JSON object containing all messages for the specified user.

### POST /api/messages
Handles incoming chat messages from the user. Expects a JSON payload with the following fields:

connection_id: A unique ID for the user.
message: The message from the user.
Returns a JSON object containing all messages for the user.

### POST /api/newchat
Resets the chat history for the specified user. Expects a JSON payload with the following field:

connection_id: A unique ID for the user.
Returns a JSON object with a value of true.

## License
This package is licensed under the MIT license. See the LICENSE file for more details.