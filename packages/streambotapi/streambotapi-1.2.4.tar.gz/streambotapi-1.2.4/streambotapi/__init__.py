import os
import logging
import eventlet
eventlet.monkey_patch(socket=True)
from tiktoken import encoding_for_model, get_encoding
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from streambot import StreamBot
import json

class StreamBotAPI:
    def __init__(self, streambots, host='0.0.0.0', port=80, origins=['*'], verbosity = 0, log_file=None, debug=False, allow_model_override=False):
        self.host = host
        self.port = port
        self.streambots = streambots
        self.origins = origins
        self.verbosity = verbosity
        self.log_file = log_file
        self.debug = debug
        self.allow_model_override = allow_model_override
        
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode="eventlet", cors_allowed_origins="*", websocket=True, log_output=self.debug)
        self.init_cors()
        self.init_routes()

        self.messages = {}
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        class StreamBotLogFormatter(logging.Formatter):
            def format(self, record):
                if hasattr(record, 'extra') and record.extra:
                    extra_items = []
                    for key, value in record.extra.items():
                        # Replace newline characters with the string "\n"
                        value_str = str(value).replace("\n", "\\n")
                        extra_items.append(f'{key}={value_str}')
                    extra_str = ' '.join(extra_items)
                    record.msg = f'{record.msg} {extra_str}'
                return super(StreamBotLogFormatter, self).format(record)


        formatter = StreamBotLogFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def init_cors(self):
        CORS(self.app, resources={r"/api/*": {"origins": self.origins}})

    def init_routes(self):
        self.app.route('/api/getmessages/<context_id>/<user_id>', methods=['GET', 'POST'])(self.get_messages)
        self.app.route('/api/message', methods=['POST'])(self.handle_message)
        self.app.route('/api/chat', methods=['POST'])(self.handle_messages)
        self.app.route('/api/newchat', methods=['POST'])(self.reset_chat)
        self.app.route('/api/addmessages', methods=['POST'])(self.add_messages)
        self.app.route('/api/gettokencount', methods=['POST'])(self.get_tokens)

    def chat_stream(self, messages, context_id, model=None):
        for event in self.streambots[int(context_id)].chat_stream(messages, model=model):
            yield event

    def get_messages(self, context_id, user_id):
        connection_id = f"{context_id}_{user_id}"
        if connection_id in self.messages:
            return jsonify(self.messages[connection_id])
        else:
            self.messages[connection_id] = self.streambots[int(context_id)].messages.copy()
            if self.verbosity >= 1:
                self.logger.info(f'{user_id} got init messages for {context_id}', extra={'extra':{'messages': json.dumps(self.messages[connection_id])}})
            return jsonify(self.messages[connection_id])

    def get_tokens(self):
        messages = request.json.get('messages')
        model = request.json.get('model')
        try:
            encoding = encoding_for_model(model)
        except KeyError:
            encoding = get_encoding("cl100k_base")
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return jsonify({"tokencounts": num_tokens})

    def handle_message(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        model = None
        if self.allow_model_override and request.json.get('model'):
            model = request.json.get('model')
        message = request.json.get('message')
        if connection_id in self.messages:
            self.messages[connection_id].append({"role": "user", "content": message})
        else:
            self.messages[connection_id] = [{"role": "user", "content": message}]
        if self.verbosity >= 1:
            self.logger.info(f'{user_id} added message', extra={'extra':{"role": "user", "content": message}})
        
        def emit_callback(messages = None):
            response = ""
            if messages:
                chat = messages
            else:
                chat = self.messages[connection_id]
            for event in self.chat_stream(chat, context_id=context_id, model=model):
                response += event
                self.socketio.emit('message', {'message': event, 'connection_id': connection_id}, room=user_id)
            self.messages[connection_id].append({"role": "assistant", "content": response})
            if self.verbosity >= 1:
                self.logger.info(f'{user_id} added message', extra={'extra':{"role": "assistant", "content": response}})
            self.socketio.emit('message_complete', {'message_completed': True, 'connection_id': connection_id, 'message': response.replace('[START_OF_STREAM]','')}, room=user_id)
            return jsonify(self.messages[connection_id])
        
        self.socketio.emit('emit_event', callback=emit_callback, room=user_id)

        @self.socketio.on('callback_event')
        def handle_callback_event(data):
            if data is not None and 'messages' in data:
                messages = data['messages']
                emit_callback(messages)
            # call the emit_callback() function to complete the loop
            emit_callback()

        return 'OK', 200
    
    def handle_messages(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        model = None
        if self.allow_model_override and request.json.get('model'):
            model = request.json.get('model')
        
        def emit_msgs_callback(messages):
            response = ""
            for event in self.chat_stream(messages, context_id=context_id, model=model):
                response += event
                self.socketio.emit('message', {'message': event, 'connection_id': connection_id}, room=user_id)

            self.socketio.emit('message_complete', {'message_completed': True, 'connection_id': connection_id, 'message': response.replace('[START_OF_STREAM]','')}, room=user_id)
            return jsonify(response)
        
        self.socketio.emit('emit_msgs_event', callback=emit_msgs_callback, room=user_id)

        @self.socketio.on('callback_msgs_event')
        def handle_callback_event(data):
            if data is not None and 'messages' in data:
                messages = data['messages']
                emit_msgs_callback(messages)

        return 'OK', 200


    
    def add_messages(self):
        #use this method to add messages without triggering ChatGPT response
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        message = request.json.get('message')
        role = request.json.get('role')

        if connection_id in self.messages:
            self.messages[connection_id].append({"role":role,"content":message})
        else:
            self.messages[connection_id] = self.streambots[int(context_id)].messages.copy()
            self.messages[connection_id].append({"role":role,"content":message})
        if self.verbosity >= 1:
            self.logger.info(f'{user_id} added message', extra={'extra':{"role": role, "content": message}})
        return jsonify(True)

    def reset_chat(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        if connection_id in self.messages:
            self.messages[connection_id] = self.streambots[int(context_id)].messages.copy()
        return jsonify(True)

    def start(self):
        self.socketio.run(self.app, host=self.host, port=self.port, debug=self.debug, log_output=self.debug)
