# Complete Setup Guide: FREE Unlimited Claude AI + Puter To-Do App

## Understanding the Stack

You're creating a system with:
1. **Puter** - FREE unlimited storage + FREE unlimited API for developers
2. **Free Claude Code** - Local proxy that routes to Puter's models
3. **To-Do App** - Uses both for completely free AI-powered task management

## Step-by-Step Setup

### Phase 1: Get Puter API Key (5 minutes)

1. Go to https://puter.com and sign up (free)
2. Navigate to Settings → API Keys
3. Create new API key (copy it somewhere safe)
4. You now have **UNLIMITED FREE API access** as a developer

### Phase 2: Install Free Claude Code (5-10 minutes)

This creates a local proxy server that uses Puter's FREE Claude models.

**macOS/Linux:**
```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh
```

When prompted:
- Choose to install Claude Code, Codex, Pi
- Answer yes to everything
- This installs Python + all dependencies

**Windows PowerShell:**
```powershell
# Run as Administrator
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1")))
```

### Phase 3: Configure Free Claude Code for Puter

Now you need to tell Free Claude Code to use Puter's FREE unlimited models.

**Terminal 1: Start the admin UI**
```bash
fcc-server
```

This starts the proxy server. You'll see:
```
INFO:     Admin UI: http://127.0.0.1:8082/admin (local-only)
```

**In your browser:**
1. Go to http://127.0.0.1:8082/admin
2. Click "Model Config"
3. Select Provider: Look for one of these options:

**Option A: Puter (BEST - Truly Unlimited FREE)**
- If "puter" provider exists, select it
- Paste your Puter API key
- Select model: (Puter will list available Claude models)
- Click "Validate" then "Apply"

**Option B: OpenRouter (FREE with free tier)**
- Go to https://openrouter.ai/keys
- Create free account, get free API key
- In FCC admin: Select "OpenRouter"
- Paste API key
- Select model: `openrouter/openrouter/free` (this tier is free)
- Click "Validate" then "Apply"

**Option C: NVIDIA NIM (FREE tier)**
- Go to https://build.nvidia.com/settings/api-keys
- Create free key
- In FCC admin: Select "NVIDIA NIM"
- Paste API key
- Select model: `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`
- Click "Validate" then "Apply"

**Keep fcc-server running in Terminal 1**

### Phase 4: Setup This App (5 minutes)

**Terminal 2:**

```bash
# Clone repo
git clone https://github.com/Mohammedalilgrh/putercfree.git
cd putercfree

# Install dependencies
npm install
```

**Create .env.local file:**
```env
# From Puter
VITE_PUTER_API_KEY=sk_your_puter_api_key_here

# Points to your local Free Claude Code proxy
VITE_FREE_CLAUDE_URL=http://localhost:8082
VITE_FREE_CLAUDE_TOKEN=freecc

# Optional settings
VITE_STORAGE_PATH=/Apps/TodoApp/
VITE_AUTO_SYNC_INTERVAL=30000
```

**Start dev server:**
```bash
npm run dev
```

Open http://localhost:5173 in your browser!

### Phase 5: Use the App

✅ **Now you have:**
- To-Do list with cloud sync (Puter, FREE)
- AI-powered features using Claude (FREE via Puter)
- No subscription costs
- No API usage fees
- Unlimited AI calls

## Verification Checklist

- [ ] Puter account created and API key obtained
- [ ] Free Claude Code installed (fcc-server works)
- [ ] FCC configured with Puter/OpenRouter/NVIDIA NIM
- [ ] App cloned and npm install complete
- [ ] .env.local created with your API key
- [ ] Both servers running (fcc-server and npm run dev)
- [ ] App loads at http://localhost:5173
- [ ] Can create todos
- [ ] AI Assistant buttons work (click "💡 Get Suggestions")
- [ ] Todos sync to Puter cloud

## How It All Works Together

```
Your Browser
    ↓
[To-Do App UI]
    ↓
When you click "✨ AI Assist":
    ↓
[App sends request to FCC]
    ↓
fcc-server (localhost:8082)
    ↓
[Routes to Puter's API using your key]
    ↓
Puter's Claude Models (Unlimited FREE)
    ↓
[Returns AI response to your app]
    ↓
You see suggestions/prioritization/categories
```

**Total Cost: $0**

## Common Issues & Solutions

### Issue: "Cannot connect to localhost:8082"
**Solution:** Make sure fcc-server is running in another terminal
```bash
fcc-server
```

### Issue: "Invalid Puter API key"
**Solution:** 
1. Check your key at https://puter.com/settings/api
2. Make sure it's in .env.local exactly
3. Restart: `npm run dev`

### Issue: "FCC says 'no provider configured'"
**Solution:**
1. Go to http://127.0.0.1:8082/admin
2. Click "Model Config"
3. Choose a provider (Puter, OpenRouter, or NVIDIA NIM)
4. Paste API key
5. Click "Validate" → "Apply"

### Issue: "AI features not working"
**Solution:**
1. Check fcc-server is running: `fcc-server --version`
2. Check provider in admin UI is set and validated
3. Open browser DevTools → Console (F12)
4. Look for error messages
5. Restart both servers

## Production Deployment

When ready to deploy (still FREE):

### Option 1: Vercel
```bash
git push origin main
# Connect GitHub repo to Vercel
# Add environment variables
# Deploy (automatic on push)
```

### Option 2: Netlify
```bash
# Same as Vercel - connect GitHub repo
# Build command: npm run build
# Publish directory: dist
```

### Option 3: Your Server/Docker
```bash
docker build -t putercfree .
docker run -p 3000:3000 \
  -e VITE_PUTER_API_KEY=your_key \
  putercfree
```

## Keep Both Servers Running

For the app to work:

**Terminal 1 (Keep running):**
```bash
fcc-server
```

**Terminal 2:**
```bash
npm run dev
```

Both need to run simultaneously.

## Next Steps

1. ✅ Complete setup above
2. Try the AI features
3. Customize the app for your needs
4. Deploy to production (still FREE)
5. Share with friends who want free AI!

## Get Help

- Puter Issues: https://github.com/HeyPuter/puter/issues
- Free Claude Code: https://github.com/Alishahryar1/free-claude-code
- This Repo: https://github.com/Mohammedalilgrh/putercfree/issues

**Remember: Everything here is FREE and always will be!**
