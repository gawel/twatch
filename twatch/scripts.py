# -*- coding: utf-8 -*-
import asyncio
from chut import console_script
from chut import path
from chut import ini
from .watcher import Watcher
from .formater import print_real_tweet


@console_script(fmt='brief')
def main(args):
    """Usage: %prog [-o] [-c CONFIG]
    """
    config = ini(args['CONFIG'] or path('~/.twatch.cfg'))
    loop = asyncio.get_event_loop()
    w = Watcher(config, callback=print_real_tweet, loop=loop)
    if args['-o']:
        loop.run_until_complete(w.searches())
    else:
        loop.run_until_complete(w.watch())
