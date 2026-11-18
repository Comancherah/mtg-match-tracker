import os
import json

log_path = os.path.join(
    os.environ["USERPROFILE"],
    "AppData", "LocalLow", "Wizards Of The Coast", "MTGA", "Player.log"
)

# Set some variables
MY_PLAYER_NAME = "Comancherah"

QUEUE_MAP = {
    "Play": "Standard",
    "Ladder": "Standard",
    "Play_Brawl": "Brawl",
    "Brawl_Ladder": "Brawl",
    "Alchemy_Play": "Alchemy",
    "Alchemy_Ladder": "Alchemy",
    "Historic_Play": "Historic",
    "Historic_Ladder": "Historic",
    "Explorer_Play": "Explorer",
    "Explorer_Ladder": "Explorer",
    "Timeless_Play": "Timeless",
    "Timeless_Ladder": "Timeless",
    "AIBotMatch": "Bot Match",
}

def map_arena_queue(raw_queue):
    #Compare with dictionary
    if raw_queue in QUEUE_MAP:
        return QUEUE_MAP[raw_queue]

    # 2. Fallback for any weird event queue name we haven't seen yet (like "Traditional_Brawl_Play")
    if "Brawl" in raw_queue:
        return "Brawl"
    return f"Unknown Queues ({raw_queue}), Suspect arena Update ID's changed." 


def get_last_arena_match(player_name):
   
    current_deck = "Unknown Deck"
    my_team = None
    current_event = "Unknown"
    matches = []

    if not os.path.exists(log_path):
        return None

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
                        if p.get("playerName") == player_name:
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
              
    if not matches:
        return None

    last_match = matches[-1]
    last_match["format"] = map_arena_queue(last_match["format"])
    last_match["turns"] = last_match["turns"] or 0
    return last_match

#For Debugging program can be run standalone
if __name__ == "__main__":
    print(get_last_arena_match("Comancherah"))