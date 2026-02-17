import feedparser, requests, os

# 💎 THE SNIPER LIST: Only ping if it's high-value logic
MUST_HAVE = ["matrixify", "logic", "flow", "automation", "3pl", "routing", "metafields", "sync", "bulk", "inventory"]

# ❌ THE BLACKLIST: If these words appear, ignore the job completely
AVOID = ["design", "logo", "theme", "css", "html", "creative", "ui", "ux", "frontend", "seo"]

def check_jobs():
    # Use the RSS link from your Secrets
    feed = feedparser.parse(os.getenv("UPWORK_RSS"))
    
    # Check the latest 10 jobs
    for entry in feed.entries[:10]:
        title = entry.title.lower()
        desc = entry.description.lower()

        # Check if the job is a "Gold Match"
        is_gold = any(word in title or word in desc for word in MUST_HAVE)
        # Check if it's "Junk"
        is_junk = any(word in title or word in desc for word in AVOID)

        if is_gold and not is_junk:
            # Format the message for your phone
            msg = (
                f"🎯 <b>99% MATCH FOUND</b>\n\n"
                f"<b>Title:</b> {entry.title}\n\n"
                f"👉 <a href='{entry.link}'>OPEN IN UPWORK</a>\n\n"
                f"<i>Send the description to AI for the proposal!</i>"
            )
            
            # Send to your Telegram
            requests.post(
                f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                json={
                    "chat_id": os.getenv("CHAT_ID"), 
                    "text": msg, 
                    "parse_mode": "HTML"
                }
            )

if __name__ == "__main__":
    check_jobs()
