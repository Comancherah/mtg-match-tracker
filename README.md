# 🃏 MTG Match Tracker

A lightweight Python desktop application built with `tkinter` and `pandas` for logging *Magic: The Gathering* match results, tracking deck win rates and land curves across formats, and identifying recurring opponent commanders.

## ✨ Features

* **Fast, Format-Aware Match Logging:** Log your deck, format, opponent commander, match outcome (`Win`/`Loss`), and ending land count through a clean desktop GUI. Automatically hides the opponent selector and logs `"N/A"` when playing non-commander formats (`Standard`, `Modern`, `Alchemy`, `Pauper`, `Legacy`, `Historic`, `Timeless`).
* **Dynamic Dropdowns:** Automatically loads previously played decks and opponent commanders from your local CSV ledger (filtering out `"N/A"` entries), with built-in pop-up windows to add new entries on the fly.
* **Live Status Banner:** Color-coded in-app feedback for missing fields, new entries, and logged matches.
* **Format-Filtered Season Analytics Pop-Up:** Opens a scrollable report with a **Filter Format** dropdown (`All Formats` or individual formats), breaking down win rates, average ending lands per format/deck, and separate **Top Nemesis** and **Most Faced Commanders** lists for each Commander/Brawl format (`Commander`, `Standard Brawl`, `Brawl`).
* **Season Reset (`Purge`):** Wipe your ledger with a confirmation prompt to start a fresh season and reset dropdowns back to defaults.
* **Local CSV Persistence:** Saves all match data automatically to `mtg_match_ledger.csv` in the application directory.

* **Side Note:** Developer is a fan of the Ravnica Guilds you may find the various automated messages to ALSO be fans of the Ravnica Guilds.

## 🛠️ Requirements

* Python 3.10+
* `pandas` (`tkinter` is included with standard Python installations on Windows/macOS)

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd YOUR-REPO-NAME
   ```

2. **Install dependencies:**
   ```bash
   pip install pandas
   ```

3. **Run the tracker:**
   ```bash
   python tracker.py
   ```

## 📊 CSV Data Structure

The app automatically generates `mtg_match_ledger.csv` on first launch with the following columns:

| Column | Description |
| :--- | :--- |
| `date` | Match date (`YYYY-MM-DD`) |
| `deck_name` | Name of the deck piloted |
| `format` | Format played (`Brawl`, `Standard Brawl`, `Commander`, `Standard`, etc.) |
| `opponent_commander` | Opposing commander (`"N/A"` for non-commander formats) |
| `result` | `Win` or `Loss` |
| `mana_total` | Total lands in play at the end of the game |
