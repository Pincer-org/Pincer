# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from pincer.objects import UserMessage


class Message:

    def __init__(self, content):
        self.content = content

    clean_content = UserMessage.clean_content


class TestUserMessages:

    def test_clean_content(self):
        assert Message('Hello, world!').clean_content == 'Hello, world!'
        assert Message('_*`Hello, world!`*_').clean_content == 'Hello, world!'
        assert Message('__~~Hello, world!~~__').clean_content == 'Hello, world!'
        assert Message('||Hello, world!||').clean_content == 'Hello, world!'
        assert Message('```py\nfoo\nbar\n```').clean_content == 'foo\nbar'
