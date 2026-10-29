"""Fetch live quotes for the dashboard and write quotes.json next to index.html."""
import json, sys, time, urllib.request

SYMBOLS = {"NVDA": "NVDA", "TSLA": "TSLA", "DOGE": "DOGE-USD", "NASDAQ": "^IXIC"}

def chart(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(sym)}?range=1d&interval=5m"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        meta = json.load(r)["chart"]["result"][0]["meta"]
    price, prev = meta["regularMarketPrice"], meta.get("chartPreviousClose") or meta.get("previousClose")
    pct = meta.get("regularMarketChangePercent")
    if pct is None and prev:
        pct = (price - prev) / prev * 100
    return {"price": price, "changePct": round(pct, 3)}

out = {"updated": int(time.time()), "quotes": {}}
for name, sym in SYMBOLS.items():
    try:
        out["quotes"][name] = chart(sym)
    except Exception as e:  # one bad symbol shouldn't break the deploy
        print(f"{name}: {e}", file=sys.stderr)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "quotes.json", "w"))
print(json.dumps(out))
