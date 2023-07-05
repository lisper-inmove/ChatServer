import json


class Request:

    def __init__(self, content, sender, action):
        self.content = content
        self.sender = sender
        self.action = action

    def to_json(self):
        return json.dumps({
            'content': self.content,
            'sender': self.sender,
            'action': self.action
        })

    def set_stop(self, stop):
        self.stop = stop

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        content = json.loads(data['content'])
        return cls(content, data['sender'], data['action'])
