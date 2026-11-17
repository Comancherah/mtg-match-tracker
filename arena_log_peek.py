import os
import json

log_path = os.path.join(
    os.environ["USERPROFILE"],
    "AppData", "LocalLow", "Wizards Of The Coast", "MTGA", "Player.log"
)

MY_PLAYER_NAME = "Comancherah"

current_deck = "Unknown Deck"
my_team = None
current_event = "Unknown"
matches = []

with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line.startswith("{"):
            continue

        # 1. Grab exact Deck Name when entering a queue
        if '"CourseDeckSummary"' in line:
            try:
                data = json.loads(line)
                deck_summary = data.get("CourseDeckSummary") or data.get("Course", {}).get("CourseDeckSummary", {})
                if deck_summary and deck_summary.get("Name"):
                    current_deck = deck_summary["Name"]
            except json.JSONDecodeError:
                pass

        # 2. Grab your teamId & queue (eventId) at the start of the match
        if "MatchGameRoomStateType_Playing" in line:
            try:
                data = json.loads(line)
                players = (
                    data.get("matchGameRoomStateChangedEvent", {})
                    .get("gameRoomInfo", {})
                    .get("gameRoomConfig", {})
                    .get("reservedPlayers", [])
                )
                for p in players:
                    if p.get("playerName") == MY_PLAYER_NAME:
                        my_team = p.get("teamId")
                        current_event = p.get("eventId", "Unknown")
            except json.JSONDecodeError:
                pass

        # 3. Grab Win/Loss & final Turn Number when the match finishes
        if '"MatchState_MatchComplete"' in line or '"MatchState_GameComplete"' in line:
            try:
                data = json.loads(line)
                messages = data.get("greToClientEvent", {}).get("greToClientMessages", [])
                winning_team = None
                final_turn = None

                for msg in messages:
                    gsm = msg.get("gameStateMessage", {})
                    game_info = gsm.get("gameInfo", {})
                    if game_info.get("matchState") == "MatchState_MatchComplete":
                        for res in game_info.get("results", []):
                            if res.get("scope") == "MatchScope_Match":
                                winning_team = res.get("winningTeamId")
                    for p in gsm.get("players", []):
                        if "turnNumber" in p:
                            final_turn = p["turnNumber"]

                if winning_team is not None and my_team is not None:
                    result = "Win" if winning_team == my_team else "Loss"
                    matches.append({
                        "deck_name": current_deck,
                        "format": current_event,
                        "result": result,
                        "turns": final_turn
                    })
                    my_team = None  # Reset so Best-of-1 doesn't double-count
            except json.JSONDecodeError:
                pass

print(f"Found {len(matches)} completed match(es):\n")
for i, m in enumerate(matches, 1):
    print(f"Match {i}: Deck='{m['deck_name']}' | Queue='{m['format']}' | Result={m['result']} | Turns={m['turns']}")
