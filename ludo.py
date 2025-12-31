import random

# ------------------ CONSTANTS ------------------
BOARD_SIZE = 30
SAFE_CELLS = [0, 8, 13, 21]
TOKENS_PER_PLAYER = 4

# ------------------ CLASSES ------------------
class Player:
    def __init__(self, name):
        self.name = name
        self.tokens = [-1] * TOKENS_PER_PLAYER  # -1 = in base

    def tokens_on_board(self):
        return any(pos >= 0 for pos in self.tokens)

    def all_home(self):
        return all(pos >= BOARD_SIZE for pos in self.tokens)


# ------------------ FUNCTIONS ------------------
def roll_dice():
    return random.randint(1, 6)


def display_state(players):
    print("\n--- BOARD STATE ---")
    for p in players:
        print(f"{p.name} tokens: {p.tokens}")


def move_token(player, token_index, dice):
    if player.tokens[token_index] == -1:
        if dice == 6:
            player.tokens[token_index] = 0
            return True
        return False
    else:
        player.tokens[token_index] += dice
        return True


def capture(players, current_player):
    for p in players:
        if p == current_player:
            continue
        for i in range(TOKENS_PER_PLAYER):
            for j in range(TOKENS_PER_PLAYER):
                if (
                    p.tokens[i] == current_player.tokens[j]
                    and p.tokens[i] not in SAFE_CELLS
                    and p.tokens[i] < BOARD_SIZE
                ):
                    print(f"💥 {current_player.name} captured {p.name}'s token!")
                    p.tokens[i] = -1


# ------------------ GAME LOOP ------------------
players = [Player("Red"), Player("Blue")]
turn = 0

print("🎲 LUDO GAME STARTED 🎲")

while True:
    current = players[turn]
    print(f"\n🔴 {current.name}'s Turn")

    attempts = 2 if not current.tokens_on_board() else 1
    rolled_six = False

    for attempt in range(attempts):
        input("Press Enter to roll dice...")
        dice = roll_dice()
        print(f"🎲 Rolled: {dice}")

        if dice == 6 or current.tokens_on_board():
            rolled_six = True
            break
        else:
            print(f"Attempts left: {attempts - attempt - 1}")

    if not rolled_six:
        print("❌ No 6 rolled. Turn skipped.")
        turn = (turn + 1) % len(players)
        continue

    print("Choose token (0–3):")
    print(current.tokens)
    token = int(input("Token number: "))

    if move_token(current, token, dice):
        capture(players, current)
    else:
        print("❌ Invalid move")

    display_state(players)

    if current.all_home():
        print(f"\n🏆 {current.name} WINS!")
        break

    if dice != 6:
