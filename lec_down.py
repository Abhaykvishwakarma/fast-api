from telethon import TelegramClient
import asyncio
import os

# --- Configuration ---
API_ID = '35571113'  
API_HASH = 'c0e44e3d6799cb8a044430eb5682b968'  # Replace with your API Hash
DOWNLOAD_PATH = '/sdcard/Download/'

def progress_callback(current, total):
    """Calculates and prints the download progress percentage."""
    percentage = (current / total) * 100
    # Displays progress in the format: [##########] 50.0%
    bar_length = 20
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r|{bar}| {percentage:.1f}% Done', end='', flush=True)

async def main():
    print("="*40)
    print("      TELEGRAM PRIVATE DOWNLOADER      ")
    print("="*40)
    
    async with TelegramClient('session', API_ID, API_HASH) as client:
        link = input("\n[?] Enter Private Video Link: ").strip()
        
        try:
            # Parsing link to get Chat ID and Message ID
            parts = link.rstrip('/').split('/')
            msg_id = int(parts[-1])
            
            if len(parts) >= 3 and parts[-3] == 'c':
                # Normal link: t.me/c/CHAT_ID/MSG_ID
                chat_id = int("-100" + parts[-2])
            else:
                # Forum/topic link: t.me/c/CHAT_ID/TOPIC_ID/MSG_ID
                chat_id = int("-100" + parts[-3])
            
            print(f"\n[*] Fetching message {msg_id} from chat {chat_id}...")
            message = await client.get_messages(chat_id, ids=msg_id)
            
            if message and message.media:
                print("[+] Media found! Starting download...")
                
                # Downloading with a progress callback
                path = await client.download_media(
                    message, 
                    file=DOWNLOAD_PATH,
                    progress_callback=progress_callback
                )
                
                print(f"\n\n{'='*40}")
                print(f"🔥 SUCCESS: File saved to {path}")
                print(f"{'='*40}\n")
            else:
                print("\n[!] Error: No media found at this link.")
             
        except IndexError:
            print("\n[!] Error: Invalid link format. Please use the full post link.")
        except ValueError:
            print("\n[!] Error: Could not parse Chat ID/Message ID from the link.")
        except Exception as e:
            print(f"\n[!] An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Ensure storage is ready
    if not os.path.exists(DOWNLOAD_PATH):
        print(f"[*] Creating directory: {DOWNLOAD_PATH}")
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[!] Download cancelled by user.")