import http.client
import json

def test():

    conn = http.client.HTTPSConnection("api.openai.com")
    payload = json.dumps({
       "model": "gpt-3.5-turbo-16k",
       "messages": [
          {
             "role": "user",
             "content": "Write a Fibonacci function using Rust"
          }
       ],
    })
    headers = {
       'Accept': 'application/json',
       'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
       'Content-Type': 'application/json',
       "Authorization": "Bearer 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"
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')


if __name__ == "__main__":
    print(test())
