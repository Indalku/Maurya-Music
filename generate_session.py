from pyrogram import Client

print("=== Maurya Music Assistant String Session Generator ===")
api_id = int(input("Apna API_ID dalein: "))
api_hash = input("Apna API_HASH dalein: ")

with Client("session_gen", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
    session_str = app.export_session_string()
    print("\n✅ Aapka STRING_SESSION niche hai (ise safe rakhein aur kisi ko na bhejein):\n")
    print(session_str)
