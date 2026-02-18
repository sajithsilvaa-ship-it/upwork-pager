import feedparser, requests, os

# 💎 THE GOLD LIST: High-paying or Easy-to-automate
MUST_HAVE = ["logic", "automation", "flow", "workflow", "matrixify", "metafields", "3pl", "status", "inventory", "bulk", "migration", "csv", "sync", "import"]

# ❌ THE JUNK LIST: Only block if these are in the TITLE (stops blocking good jobs)
AVOID_TITLE = ["design", "logo", "theme", "creative", "ui", "ux", "seo", "article", "writer", "va"]

def generate_proposal(title):
    base = "Hi! I saw your post regarding " + title + ". "
    if "migration" in title.lower() or "matrixify" in title.lower() or "bulk" in title.lower():
        pitch = "I am an expert in high-volume Shopify data management. I use Matrixify and custom Python scripts to handle complex migrations and bulk updates with 100% data integrity."
    elif "logic" in title.lower() or "flow" in title.lower():
        pitch = "I specialize in Shopify backend logic and Flow automation. I focus on building scalable systems—routing orders, managing inventory status, and automating manual tasks."
    else:
        pitch = "I am a Shopify Technical Operations specialist. I handle the technical 'heavy lifting' like app integrations, data reconciliation, and backend configuration so your store runs smoothly."
    
    closing = "\n\nI am detail-oriented, highly responsive, and can start immediately. Let’s get this sorted!\n- Indie"
    return base + pitch + closing

def check_jobs():
    print("Checking for jobs...")
    feed = feedparser.parse(os.getenv("UPWORK_RSS"))
    
    # Alert you that the bot is alive (optional, remove if annoying)
    # requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
    #               json={"chat_id": os.getenv("CHAT_ID"), "text": "🔎 Searching for Gold..."})

    for entry in feed.entries[:10]:
        title_lower = entry.title.lower()
        desc_lower = entry.description.lower()

        # Check if title contains junk
        is_junk_title = any(word in title_lower for word in AVOID_TITLE)
        
        # Check if description/title contains gold
        is_gold = any(word in title_lower or word in desc_lower for word in MUST_HAVE)

        if is_gold and not is_junk_title:
            proposal_draft = generate_proposal(entry.title)
            msg = (
                f"💎 <b>NEW JOB FOUND</b>\n\n"
                f"<b>Job:</b> {entry.title}\n\n"
                f"📝 <b>PROPOSAL:</b>\n<code>{proposal_draft}</code>\n\n"
                f"👉 <a href='{entry.link}'>Apply Now</a>"
            )
            requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", 
                          json={"chat_id": os.getenv("CHAT_ID"), "text": msg, "parse_mode": "HTML"})

if __name__ == "__main__":
    check_jobs()
