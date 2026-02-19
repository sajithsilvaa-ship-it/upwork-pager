import feedparser, requests, os

def check_jobs():
    url = os.getenv("UPWORK_RSS")
    # 🕵️ STEALTH MODE: This pretends to be a real Chrome browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    # Fetch the feed using the stealth header
    response = requests.get(url, headers=headers)
    feed = feedparser.parse(response.content)
    
    total = len(feed.entries)
    
    # Send one confirmation to Telegram
    requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                  json={"chat_id": os.getenv("CHAT_ID"), "text": f"✅ Stealth Bot Online. Found {total} new jobs."})

    # Ping the top 3 jobs found
    for entry in feed.entries[:3]:
        msg = f"🎯 <b>NEW JOB</b>\n\n{entry.title}\n\n<a href='{entry.link}'>Open on Upwork</a>"
        requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                      json={"chat_id": os.getenv("CHAT_ID"), "text": msg, "parse_mode": "HTML"})

if __name__ == "__main__":
    check_jobs()
