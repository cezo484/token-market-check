#!/usr/bin/env python3
"""token-market-check: check whether a token has a liquid market.

Uses the DexScreener public API (no key needed). Give it a token contract
address and it lists every trading pair, with price, liquidity and 24h volume,
plus a plain verdict: NO MARKET, THIN, or LIQUID.

Usage:
    python token_market_check.py 0x...            # any EVM token address
    python token_market_check.py 0x... --min-liq 50000
"""
import argparse
import json
import sys
import urllib.request

API = "https://api.dexscreener.com/latest/dex/tokens/{}"


def fetch_pairs(address):
    req = urllib.request.Request(API.format(address), headers={"User-Agent": "token-market-check/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    return data.get("pairs") or []


def fmt_usd(value):
    if value is None:
        return "-"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.2f}"


def main():
    parser = argparse.ArgumentParser(description="Check whether a token has a liquid market.")
    parser.add_argument("address", help="token contract address (any EVM chain)")
    parser.add_argument("--min-liq", type=float, default=10_000,
                        help="liquidity in USD counted as LIQUID (default: 10000)")
    args = parser.parse_args()

    try:
        pairs = fetch_pairs(args.address)
    except Exception as exc:  # network or API error
        print(f"error: could not reach DexScreener ({exc})", file=sys.stderr)
        return 1

    if not pairs:
        print(f"{args.address}\nverdict: NO MARKET (no trading pairs found)")
        return 0

    total_liq = 0.0
    print(f"{args.address} — {len(pairs)} pair(s)\n")
    print(f"{'CHAIN':<10} {'DEX':<12} {'PRICE':>14} {'LIQUIDITY':>12} {'VOL 24H':>12}")
    for pair in sorted(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0, reverse=True):
        liq = (pair.get("liquidity") or {}).get("usd") or 0
        vol = (pair.get("volume") or {}).get("h24")
        total_liq += liq
        price = pair.get("priceUsd")
        print(f"{pair.get('chainId', '-'):<10} {pair.get('dexId', '-'):<12} "
              f"{('$' + price) if price else '-':>14} {fmt_usd(liq):>12} {fmt_usd(vol):>12}")

    verdict = "LIQUID" if total_liq >= args.min_liq else "THIN"
    print(f"\ntotal liquidity: {fmt_usd(total_liq)}")
    print(f"verdict: {verdict} (threshold: {fmt_usd(args.min_liq)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
