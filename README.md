# token-market-check

A tiny command-line tool that answers one question: **does this token actually have a market?**

Give it a token contract address and it lists every trading pair from DexScreener, with price, liquidity and 24h volume, plus a plain verdict: `NO MARKET`, `THIN`, or `LIQUID`.

No API key needed. Python 3.8+ with the standard library only.

## Usage

```bash
python token_market_check.py 0x2170Ed0880ac9A755fd29B2688956BD959F933F8  # a real token
python token_market_check.py 0x... --min-liq 50000   # custom liquidity threshold
```

Example output:

```
0x... — 2 pair(s)

CHAIN      DEX          PRICE    LIQUIDITY    VOL 24H
bsc        pancakeswap  $0.00012     $26.3K      $1.2K

total liquidity: $26.3K
verdict: LIQUID (threshold: $10.0K)
```

## Why

Free-mint and airdrop tokens often look valuable on paper but have no pool to sell into. A price quote means nothing without liquidity. This checks the pool, not the promise.

## License

MIT
