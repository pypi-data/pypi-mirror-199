import subprocess
import sys

import tiktoken_async


async def test_simple():
    # Note that there are more actual tests, they're just not currently public :-)
    enc = await tiktoken_async.get_encoding("gpt2")
    assert enc.encode("hello world") == [31373, 995]
    assert enc.decode([31373, 995]) == "hello world"
    assert enc.encode("hello <|endoftext|>", allowed_special="all") == [31373, 220, 50256]

    enc = await tiktoken_async.get_encoding("cl100k_base")
    assert enc.encode("hello world") == [15339, 1917]
    assert enc.decode([15339, 1917]) == "hello world"
    assert enc.encode("hello <|endoftext|>", allowed_special="all") == [15339, 220, 100257]

    for enc_name in tiktoken_async.list_encoding_names():
        enc = await tiktoken_async.get_encoding(enc_name)
        for token in range(10_000):
            assert enc.encode_single_token(enc.decode_single_token_bytes(token)) == token


async def test_encoding_for_model():
    enc = await tiktoken_async.encoding_for_model("gpt2")
    assert enc.name == "gpt2"
    enc = await tiktoken_async.encoding_for_model("text-davinci-003")
    assert enc.name == "p50k_base"
    enc = await tiktoken_async.encoding_for_model("text-davinci-edit-001")
    assert enc.name == "p50k_edit"
    enc = await tiktoken_async.encoding_for_model("gpt-3.5-turbo-0301")
    assert enc.name == "cl100k_base"


def test_optional_blobfile_dependency():
    prog = """
import tiktoken_async
import sys
assert "blobfile" not in sys.modules
"""
    subprocess.check_call([sys.executable, "-c", prog])
