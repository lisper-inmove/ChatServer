import openai


def test():
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=[
            {'role': 'user', 'content': 'Write a Fibonacci function using Rust'}
        ],
        stream=True,
        api_key='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'
    )
    for chunk in response:
        yield chunk


if __name__ == "__main__":
    a = test()
    for aa in a:
        print(aa)
