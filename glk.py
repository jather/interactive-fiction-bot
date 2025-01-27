import pexpect
import sys
import json


class GLKSession:
    def __init__(self, game_path, channel_id):
        self.channel_id = channel_id
        self.gen = 0
        session = pexpect.spawnu("./git " + game_path)
        session.logfile = sys.stdout
        to_send = '{"type": "init", "gen": 0, "support": [], "metrics": {"width":80,"height":24}}'
        session.sendline(to_send)
        session.expect("\r\n\r\n")
        response = json.loads(session.before.replace(to_send, ""))

    def end_session(self):
        pass

    def send(self, message):
        pass


GLKSession("stories/CounterfeitMonkey-11.gblorb")
