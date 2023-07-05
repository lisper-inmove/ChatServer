import json


class Response:

    def __init__(self, content, sender, action,
                 is_start=False, is_continue=False, is_finished=False):
        self.content = content
        self.sender = sender
        self.action = action
        self.is_start = is_start
        self.is_continue = is_continue
        self.is_finished = is_finished

    def to_json(self):
        return json.dumps({
            'content': self.content,
            'sender': self.sender,
            'action': self.action,
            'is_continue': self.is_continue,
            'is_start': self.is_start,
            'is_finished': self.is_finished,
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        content = json.loads(data['content'])
        return cls(content, data['sender'], data['action'], data['stop'])
