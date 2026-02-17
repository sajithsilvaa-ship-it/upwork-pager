import feedparser, requests, os

MUST_HAVE = ["logic", "automation", "flow", "workflow", "matrixify", "metafields", "3pl", "status"]
AVOID = ["design", "logo", "theme", "css", "html", "va", "data entry", "seo"]

def check_jobs():
    print("Checking for jobs...") # This shows in your GitHub logs
    feed = feedparser.parse(os.getenv("UPWORK_RSS"))
    
    # --- TEST LINE: This should send to your Telegram every time ---
    requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                  json={"chat_id": os.getenv("CHAT_ID"), "text": "🤖 Bot is online and searching..."})
    
    for entry in feed.entries[:10]:
        title, desc = entry.title.lower(), entry.description.lower()
        is_gold = any(w in title or w in desc for w in MUST_HAVE)
        is_junk = any(w in title or w in desc for w in AVOID)

        if is_gold and not is_junk:
            msg = f"💎 <b>GOLD MATCH</b>\n\n{entry.title}\n\n<a href='{entry.link}'>Apply Now</a>"
            requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                          json={"chat_id": os.getenv("CHAT_ID"), "text": msg, "parse_mode": "HTML"})

if __name__ == "__main__":
    check_jobs()
