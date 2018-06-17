#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Example run functions."""

import asyncio
import random

import util
from config import settings
from solver import Solver

# Max browsers to open
count = 10

def get_proxies():
    src = settings["proxy_source"]
    protos = ["http://", "https://"]
    if any(p in src for p in protos):
        f = util.get_page
    else:
        f = util.load_file

    future = asyncio.ensure_future(f(src))
    asyncio.get_event_loop().run_until_complete(future)
    result = future.result()
    return result.strip().split("\n")


async def work():
    # Chromium options and arguments
    options = {"ignoreHTTPSErrors": True, 
               "args": ["--timeout 5"]
    }

    proxy = random.choice(proxies)
    client = Solver(
        settings["pageurl"],
        settings["sitekey"],
        options=options,
        proxy=proxy
    )

    if client.debug:
        print (f'Starting solver with proxy {proxy}')

    answer = await client.start()
    return answer


async def main():
    tasks = [
            asyncio.ensure_future(work())
            for i in range(count)
        ]

    futures = await asyncio.gather(*tasks)
    for (i, future) in zip(range(count), futures):
        print(i, future)


proxies = get_proxies()
print(len(proxies), "Loaded")

asyncio.get_event_loop().run_until_complete(main())