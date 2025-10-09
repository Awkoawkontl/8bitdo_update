#!/usr/bin/env python3
import csv, sys, json, time, argparse, socket
from urllib import request, error as urlerror

BASE_URL = "http://dl.8bitdo.com:8080/firmware/select"

def fetch(t, beta=False, timeout=10):
    req = request.Request(BASE_URL, method="POST")
    req.add_header("Type", str(t))
    if beta:
        req.add_header("Beta", "1")
    with request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)

def fetch_with_retries(t, beta, timeout, retries=2, wait=0.2):
    for attempt in range(retries + 1):
        try:
            return fetch(t, beta=beta, timeout=timeout)
        except (urlerror.URLError, urlerror.HTTPError, TimeoutError, socket.timeout) as e:
            if attempt == retries:
                print(f"warn: Type={t} -> {e}", file=sys.stderr)
                return None
            time.sleep(wait * (2 ** attempt))

def main():
    ap = argparse.ArgumentParser(description="Dump 8BitDo model→type pairs to CSV.")
    ap.add_argument("--start", type=int, default=0, help="Starting Type value (default: 0)")
    ap.add_argument("--max", type=int, default=200, help="Highest Type value to try (inclusive)")
    ap.add_argument("--beta", action="store_true", help="Include Beta: 1 header")
    ap.add_argument("--sleep", type=float, default=0.03, help="Delay between requests (seconds)")
    ap.add_argument("--timeout", type=float, default=10, help="HTTP timeout (seconds)")
    ap.add_argument("--out", default="8bitdo_filename_type.csv", help="CSV output path")
    args = ap.parse_args()

    seen = set()

    for t in range(args.start, args.max + 1):
        data = fetch_with_retries(t, args.beta, args.timeout)
        if not data:
            continue
        for item in (data.get("list") or []):
            name = (item.get("fileName") or "").strip()
            typ = item.get("type")
            if name and typ is not None:
                seen.add((name, int(typ)))
        time.sleep(args.sleep)

    rows = sorted(seen, key=lambda x: (x[0].lower(), x[1]))

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fileName", "type"])
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.out}")

if __name__ == "__main__":
    main()

