# 🃏 MTG Match Tracker

A lightweight Python desktop application built with `tkinter` and `pandas` for logging *Magic: The Gathering* match results, importing completed games directly from **MTG Arena**, tracking deck win rates, turn counts, and mana-curve efficiency across formats, and identifying recurring opponent commanders.

## ✨ Features

* **⚡ One-Click MTG Arena Log Import (`arena_parser.py`):**
  * Parses MTG Arena's live `Player.log` JSON game events to pull your most recently completed match with one click (**Import Last Match**).
  * Automatically fills **Deck Name**, **Format**, **Match Result** (`Win`/`Loss`), and **Turn Counter**, while safely skipping Sparky bot matches (`AIBotMatch`) and warning if an Arena update introduces an unrecognized queue ID.
  * Prompts once for your MTG Arena Display Name on first import and saves it locally to `config.json` so no code edits are required.
* **Fast, Format-Aware Match Logging:** Log your deck, format, opponent commander, match outcome (`Win`/`Loss`), ending land count, and turn counter through a clean desktop GUI. Automatically hides the opponent selector and logs `"N/A"` when playing non-commander formats (`Standard`, `Modern`, `Alchemy`, `Pauper`, `Legacy`, `Historic`, `Explorer`, `Timeless`).
* **Dynamic Dropdowns:** Automatically loads previously played decks and opponent commanders from your local CSV ledger (filtering out `"N/A"` entries), with built-in pop-up windows to add new entries on the fly—plus auto-registration when importing a brand-new Arena deck.
* **Live Status Banner:** Color-coded in-app feedback for missing fields, new entries, and logged matches.
* **Format-Filtered Season Analytics Pop-Up:** Opens a scrollable report with a **Filter Format** dropdown (`All Formats` or individual formats), breaking down win rates, average ending lands, average game length (turns), and **Mana Curve Efficiency** (`+/-` lands vs. turn curve and percentage ratio) at the **Overall**, **Per-Format**, and **Per-Deck** levels—alongside separate **Top Nemesis** and **Most Faced Commanders** lists for Commander/Brawl formats (`Commander`, `Standard Brawl`, `Brawl`).
* **Season Reset (`Purge`):** Wipe your ledger with a confirmation prompt to start a fresh season and reset dropdowns back to defaults.
* **Local CSV Persistence:** Saves all match data automatically to `mtg_match_ledger.csv` (stored in `%LOCALAPPDATA%\MTG_Match_Tracker` when running the standalone `.exe`/installer, or in the application folder when running from source).

* **Side Note:** Developer is a fan of the Ravnica Guilds you may find the various automated messages to ALSO be fans of the Ravnica Guilds.

## 🛠️ Project Structure

```text
MTG-Match-Tracker/
├── tracker.py              # Main Tkinter GUI, config setup, CSV persistence, and analytics engine
├── arena_parser.py         # MTG Arena Player.log parser & queue-to-format mapper
├── installer.iss           # Inno Setup script for building the Windows installer
├── mtg_match_ledger.csv    # Auto-generated persistent match database
├── config.json             # Auto-generated local config storing your MTG Arena display name
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Option 1: Windows Installer / Standalone `.exe` (No Python Required)
1. Download **`MTG_Tracker_Setup_v1.0.0.exe`** (full installer) or **`MTG_Tracker.exe`** (portable) from the [**Releases**](https://github.com) page.
2. Launch **MTG Match Tracker** and click **Import Last Match** after finishing an Arena game to enter your MTG Arena Display Name (without the `#12345` tag).

### Option 2: Run From Source (Python 3.10+)
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd mtg-match-tracker
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
| `turns` | Final turn counter at the end of the match |

---

*MTG Match Tracker is unofficial Fan Content permitted under the Fan Content Policy. Not approved/endorsed by Wizards. Portions of the materials used are property of Wizards of the Coast. ©Wizards of the Coast LLC.*
