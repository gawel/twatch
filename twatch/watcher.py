# -*- coding: utf-8 -*-
from twitter import Twitter
from twitter import OAuth
from chut import path
from asyncio.queues import Queue
from functools import partial
import asyncio
import logging
import time


log = logging.getLogger('twatch')


def auth_factory(c):
    return OAuth(c['token'], c['token_secret'], c['key'], c['secret'])


class Watcher(object):

    def __init__(self, config, callback=None, loop=None):
        self.config = config
        self.conn = Twitter(auth=auth_factory(config['twitter']))
        self.callback = callback
        self.loop = loop
        self.queue = Queue(loop=loop)

        self.tid = 0
        self.storage = path('~/.twatch_last_id')
        if path.isfile(self.storage):
            with open(self.storage) as fd:
                self.tid = int(fd.read())

        self.queries = [(k, v) for k, v in self.config['twatches'].items()
                        if k != 'home']

    @asyncio.coroutine
    def watch(self):
        while True:
            try:
                yield from self.searches()
            except Exception as e:
                log.exception(e)

    @asyncio.coroutine
    def searches(self):
        ids = []
        for k, v in self.queries:
            resp = yield from self.search(q=v)
            if not resp:
                continue
            for r in resp['statuses']:
                if r['id'] > self.tid and r['id'] not in ids:
                    r['twatch'] = dict(key=k, query=v)
                    try:
                        self.callback(r)
                    except Exception as e:
                        log.exception(e)
                    else:
                        ids.append(r['id'])
            if resp.rate_limit_remaining == 0:
                reset = resp.rate_limit_reset - time.time()
                yield from asyncio.sleep(reset + 5, loop=self.loop)
            else:
                yield from asyncio.sleep(3, loop=self.loop)
        if ids:
            self.tid = max(ids)
            with open(self.storage, 'w') as fd:
                fd.write(str(self.tid))

    @asyncio.coroutine
    def search(self, q):
        q = ' '.join(q.replace('\n', ' ').split())
        meth = partial(self.conn.search.tweets, q=q, result_type='recent')
        try:
            res = yield from self.loop.run_in_executor(None, meth)
            return res
        except Exception as e:
            log.exception(e)
            return None
