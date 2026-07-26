# setup_deepseek.py
import subprocess
import sys
import os

def setup_bot():
    """Setup the Study Bot with DeepSeek API"""
    
    print("=" * 50)
    print("🔧 STUDY BOT SETUP | إعداد بوت الدراسة")
    print("=" * 50)
    
    # Install required packages
    print("\n📦 Installing Python packages...")
    packages = [
        "python-telegram-bot==20.7",
        "requests",
        "pytesseract",
        "Pillow",
        "PyPDF2",
        "python-docx"
    ]
    
    for package in packages:
        try:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except:
            print(f"  ⚠️ Failed to install {package}")
    
    print("\n✅ Python packages installed!")
    
    # Check for Tesseract OCR
    print("\n🔍 Checking for Tesseract OCR...")
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR is installed!")
    except:
        print("❌ Tesseract OCR not found!")
        print("\n📥 Please install Tesseract OCR:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Mac: brew install tesseract")
        print("  Ubuntu: sudo apt-get install tesseract-ocr")
        print("  Also install Arabic language data:")
        print("  sudo apt-get install tesseract-ocr-ara")
    
    # DeepSeek API Key
    print("\n🔑 DEEPSEEK API SETUP:")
    print("1. Go to https://platform.deepseek.com/")
    print("2. Sign up or log in")
    print("3. Go to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the API key")
    print("\n6. Open the bot file and replace:")
    print('   DEEPSEEK_API_KEY = "your-deepseek-api-key-here"')
    print("   with your actual API key")
    
    # Create requirements file
    with open('requirements_deepseek.txt', 'w') as f:
        f.write("python-telegram-bot==20.7\n")
        f.write("requests>=2.28.0\n")
        f.write("pytesseract>=0.3.10\n")
        f.write("Pillow>=10.0.0\n")
        f.write("PyPDF2>=3.0.0\n")
        f.write("python-docx>=1.0.0\n")
    
    print("\n📁 Created requirements_deepseek.txt")
    
    # Bot token check
    print("\n🤖 BOT TOKEN:")
    print("Your bot token is already configured:")
    print("7954243581:AAFB_eQHGwCLRYTGeBwJ3gZWa1qtMDT76Bs")
    
    print("\n" + "=" * 50)
    print("✅ SETUP COMPLETE!")
    print("=" * 50)
    print("\n🚀 To start the bot:")
    print("1. Make sure you've added your DeepSeek API key")
    print("2. Run: python study_bot_deepseek.py")
    print("3. Open Telegram and send /start to your bot")
    print("\n📱 Bot will be available at: t.me/your_bot_username")
    print("\nGood luck with your studies! 📚")
    print("بالتوفيق في دراستك! 📚")

if __name__ == "__main__":
    setup_bot()
