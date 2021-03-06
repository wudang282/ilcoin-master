#!/usr/bin/env python3
# Copyright (c) 2014-2016 The Ilcoin Core developers
# All Rights Reserved. ILCoin Blockchain Project 2019©
"""Test running ilcoind with -reindex and -reindex-chainstate options.

- Start a single node and generate 3 blocks.
- Stop the node and restart it with -reindex. Verify that the node has reindexed up to block 3.
- Stop the node and restart it with -reindex-chainstate. Verify that the node has reindexed up to block 3.
"""

from test_framework.test_framework import IlcoinTestFramework
from test_framework.util import (
    start_nodes,
    stop_nodes,
    assert_equal,
)
import time

class ReindexTest(IlcoinTestFramework):

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 1

    def setup_network(self):
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir)

    def reindex(self, justchainstate=False):
        self.nodes[0].generate(3)
        blockcount = self.nodes[0].getblockcount()
        stop_nodes(self.nodes)
        extra_args = [["-debug", "-reindex-chainstate" if justchainstate else "-reindex", "-checkblockindex=1"]]
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir, extra_args)
        while self.nodes[0].getblockcount() < blockcount:
            time.sleep(0.1)
        assert_equal(self.nodes[0].getblockcount(), blockcount)
        print("Success")

    def run_test(self):
        self.reindex(False)
        self.reindex(True)
        self.reindex(False)
        self.reindex(True)

if __name__ == '__main__':
    ReindexTest().main()
