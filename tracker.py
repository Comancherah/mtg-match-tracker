import pandas as pd
import tkinter as tk
from tkinter import ttk # 'ttk' is where im getting my drop down menu functionality from
from tkinter import messagebox
from datetime import datetime
import os

# Define our persistent data files
DB_FILE = 'mtg_match_ledger.csv'
columns = ['date', 'deck_name', 'format', 'opponent_commander', 'result', 'mana_total']

# 1. LOAD DATA: Connect to our permanent csv storage framework
if os.path.exists(DB_FILE):
    print(f"--> File found! Loading database file: '{DB_FILE}'")
    match_history = pd.read_csv(DB_FILE)
else:
    print("--> No existing file detected. Initializing a clean match ledger spreadsheet...")
    match_history = pd.DataFrame(columns=columns)

# 2. Collect the data from the user via a simple GUI
root = tk.Tk()
root.title("MTG Match Tracker")
root.geometry("400x500") # basic layout for the GUI window

# now that weve built the basics, need data
default_deck_list = ['How Illogical', 'Tremors', 'Answers']  # Example deck names
default_opponent_list = ['Pantlaza', 'Svella', 'Belladonna']  # Example opponent names

# dont forget what we saved from before, if we have any
if not match_history.empty:
    saved_decks = match_history['deck_name'].unique().tolist()
    # Merge the saved decks with the default list, ensuring no duplicates
    combined_deck_list = sorted(set(default_deck_list + saved_decks), key=str.lower)

    saved_opponents = [
        opp for opp in match_history['opponent_commander'].dropna().unique().tolist()
        if str(opp).strip().upper() != "N/A"
    ]

    combined_opponent_list = sorted(set(default_opponent_list + saved_opponents), key=str.lower)

else:
    combined_deck_list = sorted(default_deck_list, key=str.lower)
    combined_opponent_list = sorted(default_opponent_list, key=str.lower)

NON_COMMANDER_FORMATS = ("Standard", "Alchemy", "Pauper", "Legacy", "Historic", "Timeless", "Modern")

# most important part
deck_list = combined_deck_list + ["[ Add New Deck... ]"]  # Ensure the "Add New Deck..." option is always present
opponent_list = combined_opponent_list + ["[Add New Opponent...]"]  # Ensure the "Add New Opponent..." option is always present

Formats = ['Brawl', 'Standard Brawl', 'Commander', 'Standard', 'Modern', 'Pauper', 'Legacy', 'Timeless', 'Alchemy']
result_options = ['Win', 'Loss']
mana_options = list(range(0, 50))  # Assuming a max of 50 lands on the field should never be this high.... but yea

# Stats, anyone? Also all Def functions
def calculate_stats():
    # Open a dedicated pop-up window
    stats_window = tk.Toplevel(root)
    stats_window.title("Season Match Analytics")
    stats_window.geometry("500x580")
    stats_window.grab_set()

    # Header banner inside the pop-up
    header_lbl = tk.Label(
        stats_window,
        text="MTG Season Analytics Report",
        font=("arial", 13, "bold"),
        fg="#1a237e"
    )
    header_lbl.pack(pady=(12, 6))

    # --- FORMAT FILTER DROPDOWN BAR ---
    filter_frame = tk.Frame(stats_window)
    filter_frame.pack(pady=(0, 6))

    tk.Label(filter_frame, text="Filter Format:", font=("arial", 10, "bold")).pack(side="left", padx=(0, 6))

    if match_history.empty:
        available_formats = ["All Formats"]
    else:
        available_formats = ["All Formats"] + sorted(match_history['format'].dropna().unique().tolist())

    filter_dropdown = ttk.Combobox(filter_frame, values=available_formats, state="readonly", width=22)
    filter_dropdown.set("All Formats")
    filter_dropdown.pack(side="left")

    # Scrollable text area for clean, aligned stats
    text_frame = tk.Frame(stats_window)
    text_frame.pack(fill="both", expand=True, padx=12, pady=6)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    report_box = tk.Text(
        text_frame,
        wrap="word",
        font=("Consolas", 10),
        yscrollcommand=scrollbar.set,
        bg="#f8f9fa",
        padx=10,
        pady=10
    )
    report_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=report_box.yview)

    # Helper function to build & refresh the report whenever the dropdown changes
    def update_report(event=None):
        selected_filter = filter_dropdown.get()

        if match_history.empty:
            report = "No matches logged yet for this season.\n\nGo play some games and log them first!"
        else:
            if selected_filter == "All Formats":
                filtered_df = match_history
            else:
                filtered_df = match_history[match_history['format'] == selected_filter]

            if filtered_df.empty:
                report = f"No matches logged for {selected_filter} yet."
            else:
                total_games = len(filtered_df)
                total_wins = len(filtered_df[filtered_df['result'] == 'Win'])
                overall_wr = (total_wins / total_games) * 100
                avg_lands = filtered_df['mana_total'].mean()

                lines = []
                lines.append("=" * 46)
                lines.append(f"{selected_filter.upper()} SUMMARY")
                lines.append(f"RECORD: {total_wins}W - {total_games - total_wins}L ({overall_wr:.1f}%)")
                lines.append(f"AVG ENDING LANDS: {avg_lands:.1f}")
                lines.append("=" * 46)

                # --- PER-FORMAT DECK & COMMANDER BREAKDOWN ---
                for fmt, fmt_group in filtered_df.groupby('format'):
                    f_games = len(fmt_group)
                    f_wins = len(fmt_group[fmt_group['result'] == 'Win'])
                    f_wr = (f_wins / f_games) * 100
                    f_lands = fmt_group['mana_total'].mean()

                    lines.append(f"\n=== {fmt.upper()} ({f_games} Games) ===")
                    lines.append(f"Record: {f_wins}W-{f_games - f_wins}L ({f_wr:.1f}%) | Avg Lands: {f_lands:.1f}")
                    lines.append("-" * 46)

                    # Deck win rates inside this specific format
                    for deck, deck_group in fmt_group.groupby('deck_name'):
                        d_games = len(deck_group)
                        d_wins = len(deck_group[deck_group['result'] == 'Win'])
                        d_wr = (d_wins / d_games) * 100
                        d_lands = deck_group['mana_total'].mean()
                        lines.append(f"• {deck}: {d_wins}W-{d_games - d_wins}L ({d_wr:.1f}%) | Lands: {d_lands:.1f}")

                    # Separate Commander / Brawl opponent breakdown per format
                    if fmt not in NON_COMMANDER_FORMATS:
                        valid_opps = fmt_group[
                            fmt_group['opponent_commander'].notna() &
                            (fmt_group['opponent_commander'].astype(str).str.strip().str.upper() != "N/A")
                        ]

                        if not valid_opps.empty:
                            lines.append(f"\n  [{fmt} Top Nemeses]")
                            losses = valid_opps[valid_opps['result'] == 'Loss']
                            if losses.empty:
                                lines.append("  • Undefeated in this format! Zero losses.")
                            else:
                                for opp, count in losses['opponent_commander'].value_counts().head(5).items():
                                    lines.append(f"  • {opp}: {count} loss(es)")

                            lines.append(f"\n  [{fmt} Most Faced Commanders]")
                            for opp, count in valid_opps['opponent_commander'].value_counts().head(5).items():
                                lines.append(f"  • {opp}: {count} game(s)")

                report = "\n".join(lines)

        # Unlock box, swap text, and lock back to read-only
        report_box.config(state="normal")
        report_box.delete("1.0", tk.END)
        report_box.insert("1.0", report)
        report_box.config(state="disabled")

    # Bind dropdown selection and load initial "All Formats" view
    filter_dropdown.bind("<<ComboboxSelected>>", update_report)
    update_report()

    # Close button at the bottom
    close_btn = tk.Button(
        stats_window,
        text="Close Report",
        command=stats_window.destroy,
        bg="#333333",
        fg="white",
        font=("arial", 10, "bold")
    )
    close_btn.pack(pady=(6, 12))



# Certain formats dont have commanders, so remove the commander
def on_format_change(event=None):
    selected_format = format_dropdown.get()
    
    if selected_format in NON_COMMANDER_FORMATS:
        opponent_lbl.grid_remove()
        opponent_dropdown.grid_remove()
        opponent_dropdown.set("N/A")
    else:
        opponent_lbl.grid()
        opponent_dropdown.grid()
        if opponent_dropdown.get() == "N/A":
            opponent_dropdown.set("")

# Data purge (careful!!!)
def purge_data():
    #trigger a native Yes/No warning dialog box to confirm the purge action
    confirm = messagebox.askyesno(
        title="⚠️ SEASON RESET WARNING",
        message="Are you sure you want to purge all match history?\n\n This action cannot be undone."
    )
    #if the user says no... RUN AWAY, RUN AWAY!
    if not confirm:
        status_lbl.config(
            text="Purge aborted. Your Orzhov ledger remains intact.",
            fg="#b30000",
            font=("arial", 10, "bold")
        )
        return
    #if the user says yes, then we proceed with the purge
    global match_history
    match_history = pd.DataFrame(columns=columns)  # Reset the DataFrame

    #overwrite the pgysical csv file to confirm data purge
    match_history.to_csv(DB_FILE, index=False)

    #reset time
    deck_list = default_deck_list + ["[ Add New Deck... ]"]
    opponent_list = default_opponent_list + ["[Add New Opponent...]"]

    #push this out to the GUI dropdowns
    deck_dropdown['values'] = deck_list
    opponent_dropdown['values'] = opponent_list

    #And last but not least Clear the GUI dropdowns to reflect the purge
    deck_dropdown.set('')
    format_dropdown.set('')
    opponent_dropdown.set('')
    result_dropdown.set('')
    mana_dropdown.set('')

    status_lbl.config(
        text="All match history has been purged. Your Orzhov ledger is now clean.   Eww, I hate that word. I feel dirty just saying it.",
        fg="#b30000",
        font=("arial", 10, "bold")
    )
    calculate_stats()  # Recalculate stats after purge to verify that the ledger is empty

# 2.2 GUI: Create the submit button to log the match
def submit_match():
    selected_deck = deck_dropdown.get()
    selected_format = format_dropdown.get()
    enemy_commander = opponent_dropdown.get().strip() # normalize the opponent name by stripping whitespace (read NO SPACES)
    selected_result = result_dropdown.get()
    selected_mana_total = mana_dropdown.get()

    # Validate that all fields are filled

    if not all([selected_deck, selected_format, enemy_commander, selected_result, selected_mana_total]):
        messagebox.showerror("Incomplete Information", "Please fill in all fields.")
        return

    # OK building some backend stuff for later (pop up window)

# ==========================================
# ZONE 3: FUNCTION DEFINITIONS
# ==========================================
def deck_change(event=None):
    if deck_dropdown.get() == "[ Add New Deck... ]":
        deck_dropdown.set("")
        open_new_deck_window()

def opponent_change(event=None):
    if opponent_dropdown.get() == "[Add New Opponent...]":
        opponent_dropdown.set("")
        open_new_opponent_window()    

def open_new_deck_window():
    new_deck_window = tk.Toplevel(root)
    new_deck_window.title("Add New Deck")
    new_deck_window.geometry("300x150")
    new_deck_window.grab_set()

    popup_deck_lbl = ttk.Label(new_deck_window, text="Enter New Deck Name:")
    popup_deck_lbl.pack(pady=10)

    new_deck_entry = ttk.Entry(new_deck_window, width=30)
    new_deck_entry.pack(pady=10)
    new_deck_entry.focus_set()

    def save_new_deck():
        new_deck_name = new_deck_entry.get().strip()
        if new_deck_name and new_deck_name not in deck_list:
            deck_list.insert(-1, new_deck_name)
            deck_list[:-1] = sorted(deck_list[:-1], key=str.lower)
            deck_dropdown['values'] = deck_list
            deck_dropdown.set(new_deck_name)
            status_lbl.config(
                text=f"New Deck  '{new_deck_name}' added! Ready to log results.",
                fg="#2e7d32",
                font=("arial", 9, "bold")
            )
            new_deck_window.destroy()
        else:
            status_lbl.config(
                text="All forms in triplicate, yours are not. Fix.",
                fg="#b30000",
                font=("arial", 9, "bold")
            )
            new_deck_window.destroy()

    save_deck_btn = ttk.Button(new_deck_window, text="Save Deck", command=save_new_deck)
    save_deck_btn.pack(pady=10)


def open_new_opponent_window():
    new_opponent_window = tk.Toplevel(root)
    new_opponent_window.title("Add New Opponent...")
    new_opponent_window.geometry("300x150")
    new_opponent_window.grab_set()

    popup_opponent_lbl = ttk.Label(new_opponent_window, text="Enter New Opponent Name:")
    popup_opponent_lbl.pack(pady=10)

    new_opponent_entry = ttk.Entry(new_opponent_window, width=30)
    new_opponent_entry.pack(pady=10)
    new_opponent_entry.focus_set()

    def save_new_opponent():
        new_opponent_name = new_opponent_entry.get().strip()
        existing_lower = [opp.lower() for opp in opponent_list[:-1]]

        if not new_opponent_name:
            status_lbl.config(
                text="Azorius lawyers demand to know who we are suing! ",
                fg="#b30000",
                font=("arial", 9, "bold")
            )
        elif new_opponent_name.lower() in existing_lower:
            match_index = existing_lower.index(new_opponent_name.lower())
            opponent_dropdown.set(opponent_list[match_index])
            status_lbl.config(
                text=f"'{opponent_list[match_index]}' is already on the docket—selected it for you!",
                fg="#b30000",
                font=("arial", 9, "bold")
            )
        else:
            opponent_list.insert(-1, new_opponent_name)
            opponent_list[:-1] = sorted(opponent_list[:-1], key=str.lower)
            opponent_dropdown['values'] = opponent_list
            opponent_dropdown.set(new_opponent_name)
            status_lbl.config(
                text=f"New Opponent '{new_opponent_name}' added! Ready to log match.",
                fg="#2e7d32",
                font=("arial", 9, "bold")
            )

        new_opponent_window.destroy()


    save_opponent_btn = ttk.Button(new_opponent_window, text="Save Opponent", command=save_new_opponent)
    save_opponent_btn.pack(pady=10)


def submit_match():
    selected_deck = deck_dropdown.get()
    selected_format = format_dropdown.get()
    enemy_commander = opponent_dropdown.get().strip()
    selected_result = result_dropdown.get()
    selected_mana_total = mana_dropdown.get()

    # Check for "Add New..." triggers BEFORE checking if all fields are filled
    if selected_deck == "[ Add New Deck... ]":
        status_lbl.config(
            text="Azorius lawyers despise incomplete forms. Please state your business(deck).",
            fg="#b30000",
            font=("arial", 9, "bold") 
        )
        open_new_deck_window()
        return

    if enemy_commander == "[Add New Opponent...]":
        status_lbl.config(
            text="Azorius lawyers despise incomplete forms. Please state who to file your injunction against: ",
            fg="#b30000",
            font=("arial", 9, "italic")
        )
        open_new_opponent_window()
        return

    # Validate that all fields are filled
    if not all([selected_deck, selected_format, enemy_commander, selected_result, selected_mana_total]):
        messagebox.showerror("Incomplete Information", "Please fill in all fields.")
        return

    global match_history
    new_game = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'deck_name': selected_deck,
        'format': selected_format,
        'opponent_commander': enemy_commander,
        'result': selected_result,
        'mana_total': int(selected_mana_total)
    }

    # Check for add New triggers First
    if selected_deck == "[ Add New Deck... ]":
        status_lbl.config(text="Azorius lawyers despise incomplete forms. Please state New Deck Name: ")
        open_new_deck_window()
        return

    if enemy_commander == "[Add New Opponent...]":
        status_lbl.config(text="Azorius lawyers demand to know who we are suing! ")
        open_new_opponent_window()
        return

    #validate again that all fields are filled
    if not all([selected_deck, selected_format, enemy_commander, selected_result, selected_mana_total]):
        messagebox.showerror("Incomplete Information for the Syndicate", "Please fill in all fields. The Azorius Guild is watching.")
        return

    match_history = pd.concat([match_history, pd.DataFrame([new_game])], ignore_index=True)
    match_history.to_csv(DB_FILE, index=False)
    status_lbl.config(
        text=f"Business Recorded for 'protection' of {selected_deck} vs {enemy_commander} - Result: {selected_result}, Lands: {selected_mana_total}",
        fg="#2e7d32",
        font=("arial", 9, "bold")
    )

    # Clear match specific entries
    mana_dropdown.set('')
    result_dropdown.set('')
    

# 2.1 GUI: Create the dropdowns for user input
deck_lbl = ttk.Label(root, text="Select Deck:")
deck_lbl.grid(row=0, column=0, padx=10, pady=5, sticky='w')
deck_dropdown = ttk.Combobox(root, values=deck_list, state="readonly")
deck_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky='w')

format_lbl = ttk.Label(root, text="Select Format:")
format_lbl.grid(row=1, column=0, padx=10, pady=5, sticky='w')
format_dropdown = ttk.Combobox(root, values=Formats, state="readonly")
format_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky='w')

opponent_lbl = ttk.Label(root, text="Select Opponent:")
opponent_lbl.grid(row=2, column=0, padx=10, pady=5, sticky='w')
opponent_dropdown = ttk.Combobox(root, values=opponent_list, state="readonly")
opponent_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky='w')

result_lbl = ttk.Label(root, text="Match Result:")
result_lbl.grid(row=3, column=0, padx=10, pady=5, sticky='w')
result_dropdown = ttk.Combobox(root, values=result_options, state="readonly")
result_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky='w')

mana_lbl = ttk.Label(root, text="Total Lands At End:")
mana_lbl.grid(row=4, column=0, padx=10, pady=5, sticky='w')
mana_dropdown = ttk.Combobox(root, values=mana_options, state="readonly")
mana_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky='w')

# row 5: live status / feedback banner
status_lbl = tk.Label(
    root, 
    text="Status: Ready to log match.",
    foreground="#555555",
    font=("arial", 10, "italic"),
    wraplength=360,
    justify="center"
)
status_lbl.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 15), sticky='nsew')

# Master Submit, kinda like the master emerald, but not as powerful, and not as green, and not as shiny, and not as valuable, and not as rare, and not as expensive, and not as useful, and not as good, and not as cool, and not as fun, and not as interesting, and not as exciting, and not as entertaining, and not as enjoyable, and not as satisfying, and not as rewarding, and not as fulfilling, and not as meaningful, and not as significant, and not as impactful, and not as influential, and not as important, and not as relevant, and not as applicable, and not as practical, and not as useful, and not as beneficial, and not as advantageous, and not as helpful, and not as supportive, and not as encouraging, and not as motivating, and not as inspiring, but still pretty good.
submit_btn = tk.Button(
    root, 
    text="Log Match Record", 
    command=submit_match, 
    bg="blue", 
    fg="white", 
    font=("arial", 12, "bold")
)
submit_btn.grid(row=6, column=0, columnspan=2, pady=20, sticky='nsew')

# Calculate Stats Button
stats_btn = tk.Button(
    root, 
    text="Calculate Stats", 
    command=calculate_stats, 
    bg="green", 
    fg="white", 
    font=("arial", 12, "bold")
)
stats_btn.grid(row=7, column=0, columnspan=2, pady=10, sticky='nsew')

# Row 7: Season Reset / Purge Button
purge_btn = tk.Button(
    root, 
    text="Purge Season Data", 
    command=purge_data, 
    bg="#b30000", 
    fg="white", 
    font=("arial", 10, "bold")
)

purge_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=(0, 15), sticky='nsew')

format_dropdown.bind("<<ComboboxSelected>>", on_format_change)
on_format_change() #syncs visability when the window first opens

deck_dropdown.bind("<<ComboboxSelected>>", deck_change)
opponent_dropdown.bind("<<ComboboxSelected>>", opponent_change)



root.mainloop()  # Start the GUI event loop
