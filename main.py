import requests, feedparser, os

def get_purity(title, desc):
    score = 0
    t_low, d_low = title.lower(), desc.lower()
    
    # 💎 GOLD FACTORS (Logic & Automation)
    gold_terms = ["flow", "logic", "automation", "matrixify", "bulk", "3pl", "routing", "metafields", "migration"]
    if any(x in t_low for x in gold_terms): score += 70
    if any(x in d_low for x in ["sync", "reconcile", "csv", "python"]): score += 20
    
    # ❌ TRASH FACTORS (Manual/Creative work)
    if any(x in t_low for x in ["design", "logo", "creative", "theme", "css", "va", "seo"]): score -= 60
    
    return max(0, min(100, score))

def get_action_plan(title, purity):
    if purity >= 85:
        return "🔥 PURE GOLD: High pay, low effort. Use AI to write the logic/script. 15-min fix."
    if purity >= 60:
        return "🛠️ TECHNICAL OPS: Solid money. AI can draft the migration plan for you."
    return "⚖️ EVALUATE: Standard task. Check if budget is worth the effort."

def check_jobs():
    url = os.getenv("UPWORK_RSS")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0',
        'Cookie': os.getenv("UPWORK_COOKIE") # 🍪 LOGGED IN AS INDIE
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            print("No new jobs in feed.")
            return

        for entry in feed.entries[:3]:
            purity = get_purity(entry.title, entry.description)
            
            # Only ping for decent quality (40%+)
            if purity >= 40:
                action = get_action_plan(entry.title, purity)
                
                msg = (
                    f"✨ <b>PURITY: {purity}%</b>\n\n"
                    f"<b>📍 JOB:</b> {entry.title}\n\n"
                    f"<b>🧠 ACTION:</b> {action}\n\n"
                    f"🔗 <a href='{entry.link}'>OPEN ON UPWORK</a>"
                )
                
                requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                              json={"chat_id": os.getenv("CHAT_ID"), "text": msg, "parse_mode": "HTML"})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_jobs()
