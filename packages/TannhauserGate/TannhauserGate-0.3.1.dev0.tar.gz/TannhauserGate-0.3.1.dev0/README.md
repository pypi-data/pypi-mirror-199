# Tannhauser Gate Atomic Swap

## Video Showcase (YouTube)

[![Video](https://img.youtube.com/vi/qfZ3Hac58Pw/0.jpg)](https://youtu.be/watch?v=qfZ3Hac58Pw "TannhauserGate")

## Installation

```
python3 -m venv venv
. venv/bin/activate
pip install TannhauserGate
tannhauser
```

## Depends

**Tannhauser Gate depends at [Tor](https://github.com/torproject/tor), [BitcoinCore](https://github.com/bitcoin/bitcoin) and [LitecoinCore](https://github.com/litecoin-project/litecoin). Please install it first. You will find sample config files [here](https://github.com/TannhauserGate420/tannhauser/tree/main/atomicswap/contrib).**

## Transactions:

|           Action | TXID                                                         |
| ---------------: | ------------------------------------------------------------ |
|      Client Bond | https://chain.so/tx/BTC/1242b63342d6222a55cfb7c339142acb3e23937b255aeb108a6783ddad56b07c |
|       TG Funding | https://chain.so/tx/LTC/b9bf6e608636560084f0abdb2a552feaaa18452439c90c0c38abc77c0976fddc |
|   Client Funding | https://chain.so/tx/BTC/756c491c236a1ff87feb10f72001fc2450f1815333b38995f23daf034e17fdb0 |
| TG Bond withdraw | https://chain.so/tx/BTC/503ba2a313de754ee850340dd8aac601df11c3586d115abd8c647ce34bf3e46c |
| TG Swap withdraw | https://chain.so/tx/BTC/24872849fef2f7ee6a284b675eb28c9d2a16bf8b550f586cd185004588dcdf14 |
|  Client withdraw | https://chain.so/tx/LTC/9349b37068f8cffb04d7327c2d92930f3d7771999e31d2e8362c8bb03d7a23f0 |

## Notes

**Tannhauser Gate  is a simple POC for an automatic atomic swap service. Tannhauser  is still in development mode - so use it at your own risk. For the Litecoin connection Tannhauser uses a customized version of python-bitcoinlib. There is a simple GUI as wrapper for easy handling. The GUI is a little bit guerrilla - but it does the job. So if you are a QT wizard - feel free to make a PR. The GUI uses a different (additional) library for RPC in contrast to the CLI. For some reason the GUI produces a broken pipe error at irregular intervals and I don't have time to look into it at the moment. The main goal of the development is a simple p2p client, where the user can be both maker and taker. Currently I take a closer look at [GNUnet](https://www.gnunet.org/en/) to realize this in a safe way. Until then you can swap smaller amounts with Tannhauser. For Tannhauser there is a general refund window of 2 hours. Refunds for the user are possible after 1 hour or after 2 hours (Bond).**

## Donations

**I do not accept donations. If you have some sats left donate them to the [Torproject](https://donate.torproject.org/cryptocurrency/) or to the [EFF](https://supporters.eff.org/donate/join-eff-4).**
