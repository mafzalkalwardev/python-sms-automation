import pandas as pd
import pyautogui
import time
from datetime import datetime

# ===== CONFIGURATION ===== #
EXCEL_PATH = "phones.xlsx"  # Your Excel file
MESSAGE = """Hello {name}! I'm Tom Harrison, a dispatcher at Echo Vista LLC. 
We partner with Premium Brokers to bring you high-paying freight loads and 
outstanding per mile rates. Reply with MC# & Zip Code."""
INITIAL_DELAY = 5  
TYPE_DELAY = 0.1   
COOLDOWN = 2  # Added safety cooldown between messages

pyautogui.FAILSAFE = True  

def prepare_dialer():
    print(f"Prepare your SMS app! Starting in {INITIAL_DELAY} seconds...")
    time.sleep(INITIAL_DELAY)
    # Focus on the SMS app window
    pyautogui.click()  

def send_sms(number, message):
    try:
        # Format number with country code
        formatted_number = f"+1{number}" if len(number) == 10 else number
        
        # Clear previous inputs
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        
        # Enter phone number
        pyautogui.write(formatted_number, interval=TYPE_DELAY)
        time.sleep(0.5)
        
        # Navigate to message field (may need adjustment for your SMS app)
        pyautogui.press('tab', presses=3, interval=0.3)  # Adjust tab count as needed
        time.sleep(0.2)
        
        # Type message with proper newline handling
        for line in message.split('\n'):
            pyautogui.write(line, interval=TYPE_DELAY)
            pyautogui.hotkey('shift', 'enter')  # Use proper newline for your app
        time.sleep(0.5)
        
        # Send message
        pyautogui.press('enter')
        time.sleep(1)
        
        # Reset for next message
        pyautogui.press('esc', presses=2, interval=0.5)
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Load and validate contacts
try:
    df = pd.read_excel(EXCEL_PATH)
    print(f"Loaded {len(df)} contacts at {datetime.now().strftime('%H:%M:%S')}")
    
    # Clean phone numbers
    df['Phone'] = df['Phone'].astype(str).str.replace(r'\D+', '', regex=True)
    
except Exception as e:
    print(f"File error: {str(e)}")
    exit()

# Start sending
prepare_dialer()
success_count = 0

for index, row in df.iterrows():
    phone = row['Phone']
    name = row['Name']
    
    if len(phone) != 10 or not phone.isdigit():
        print(f"⚠️ Invalid: {phone} for {name}")
        continue
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sending to {name} ({phone})...")
    
    if send_sms(phone, MESSAGE.format(name=name)):
        success_count += 1
        print("Success!")
        time.sleep(COOLDOWN)
    else:
        print(f"Failed {phone}")

    # Progress update
    print(f"Progress: {index+1}/{len(df)}")

print(f"\nFinal report: {success_count} successful / {len(df)} total")
pyautogui.moveTo(100, 100)  # Move mouse to safe corner