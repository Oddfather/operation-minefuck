import json, collections, time
from pathlib import Path

SRC = Path("data/sample_events.jsonl")
OUT = Path("data/profile.json")

def load_events():
    with SRC.open() as f:
        for line in f:
            yield json.loads(line)

def main():
    events = list(load_events())
    by_cat = collections.defaultdict(list)
    for e in events:
        by_cat[e["category"]].append(e)

    top_interests = {}
    spend_month = 0.0
    for cat, es in by_cat.items():
        if cat == "audiobook.esoterica":
            minutes = sum(e["value"] for e in es)
            top = collections.Counter(e["detail"] for e in es).most_common(3)
            top_interests["audiobooks"] = {"minutes": minutes, "top_titles":[t for t,_ in top]}
        if cat == "gaming.purchases":
            spend = sum(float(e["value"]) for e in es)
            spend_month += spend
            top = collections.Counter(e["detail"] for e in es).most_common(3)
            top_interests["gaming"] = {"spend_month": round(spend,2), "top_types":[t for t,_ in top]}
        if cat == "temu.gadgets":
            spend = sum(float(e["value"]) for e in es)
            spend_month += spend
            top = collections.Counter(e["detail"] for e in es).most_common(3)
            top_interests["temu"] = {"spend_month": round(spend,2), "top_items":[t for t,_ in top]}

    profile = {
        "version": 1,
        "updated": int(time.time()),
        "demographic": {"age_range":"25-45","region":"US","confidence":0.5},
        "interests": top_interests,
        "attention_policy": {
            "allowed_categories": ["books.esoteric","gaming.hardware","tools.industrial","gadgets.novelty"],
            "blocked_categories": ["mlm.crypto","political","surveillance"],
            "min_bid_usd": 0.02,
            "max_ads_per_day": 10
        },
        "contact": {
            "payment": {"method":"lightning_or_tip","address":"set-me"},
            "message_url": "/offer"
        }
    }
    OUT.write_text(json.dumps(profile, indent=2))
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
