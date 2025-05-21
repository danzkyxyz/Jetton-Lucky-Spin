import requests
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, ttk
import sys
from io import StringIO

class MiniAppAutoSpinBot:
    def __init__(self):
        self.accounts = []
        self.load_accounts()
        self.running = False
        self.threads = []
        # Initialize UI
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("JETTON SPIN Auto-Bot")
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1E2E")  # Dark theme background

        # Styling
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background="#FF6B6B", foreground="#FFFFFF")
        style.configure("TLabel", font=("Helvetica", 14), background="#1E1E2E", foreground="#E0E0E0")

        # Banner
        banner_frame = tk.Frame(self.root, bg="#FF6B6B")
        banner_frame.pack(fill="x", pady=10)
        banner_label = tk.Label(banner_frame, text="JETTON SPIN AUTO BOT", font=("Helvetica", 24, "bold"), fg="#FFFFFF", bg="#FF6B6B")
        banner_label.pack(pady=5)
        sub_banner_label = tk.Label(banner_frame, text="By Airdropdxns", font=("Helvetica", 12, "italic"), fg="#E0E0E0", bg="#FF6B6B")
        sub_banner_label.pack()

        # Output area
        self.output_text = scrolledtext.ScrolledText(self.root, height=20, bg="#2E2E3E", fg="#00FFAA", font=("Courier", 12), wrap=tk.WORD)
        self.output_text.pack(padx=20, pady=10, fill="both", expand=True)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#1E1E2E")
        button_frame.pack(pady=10)
        start_button = ttk.Button(button_frame, text="Start Bot", command=self.start)
        start_button.pack(side="left", padx=5)
        stop_button = ttk.Button(button_frame, text="Stop Bot", command=self.stop)
        stop_button.pack(side="left", padx=5)

        # Redirect console output to text area
        sys.stdout = TextRedirector(self.output_text)

    def load_accounts(self):
        try:
            with open('data.txt', 'r') as file:
                self.accounts = [line.strip() for line in file.readlines() if line.strip()]
            print(f"Loaded {len(self.accounts)} accounts from data.txt")
        except FileNotFoundError:
            print("data.txt not found. Please create it with one query_id per line.")
            self.accounts = []

    def get_headers(self, query_id):
        return {
            'authority': 'api.jtmkbot.click',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://v2.jtmkbot.click',
            'priority': 'u=1, i',
            'referer': 'https://v2.jtmkbot.click/',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'secure-header': query_id,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }

    def get_account_info(self, query_id):
        url = "https://api.jtmkbot.click/client/info"
        headers = self.get_headers(query_id)
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    'username': data.get('userName', 'N/A'),
                    'first_name': data.get('firstName', 'N/A'),
                    'spin_level': data.get('spinLevel', 'N/A')
                }
        except Exception as e:
            print(f"Error getting account info: {e}")
        
        return None

    def get_balance(self, query_id):
        url = "https://api.jtmkbot.click/wallet/balance"
        headers = self.get_headers(query_id)
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('balance', 0)
        except Exception as e:
            print(f"Error getting balance: {e}")
        
        return 0

    def get_available_spins(self, query_id):
        url = "https://api.jtmkbot.click/roulette/spin/available"
        headers = self.get_headers(query_id)
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('available', 0)
        except Exception as e:
            print(f"Error getting available spins: {e}")
        
        return 0

    def perform_spin(self, query_id):
        url = "https://api.jtmkbot.click/roulette/spin"
        headers = self.get_headers(query_id)
        
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for line in ['firstLine', 'secondLine', 'thirdLine']:
                    if data.get(line, {}).get('prize'):
                        prize = data[line]['prize']
                        if 'tickets' in prize:
                            return f"Won {prize['tickets']} tickets!"
                        elif 'coins' in prize:
                            return f"Won {prize['coins']} coins!"
                return "Spin completed (no win)"
        except Exception as e:
            print(f"Error performing spin: {e}")
        
        return "Spin failed"

    def account_worker(self, query_id, account_idx):
        account_info = self.get_account_info(query_id)
        if not account_info:
            print(f"Account {account_idx}: Failed to get account info")
            return
            
        username = account_info['username']
        first_name = account_info['first_name']
        spin_level = account_info['spin_level']
        
        print(f"\nAccount {account_idx}: {first_name} (@{username}) - {spin_level} level")
        
        while self.running:
            try:
                balance = self.get_balance(query_id)
                available_spins = self.get_available_spins(query_id)
                
                if available_spins > 0:
                    spin_result = self.perform_spin(query_id)
                    new_available = self.get_available_spins(query_id)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Account {account_idx}: Balance: {balance} | {spin_result} | Remaining spins: {new_available}")
                else:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Account {account_idx}: No spins available (Balance: {balance})")
                
                time.sleep(5)
                
            except Exception as e:
                print(f"Account {account_idx}: Error in worker: {e}")
                time.sleep(10)

    def start(self):
        if not self.accounts:
            print("No accounts loaded. Please add query_ids to data.txt")
            return
            
        self.running = True
        print("Starting auto-spin bot...")
        
        for idx, query_id in enumerate(self.accounts, 1):
            thread = threading.Thread(target=self.account_worker, args=(query_id, idx))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
            time.sleep(1)
        
        print(f"Started {len(self.accounts)} account workers. Press Ctrl+C in console or use Stop button.")

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        print("Auto-spin bot stopped.")

    def run(self):
        try:
            self.start()
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop()

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.update()

    def flush(self):
        pass

if __name__ == "__main__":
    bot = MiniAppAutoSpinBot()
    bot.run()