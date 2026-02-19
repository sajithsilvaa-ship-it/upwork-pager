import requests, feedparser, os, time, random

def check_jobs():
    # 🕵️ HUMAN JITTER: Waits between 1 and 480 seconds (up to 8 mins) 
    # This makes the timing look random to Upwork.
    delay = random.randint(1, 480)
    print(f"Human Jitter: Waiting {delay} seconds before checking...")
    time.sleep(delay)

    url = os.getenv("UPWORK_RSS")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0',
        'Cookie': os.getenv("UPWORK_COOKIE")
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            return

        for entry in feed.entries[:3]:
            # (Insert Purity Logic below)
            t_low, d_low = entry.title.lower(), entry.description.lower()
            score = 0
            if any(x in t_low for x in ["flow", "logic", "automation", "matrixify", "bulk", "3pl", "routing"]): score += 70
            if any(x in d_low for x in ["sync", "reconcile", "csv", "python"]): score += 20
            if any(x in t_low for x in ["design", "logo", "creative", "theme", "css", "va", "seo"]): score -= 60
            
            purity = max(0, min(100, score))

            if purity >= 40:
                msg = f"✨ <b>PURITY: {purity}%</b>\n\n<b>📍 JOB:</b> {entry.title}\n\n🔗 <a href='{entry.link}'>Apply Now</a>"
                requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                              json={"chat_id": os.getenv("CHAT_ID"), "text": msg, "parse_mode": "HTML"})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_jobs()
