import webbrowser
import time
import sys

PASSWORD = "kamineelovesraj"
WEBSITE_FILE = "index.html"

print("🔒 This webpage is protected")
print("🖤 Black Screen Protection Enabled\n")

user_input = input("Enter Password: ")

if user_input == PASSWORD:
    print("\n✅ Access Granted!")
    print("✨ Opening your webpage...")
    time.sleep(1)
    webbrowser.open(WEBSITE_FILE)
else:
    print("\n❌ Wrong Password!")
    print("🚫 Access Denied")
    print("🌐 Redirecting to GitHub...")
    time.sleep(2)
    webbrowser.open("https://github.com")
    sys.exit()
