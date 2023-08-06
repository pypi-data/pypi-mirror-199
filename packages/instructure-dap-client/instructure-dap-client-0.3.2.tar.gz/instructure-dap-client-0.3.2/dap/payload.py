import io
import json
import zlib
from typing import AsyncIterator

import aiohttp
from strong_typing.core import JsonType


async def get_json_lines_from_stream(
    stream: aiohttp.StreamReader,
) -> AsyncIterator[JsonType]:
    "Extracts JSON objects from an uncompressed HTTP payload stream of content type JSONL."

    buf = io.BytesIO()
    async for data in stream.iter_chunked(1024 * 1024):
        start: int = 0
        while True:
            # find newline character
            end: int = data.find(10, start)
            if end >= 0:  # has newline, process data
                buf.write(data[start:end])
                buf.seek(0, io.SEEK_SET)
                yield json.load(buf)
                buf = io.BytesIO()
                start = end + 1
            else:  # has no newline, read more data
                buf.write(data[start:])
                break

    # process remaining data
    rem = buf.getvalue()
    if rem:
        yield json.loads(rem)


async def get_json_lines_from_gzip_stream(
    stream: aiohttp.StreamReader,
) -> AsyncIterator[JsonType]:
    "Extracts JSON objects from a gzipped HTTP payload stream of content type JSONL."

    # use a special value for wbits (windowBits) to indicate gzip compression
    # see: https://docs.python.org/3/library/zlib.html#zlib.decompress
    decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

    buf = io.BytesIO()
    async for chunk in stream.iter_chunked(1024 * 1024):
        data = decompressor.decompress(chunk)

        start: int = 0
        while True:
            # find newline character
            end: int = data.find(10, start)
            if end >= 0:  # has newline, process data
                buf.write(data[start:end])
                buf.seek(0, io.SEEK_SET)
                yield json.load(buf)
                buf = io.BytesIO()
                start = end + 1
            else:  # has no newline, read more data
                buf.write(data[start:])
                break

    # process remaining data
    rem = buf.getvalue()
    if rem:
        yield json.loads(rem)
