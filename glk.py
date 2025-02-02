import pexpect
import sys
import json
import discord


class GLKSession:
    def __init__(self, game_path):
        self.gen = 0
        self.session = pexpect.spawnu("./git " + game_path)
        self.session.logfile = sys.stdout
        # send init input to session
        self.to_send = '{"type": "init", "gen": 0, "support": [], "metrics": {"width":80,"height":24}}'
        self.session.sendline(self.to_send)
        self.handle_response()

    def get_response(self):
        return format_response(self.game_response)

    def end_session(self):
        self.session.terminate(force=False)

    def send(self, message):
        self.gen += 1
        self.to_send = (
            '{{"type": "{}", "gen": {}, "window": {}, "value": "{}"}}'.format(
                self.input_type,
                self.gen,
                self.window_id,
                message,
            )
        )
        self.session.sendline(self.to_send)
        # process the response
        self.handle_response()

    def handle_response(self):
        self.session.expect("\r\n\r\n")
        self.game_response = json.loads(self.session.before.replace(self.to_send, ""))
        if self.game_response["type"] == "error":
            raise Exception
        self.input_type = self.game_response["input"][0]["type"]
        self.window_id = self.game_response["content"][1]["id"]


def format_response(response_object):
    return response_object["content"][1]["text"]
