import feedparser, requests, os, time

def get_purity(title, desc):
    score = 0
    t_low, d_low = title.lower(), desc.lower()
    # 💎 GOLD FACTORS
    if any(x in t_low for x in ["flow", "logic", "automation", "matrixify", "bulk", "3pl", "routing", "metafields"]): score += 70
    if any(x in d_low for x in ["sync", "migration", "workflow", "reconcile", "csv"]): score += 20
    # ❌ TRASH FACTORS
    if any(x in t_low for x in ["design", "logo", "creative", "theme", "css", "va"]): score -= 60
    return max(0, min(100, score))

def check_jobs():
    url = os.getenv("UPWORK_RSS")
    # 🕵️ THE HUMAN FINGERPRINT: Prevents Upwork from blocking the bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            # If Upwork blocks us, the bot will tell you exactly why
            requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                          json={"chat_id": os.getenv("CHAT_ID"), "text": f"⚠️ Bot Blocked: Upwork returned Error {response.status_code}. Need to update RSS link."})
            return

        feed = feedparser.parse(response.content)
        if not feed.entries:
            print("Feed empty. No new jobs found.")
            return

        for entry in feed.entries[:5]:
            purity = get_purity(entry.title, entry.description)
            if purity >= 40:
                action = "🔥 PURE GOLD: Use AI for logic/Python script." if purity >= 80 else "🛠️ DATA OPS: Use AI to plan the migration."
                msg = (
                    f"✨ <b>PURITY: {purity}%</b>\n"
                    f"<b>📍 JOB:</b> {entry.title}\n"
                    f"<b>🧠 ACTION:</b> {action}\n\n"
                    f"🔗 <a href='{entry.li
