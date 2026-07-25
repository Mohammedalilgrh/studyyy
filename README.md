# 🚀 Puter To-Do List App with FREE Unlimited Claude AI

**100% FREE FOREVER** - No subscriptions, no API limits, no credit cards needed!

Combines:
- ✅ **Puter.js** - Cloud OS for unlimited free file storage
- ✅ **Free Claude Code** - Proxy to Claude models for FREE
- ✅ **Unlimited API Access** - Developers get unlimited free usage

## 🎯 Why This Project?

**The Problem:** Claude API costs money. LLM APIs are expensive.

**The Solution:** 
1. **Free Claude Code** - Run a local proxy that routes to free/cheap providers
2. **Puter Models** - Puter offers UNLIMITED FREE access for developers
3. **This App** - Use both together for a completely free AI-powered productivity tool

## ⚡ Key Features

✨ **100% FREE AI-Powered Features:**
- Task suggestions powered by Claude
- Smart prioritization (urgency, due date, complexity)
- Auto-categorization (Work, Personal, Shopping, etc.)
- Description expansion from brief titles
- Productivity analytics

☁️ **Unlimited Cloud Storage:**
- Sync todos to Puter cloud (unlimited free storage)
- Access from any device
- No data loss

🚀 **Production Ready:**
- Vue 3 + TypeScript
- TailwindCSS styling
- Docker support
- GitHub Actions CI/CD

## 🆓 The Free Stack

```
┌─────────────────────────────────────────┐
│  Puter To-Do App (This Repo)            │
│  Vue 3 + TypeScript + TailwindCSS        │
└────────────┬────────────────────────────┘
             │
             ├──► Puter.js (Cloud Storage)
             │    └─ UNLIMITED FREE for devs
             │
             └──► Free Claude Code (Local Proxy)
                  ├─ UNLIMITED FREE for devs via Puter
                  └─ Routes to Puter's Claude models
```

## 🚀 Quick Start (5 mins)

### 1. Install Free Claude Code (One-time setup)

**macOS/Linux:**
```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh
```

**Windows PowerShell:**
```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1")))
```

### 2. Configure Puter Provider (In Free Claude Code)

When prompted during installation, set up Puter:
1. Go to [puter.com](https://puter.com) → Settings → API Keys
2. Copy your **Puter API Key**
3. Run `fcc-server` (the admin UI opens at http://127.0.0.1:8082/admin)
4. Set `MODEL_CONFIG`:
   - Provider: `puter` (if available)
   - Or use OpenRouter free tier which supports Claude models

**Option A: Use Puter (RECOMMENDED - Unlimited Free)**
```bash
# Export your Puter API key
export PUTER_API_KEY=your_key_here
fcc-server
```

**Option B: Use OpenRouter (FREE tier available)**
```bash
# Get free key: https://openrouter.ai/keys
export OPENROUTER_API_KEY=your_key_here
fcc-server
```

### 3. Clone & Setup This App

```bash
git clone https://github.com/Mohammedalilgrh/putercfree.git
cd putercfree
npm install
```

### 4. Create .env.local

```env
# Get from puter.com/settings/api
VITE_PUTER_API_KEY=sk-...

# Free Claude Code proxy (already running)
VITE_FREE_CLAUDE_URL=http://localhost:8082
VITE_FREE_CLAUDE_TOKEN=freecc
```

### 5. Run Both (in separate terminals)

**Terminal 1 - Free Claude Code Server:**
```bash
fcc-server
# Keeps running in background
```

**Terminal 2 - Your Todo App:**
```bash
npm run dev
# Opens http://localhost:5173
```

## 💰 Cost Breakdown

| Component | Cost | Why Free |
|-----------|------|----------|
| **Puter.js** | $0 | Unlimited free storage for devs |
| **Claude API** | $0 | Free Claude Code + Free provider (Puter/OpenRouter) |
| **This App** | $0 | Open source MIT license |
| **Domain** | $0 | Deploy free on Vercel/Netlify |
| **Hosting** | $0 | Free tier options available |
| **Total** | **$0** | **Forever Free** |

## 🤖 How The AI Works (FREE)

### You Run Locally:
1. **Free Claude Code Server** - Local proxy on port 8082
   - Intercepts API calls
   - Routes to free provider
   - No external API calls to Anthropic

### Connection Flow:
```
Your App → Free Claude Code (Local)
              ↓
         Routes to Puter Models
         (Unlimited free for devs)
              ↓
         Returns Claude responses
         (No Anthropic API charges)
```

### Puter Unlimited Free Features:
- ✅ Claude models (full capability)
- ✅ Unlimited API calls
- ✅ No rate limiting
- ✅ For development use
- ✅ No credit card needed

## 📁 Project Structure

```
putercfree/
├── src/
│   ├── components/          # Vue 3 components
│   │   ├── TodoList.vue
│   │   ├── TodoForm.vue
│   │   ├── TodoItem.vue
│   │   ├── AIAssistant.vue  # ← FREE AI features
│   │   └── TaskStats.vue
│   ├── services/
│   │   ├── puter.ts         # FREE cloud storage
│   │   ├── claude.ts        # FREE AI API calls
│   │   └── storage.ts
│   ├── stores/
│   │   └── todoStore.ts
│   └── App.vue
├── Dockerfile
├── package.json
└── README.md
```

## 🔧 AI Features (All Powered by FREE Claude)

### 1. Task Suggestions
```
💡 "Based on your tasks, here's what you should do next..."
→ FREE Claude analyzes via Puter
→ No Anthropic API cost
```

### 2. Smart Prioritization
```
📊 "Reorder tasks by importance and due dates"
→ FREE Claude via Puter
→ Unlimited calls
```

### 3. Auto-Categorization
```
🏷️ "Sort into Work, Personal, Shopping, etc."
→ FREE Claude via Puter
→ Zero cost
```

### 4. Description Expansion
```
📝 Input: "Buy groceries"
→ Output: "Pick up fresh vegetables and dairy items at local supermarket"
→ FREE Claude via Puter
```

## 🚀 Production Deployment (FREE)

### Option 1: Vercel (Recommended)

```bash
# Push to GitHub
git push origin main

# Connect to Vercel: https://vercel.com
# Set environment variables:
# VITE_PUTER_API_KEY=your_key
# VITE_FREE_CLAUDE_URL=http://localhost:8082 (won't work on Vercel, use Puter API directly)
```

**Better for Production:**
Use Puter API directly in the app instead of local proxy:

```typescript
// Call Puter's Claude API directly
const response = await fetch('https://api.puter.com/ai/claude', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${PUTER_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'claude-3-5-sonnet',
    messages: [{role: 'user', content: prompt}]
  })
})
```

### Option 2: Docker (Your Server)

```bash
# Build
docker build -t putercfree .

# Run
docker run -p 3000:3000 \
  -e VITE_PUTER_API_KEY=your_key \
  putercfree
```

### Option 3: Netlify (FREE Tier)

1. Push to GitHub
2. Connect to Netlify
3. Build command: `npm run build`
4. Publish: `dist/`
5. Add environment variables

## 🔐 Security

- ✅ All data encrypted in Puter
- ✅ Your API keys stored securely
- ✅ No tracking or analytics
- ✅ No external services (except Puter)
- ✅ Open source for transparency

## 🐛 Troubleshooting

### "Cannot connect to Free Claude Code"

```bash
# Check if running
fcc-server --version

# Check port 8082
lsof -i :8082

# Restart
fcc-server
```

### "Invalid Puter API key"

1. Get key: https://puter.com/settings/api
2. Add to `.env.local`
3. Restart: `npm run dev`

### "Puter storage not syncing"

```bash
# Clear cache
rm -rf .puter-cache/

# Restart app
npm run dev
```

## 📚 References

- **Puter Docs**: https://docs.puter.com
- **Free Claude Code**: https://github.com/Alishahryar1/free-claude-code
- **Puter API Keys**: https://puter.com/settings/api
- **OpenRouter (Alternative)**: https://openrouter.ai

## 💡 Pro Tips for Maximum Savings

1. **Use Puter for everything** - Unlimited free for devs
2. **Run Free Claude Code locally** - No external API costs
3. **Cache responses** - Reduce API calls
4. **Batch operations** - Group multiple AI requests
5. **Use free hosting** - Vercel/Netlify free tier

## 🤝 Contributing

```bash
# Fork & clone
git clone https://github.com/YOUR_USERNAME/putercfree.git

# Create feature branch
git checkout -b feature/amazing-feature

# Commit
git commit -m 'Add amazing feature'

# Push & PR
git push origin feature/amazing-feature
```

## 📝 License

MIT - Use freely, forever.

## 🎉 The Promise

**This app will ALWAYS be:**
- ✅ 100% FREE
- ✅ Open Source
- ✅ No ads or tracking
- ✅ No locked features
- ✅ No forced upgrades

**Because:** We believe AI should be free for everyone.

---

**Made with ❤️ for developers who want unlimited AI without breaking the bank.**

⭐ Star this repo if you love free software!
