from flask import Flask, jsonify, request
import json, time

app = Flask(__name__)

def load_profile():
    with open("data/profile.json") as f:
        return json.load(f)

@app.get("/profile")
def profile():
    return jsonify(load_profile())

@app.post("/bid")
def bid():
    # Buyer sends JSON like:
    # {"category":"gaming.hardware","bid_usd":0.05,"creative_url":"https://example.com/banner.png"}
    # We accept only if category is allowed and bid meets min.
    data = request.get_json(force=True, silent=True) or {}
    prof = load_profile()
    allowed = set(prof["attention_policy"]["allowed_categories"])
    min_bid = float(prof["attention_policy"]["min_bid_usd"])
    cat = data.get("category","")
    bid = float(data.get("bid_usd",0))
    if cat not in allowed or bid < min_bid:
        return jsonify({"accepted": False, "reason":"policy_or_bid_too_low", "min_bid":min_bid}), 406
    # TODO: integrate payment check before accept
    return jsonify({"accepted": True, "show_ad": data.get("creative_url",""), "timestamp": int(time.time())})

@app.get("/")
def index():
    return jsonify({"ok": True, "endpoints": ["/profile","POST /bid"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787)
