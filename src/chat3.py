import json
import random
import time


class Message:

    def __init__(self, chunk):
        choice = chunk.get("choices")[0]
        self.is_start = choice.get("delta").get("role") == "assistant"
        self.is_finished = choice.get("finish_reason") == "stop"
        self.is_continue = not (self.is_start or self.is_finished)
        self.content = choice.get('delta').get('content')


class Chat:

    def chat(self):
        f = open("test")
        response = json.load(f)
        for chunk in response:
            start = time.time()
            time.sleep(random.randint(10, 30) / 200)
            yield Message(chunk)
            print(time.time() - start)


if __name__ == "__main__":
    a = Chat().chat()
    for aa in a:
        print(aa)
