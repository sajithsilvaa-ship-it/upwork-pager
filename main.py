import feedparser, requests, os

def get_purity(title, desc):
    score = 0
    # 💎 GOLD FACTORS (Logic, Automation, Bulk)
    if any(x in title.lower() for x in ["flow", "logic", "automation", "matrixify", "bulk", "3pl", "routing"]): score += 60
    if any(x in desc.lower() for x in ["metafields", "sync", "migration", "workflow"]): score += 20
    if "$" in desc or "budget" in desc.lower(): score += 10
    
    # ❌ TRASH FACTORS (Manual work, Design)
    if any(x in title.lower() for x in ["design", "logo", "creative", "theme", "css"]): score -= 50
    if "data entry" in desc.lower(): score -= 30
    
    return max(0, min(100, score))

def get_action_plan(title, purity):
    t = title.lower()
    if purity >= 80:
        return "🔥 PURE GOLD: Use AI (ChatGPT/Claude) to write the Liquid code or Flow logic. This is a 15-minute fix."
    if "matrixify" in t or "bulk" in t:
        return "🛠️ DATA PLAY: Use AI to write a Python script for CSV cleaning. Fast money."
    return "⚖️ EVALUATE: Standard technical ops. AI can draft the plan, you execute."

def check_jobs():
    url = os.getenv("UPWORK_RSS")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'}
    
    response = requests.get(url, headers=headers)
    feed = feedparser.parse(response.content)
    
    # Only look at the top 3 newest jobs
    for entry in feed.entries[:3]:
        purity = get_purity(entry.title, entry.description)
        
        # Only ping if it's at least 40% Purity (ignores junk)
        if purity >= 40:
            action = get_action_plan(entry.title, purity)
            
            # Extract budget if mentioned
            budget = "Fixed Price / See Link"
            if "Budget" in entry.description:
                budget = entry.description.split("Budget")[1][:20].replace(":", "").strip()

            msg = (
                f"✨ <b>PURITY: {purity}%</b>\n\n"
                f"<b>💰 BUDGET:</b> {budget}\n"
                f"<b>📍 JOB:</b> {entry.title}\n\n"
                f"<b>🧠 ACTION:</b> {action}\n\n"
                f"🔗 <a href='{entry.link}'>OPEN ON UPWORK</a>"
            )
            
            requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                          json={"chat_id": os.getenv("CHAT_ID"), "text": msg, "parse_mode": "HTML"})

if __name__ == "__main__":
    check_jobs()
