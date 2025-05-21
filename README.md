# JETTON SPIN Auto-Bot
A Python-based bot for automating spins in the JETTON SPIN mini-app, featuring a sleek, modern UI with a vibrant "JETTON SPIN" banner and "By Airdropdxns" branding. The bot interacts with the JETTON SPIN API to perform spins, check balances, and display account information in real-time.

# Register

https://t.me/jetton_lucky_spin_bot?start=1824331381

## Features

- Automated Spinning: Automatically performs spins for multiple accounts using threading.
- Eye-Catching UI/UX: Built with Tkinter, featuring a dark theme, vibrant coral banner (#FF6B6B), and cyan output text (#00FFAA) for a visually appealing experience.
- Real-Time Output: Displays account details, spin results, and balances in a scrollable text area.
- Start/Stop Controls: Intuitive buttons to start or stop the bot, with Ctrl+C support in the console.
- Multi-Account Support: Loads account query IDs from data.txt for batch processing.

## Prerequisites

- Python 3: Ensure Python 3 is installed (check with python --version or python3 --version).

## Dependencies:
- requests: For API communication.
- tkinter: For the GUI (usually included with Python; install separately on Linux if needed).
- A data.txt file with one query ID per line for account authentication.

## Installation

Clone the Repository:

```bash
git clone https://github.com/yourusername/jetton-spin-auto-bot.git
cd jetton-spin-auto-bot
```


## Install Dependencies:

```bash
pip install request
```

Install tkinter (if not included):

- Windows/macOS: tkinter is typically included with Python.
- Linux Debian/Ubuntu
``` bash
sudo apt-get install python3-tk
```
```bash
sudo dnf install python3-tkinter  # Red Hat/Fedora
```
Verify with:
python -c "import tkinter"

## Prepare data.txt:

- Create a file named data.txt in the project directory.
- Add one query ID per line (obtained from the JETTON SPIN app).

## Usage

Run the script:
```bash
python bot.py
```
or
```bash
python3 bot.py
```

## The GUI will launch, displaying:
- A "JETTON SPIN" banner with "By Airdropdxns" below it.
- A scrollable text area for real-time bot output.
- "Start Bot" and "Stop Bot" buttons.
- Click "Start Bot" to begin automated spinning for all accounts in data.txt.
- Click "Stop Bot" or press Ctrl+C in the console to stop the bot.

## File Structure

- main.py: The main script containing the bot logic and Tkinter GUI.
- data.txt: User-provided file for query IDs (not included in the repository).

## Notes

- Ensure data.txt exists and contains valid query IDs, or the bot will not run.
- The bot uses threading to handle multiple accounts concurrently, with a 5-second delay between spins.
- The UI features a dark theme (#1E1E2E) with a coral banner (#FF6B6B) and cyan text (#00FFAA) for readability.
- For issues with tkinter or API errors, check the console output in the GUI.

## Contributing
Feel free to submit issues or pull requests for improvements, such as additional features or UI enhancements.

## License
This project is licensed under the MIT License.

## Credits
Developed with ❤️ by Airdropdxns.
