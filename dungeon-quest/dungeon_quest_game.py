import json
import random
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================================
# DUNGEON QUEST - A PYTHON ADVENTURE GAME
# Built with Python and Tkinter
# ==========================================================

SAVE_FILE = "dungeon_quest_save.json"

BG = "#101827"
PANEL = "#1D293B"
PANEL_LIGHT = "#26364C"
GOLD = "#F5C451"
WHITE = "#F3F4F6"
MUTED = "#B8C3D4"
RED = "#E05252"
GREEN = "#35B879"
BLUE = "#4285F4"
PURPLE = "#9B7AE8"


class DungeonQuest:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Quest | Python Adventure")
        self.root.geometry("940x760")
        self.root.minsize(760, 650)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

        self.high_score = self.load_high_score()
        self.reset_game_state()
        self.create_layout()
        self.show_main_menu()

    # ------------------------------------------------------
    # GAME STATE
    # ------------------------------------------------------

    def reset_game_state(self):
        self.player_name = "Adventurer"
        self.player_health = 60
        self.max_health = 60
        self.attack_power = 10
        self.armor = 0
        self.coins = 0
        self.score = 0
        self.potions = 2
        self.level = 1
        self.enemy_name = ""
        self.enemy_health = 0
        self.enemy_max_health = 0
        self.enemy_attack_min = 4
        self.enemy_attack_max = 10
        self.defending = False
        self.inventory = []
        self.visited_rooms = []
        self.achievements = []
        self.game_active = False
        self.battle_active = False
        self.treasure_claimed = False
        self.boss_defeated = False
        self.difficulty = "Normal"

    # ------------------------------------------------------
    # WINDOW LAYOUT
    # ------------------------------------------------------

    def create_layout(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(16, 8))

        tk.Label(
            header, text="⚔  DUNGEON QUEST",
            font=("Georgia", 27, "bold"), fg=GOLD, bg=BG
        ).pack()

        tk.Label(
            header, text="A Python Adventure Game",
            font=("Arial", 11), fg=MUTED, bg=BG
        ).pack(pady=(3, 0))

        self.stats_frame = tk.Frame(self.root, bg=PANEL)
        self.stats_frame.pack(fill="x", padx=24, pady=8)

        self.health_label = self.make_stat_label(self.stats_frame, "❤️ Health")
        self.health_label.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="w")
        self.health_bar = ttk.Progressbar(
            self.stats_frame, maximum=self.max_health, length=180,
            mode="determinate", style="Health.Horizontal.TProgressbar"
        )
        self.health_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.level_label = self.make_stat_label(self.stats_frame, "🗺 Level: 1")
        self.level_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.coins_label = self.make_stat_label(self.stats_frame, "🪙 Coins: 0")
        self.coins_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.score_label = self.make_stat_label(self.stats_frame, "⭐ Score: 0")
        self.score_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.potion_label = self.make_stat_label(self.stats_frame, "🧪 Potions: 2")
        self.potion_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        for column in range(3):
            self.stats_frame.columnconfigure(column, weight=1)

        self.story_frame = tk.Frame(
            self.root, bg=PANEL,
            highlightbackground="#36465E", highlightthickness=1
        )
        self.story_frame.pack(fill="both", expand=True, padx=24, pady=(5, 12))

        self.story_title = tk.Label(
            self.story_frame, text="Your Adventure Begins",
            font=("Georgia", 19, "bold"), fg=GOLD, bg=PANEL
        )
        self.story_title.pack(pady=(22, 12))

        self.story_text = tk.Label(
            self.story_frame, text="", font=("Arial", 12),
            fg=WHITE, bg=PANEL, wraplength=800,
            justify="center", padx=20
        )
        self.story_text.pack(fill="both", expand=True, padx=22, pady=12)

        self.extra_frame = tk.Frame(self.story_frame, bg=PANEL)
        self.extra_frame.pack(fill="x", padx=25, pady=(0, 15))

        self.button_frame = tk.Frame(self.root, bg=BG)
        self.button_frame.pack(fill="x", padx=24, pady=(0, 8))

        self.footer = tk.Label(
            self.root,
            text="Explore wisely. Your choices shape your destiny.",
            font=("Arial", 9, "italic"), fg=MUTED, bg=BG
        )
        self.footer.pack(pady=(0, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Health.Horizontal.TProgressbar",
            troughcolor=PANEL_LIGHT, background=GREEN,
            bordercolor=PANEL, lightcolor=GREEN, darkcolor=GREEN
        )
        style.configure(
            "Enemy.Horizontal.TProgressbar",
            troughcolor=PANEL_LIGHT, background=RED,
            bordercolor=PANEL, lightcolor=RED, darkcolor=RED
        )
        self.update_stats()

    def make_stat_label(self, parent, text):
        return tk.Label(
            parent, text=text, font=("Arial", 10, "bold"),
            fg=WHITE, bg=PANEL
        )

    def set_story(self, title, text):
        self.story_title.config(text=title)
        self.story_text.config(text=text)

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def clear_extra(self):
        for widget in self.extra_frame.winfo_children():
            widget.destroy()

    def add_button(self, text, command, color=BLUE):
        button = tk.Button(
            self.button_frame, text=text, command=command,
            font=("Arial", 10, "bold"), fg="white", bg=color,
            activebackground=color, activeforeground="white",
            relief="flat", cursor="hand2", padx=12, pady=10,
            wraplength=190
        )
        button.pack(side="left", expand=True, fill="x", padx=4, pady=4)
        button.bind("<Enter>", lambda event: button.config(
            highlightthickness=1, highlightbackground=GOLD
        ))
        button.bind("<Leave>", lambda event: button.config(
            highlightthickness=0
        ))
        return button

    def update_stats(self):
        self.health_label.config(
            text=f"❤️ Health: {self.player_health}/{self.max_health}"
        )
        self.health_bar.configure(maximum=self.max_health)
        self.health_bar["value"] = self.player_health
        self.level_label.config(text=f"🗺 Level: {self.level}")
        self.coins_label.config(text=f"🪙 Coins: {self.coins}")
        self.score_label.config(text=f"⭐ Score: {self.score}")
        self.potion_label.config(text=f"🧪 Potions: {self.potions}")

    # ------------------------------------------------------
    # SAVE DATA AND HIGH SCORE
    # ------------------------------------------------------

    def load_save_data(self):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                return {}
            return data
        except (OSError, json.JSONDecodeError):
            return {}

    def load_high_score(self):
        data = self.load_save_data()
        try:
            return max(0, int(data.get("high_score", 0)))
        except (ValueError, TypeError):
            return 0

    def save_game(self, show_message=True):
        data = {
            "high_score": max(self.high_score, self.score),
            "player_name": self.player_name,
            "player_health": self.player_health,
            "max_health": self.max_health,
            "attack_power": self.attack_power,
            "armor": self.armor,
            "coins": self.coins,
            "score": self.score,
            "potions": self.potions,
            "level": self.level,
            "inventory": self.inventory,
            "visited_rooms": self.visited_rooms,
            "achievements": self.achievements,
            "difficulty": self.difficulty,
            "treasure_claimed": self.treasure_claimed,
            "boss_defeated": self.boss_defeated,
            "game_active": self.game_active
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            self.high_score = data["high_score"]
            if show_message:
                messagebox.showinfo("Game Saved", "Your progress has been saved!")
        except OSError:
            messagebox.showerror(
                "Save Error", "Could not save the game. Check folder permissions."
            )

    def continue_game(self):
        data = self.load_save_data()
        if not data.get("game_active"):
            messagebox.showinfo(
                "No Saved Game",
                "There is no saved adventure to continue. Start a new game first."
            )
            return

        try:
            self.player_name = str(data.get("player_name", "Adventurer"))[:24]
            self.max_health = max(1, int(data.get("max_health", 60)))
            self.player_health = max(
                1, min(self.max_health, int(data.get("player_health", self.max_health)))
            )
            self.attack_power = max(1, int(data.get("attack_power", 10)))
            self.armor = max(0, int(data.get("armor", 0)))
            self.coins = max(0, int(data.get("coins", 0)))
            self.score = max(0, int(data.get("score", 0)))
            self.potions = max(0, int(data.get("potions", 0)))
            self.level = max(1, min(4, int(data.get("level", 1))))
            self.inventory = list(data.get("inventory", []))
            self.visited_rooms = list(data.get("visited_rooms", []))
            self.achievements = list(data.get("achievements", []))
            self.difficulty = data.get("difficulty", "Normal")
            self.treasure_claimed = bool(data.get("treasure_claimed", False))
            self.boss_defeated = bool(data.get("boss_defeated", False))
            self.game_active = True
            self.battle_active = False
            self.defending = False
            self.update_stats()
            self.show_hub(
                "Your saved adventure has been restored. Choose where to go next."
            )
        except (ValueError, TypeError):
            messagebox.showerror(
                "Save Error", "The saved game data is invalid. Start a new game instead."
            )

    # ------------------------------------------------------
    # MAIN MENU AND NEW GAME
    # ------------------------------------------------------

    def show_main_menu(self):
        self.clear_buttons()
        self.clear_extra()
        self.set_story(
            "Welcome, Adventurer!",
            "Enter an ancient dungeon filled with dangerous creatures, "
            "hidden treasure, and forgotten magic.\n\n"
            "Defeat enemies, collect coins, buy equipment, complete quests, "
            "and try to defeat the final boss.\n\n"
            f"Personal Best: {self.high_score} points\n\n"
            "Tip: Defending reduces the next enemy attack."
        )
        self.add_button("⚔ New Adventure", self.new_game, GREEN)
        self.add_button("▶ Continue", self.continue_game, BLUE)
        self.add_button("🏆 Achievements", self.show_achievements, PURPLE)
        self.add_button("✖ Quit", self.quit_game, RED)

    def new_game(self):
        self.reset_game_state()
        self.game_active = True
        self.clear_buttons()
        self.clear_extra()

        form = tk.Frame(self.extra_frame, bg=PANEL)
        form.pack()

        tk.Label(
            form, text="Adventurer name:", fg=WHITE, bg=PANEL,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=6, pady=5)

        name_entry = tk.Entry(
            form, width=18, font=("Arial", 11),
            bg="#F3F4F6", fg="#101827"
        )
        name_entry.insert(0, "Adventurer")
        name_entry.grid(row=0, column=1, padx=6, pady=5)

        tk.Label(
            form, text="Difficulty:", fg=WHITE, bg=PANEL,
            font=("Arial", 10, "bold")
        ).grid(row=1, column=0, padx=6, pady=5)

        difficulty = tk.StringVar(value="Normal")
        difficulty_box = ttk.Combobox(
            form, textvariable=difficulty,
            values=["Easy", "Normal", "Hard"],
            state="readonly", width=15
        )
        difficulty_box.grid(row=1, column=1, padx=6, pady=5)

        def start():
            name = name_entry.get().strip()
            self.player_name = name[:24] if name else "Adventurer"
            self.difficulty = difficulty.get()
            if self.difficulty == "Easy":
                self.max_health = 75
                self.player_health = 75
                self.potions = 3
            elif self.difficulty == "Hard":
                self.max_health = 45
                self.player_health = 45
                self.potions = 1
            else:
                self.max_health = 60
                self.player_health = 60
                self.potions = 2
            self.update_stats()
            self.show_hub(
                f"Welcome, {self.player_name}! Difficulty: {self.difficulty}.\n\n"
                "Your adventure begins at the dungeon entrance."
            )

        self.add_button("Begin Adventure", start, GREEN)
        self.add_button("Back to Menu", self.show_main_menu)

    # ------------------------------------------------------
    # DUNGEON HUB AND LEVELS
    # ------------------------------------------------------

    def show_hub(self, message="Choose your next action."):
        self.battle_active = False
        self.clear_buttons()
        self.clear_extra()
        self.update_stats()

        self.set_story(
            f"Dungeon Camp — Level {self.level}",
            f"{message}\n\n"
            "From the camp, you can explore the next room, visit the shop, "
            "check your inventory, or save your progress."
        )
        self.add_button("🗺 Explore Dungeon", self.explore, GREEN)
        self.add_button("🛒 Visit Shop", self.show_shop, GOLD)
        self.add_button("🎒 Inventory", self.show_inventory, BLUE)
        self.add_button("💾 Save Game", self.save_game, PURPLE)
        self.add_button("Main Menu", self.show_main_menu)

    def explore(self):
        if self.level == 1:
            self.start_battle("Goblin", 32, 5, 11)
        elif self.level == 2:
            self.start_battle("Skeleton", 42, 7, 13)
        elif self.level == 3:
            self.start_battle("Orc Warrior", 55, 8, 15)
        else:
            self.start_battle("Dungeon Dragon", 85, 10, 18, boss=True)

    def start_battle(self, enemy, health, attack_min, attack_max, boss=False):
        if self.level in self.visited_rooms and not boss:
            self.show_hub("You have already cleared this room.")
            return

        self.enemy_name = enemy
        self.enemy_max_health = health
        self.enemy_health = health
        self.enemy_attack_min = attack_min
        self.enemy_attack_max = attack_max
        self.battle_active = True
        self.defending = False
        self.is_boss = boss
        self.show_battle(f"{enemy} appears! Prepare yourself.")

    # ------------------------------------------------------
    # COMBAT
    # ------------------------------------------------------

    def show_battle(self, message):
        self.clear_buttons()
        self.clear_extra()
        self.update_stats()

        self.set_story(
            f"⚔ Battle: {self.enemy_name}",
            f"{message}\n\n"
            f"Your Health: {self.player_health}/{self.max_health}\n"
            f"{self.enemy_name} Health: {self.enemy_health}/{self.enemy_max_health}"
        )

        self.enemy_bar = ttk.Progressbar(
            self.extra_frame, maximum=self.enemy_max_health,
            length=300, mode="determinate",
            style="Enemy.Horizontal.TProgressbar"
        )
        self.enemy_bar.pack(pady=5)
        self.enemy_bar["value"] = self.enemy_health

        self.add_button("⚔ Attack", self.attack_enemy, RED)
        self.add_button("🛡 Defend", self.defend)
        self.add_button("🧪 Use Potion", self.use_potion, GREEN)
        self.add_button("🏃 Retreat", self.retreat, "#596579")

    def attack_enemy(self):
        if not self.battle_active:
            return

        damage = random.randint(max(2, self.attack_power - 3), self.attack_power + 3)
        if random.random() < 0.12:
            damage *= 2
            message = f"Critical hit! You deal {damage} damage!"
        else:
            message = f"You attack {self.enemy_name} for {damage} damage."

        self.enemy_health = max(0, self.enemy_health - damage)

        if self.enemy_health <= 0:
            self.win_battle()
            return

        self.enemy_turn(message)

    def defend(self):
        if not self.battle_active:
            return
        self.defending = True
        self.enemy_turn("You take a defensive stance and brace for the attack.")

    def use_potion(self):
        if not self.battle_active:
            return
        if self.potions <= 0:
            self.show_battle("You have no potions left!")
            return
        if self.player_health >= self.max_health:
            self.show_battle("Your health is already full. Save the potion!")
            return

        self.potions -= 1
        healing = random.randint(18, 28)
        actual_healing = min(healing, self.max_health - self.player_health)
        self.player_health += actual_healing
        self.update_stats()
        self.enemy_turn(f"You use a potion and recover {actual_healing} health.")

    def enemy_turn(self, message):
        damage = random.randint(self.enemy_attack_min, self.enemy_attack_max)

        if self.defending:
            damage = max(1, damage // 2)
            self.defending = False

        damage = max(1, damage - self.armor)
        if self.difficulty == "Easy":
            damage = max(1, damage - 2)
        elif self.difficulty == "Hard":
            damage += 2

        self.player_health = max(0, self.player_health - damage)
        message += f"\n\n{self.enemy_name} attacks for {damage} damage."
        self.update_stats()

        if self.player_health <= 0:
            self.finish_game(
                f"{self.enemy_name} defeated you. Your adventure has ended."
            )
        else:
            self.show_battle(message)

    def win_battle(self):
        self.battle_active = False
        self.visited_rooms.append(self.level)

        reward = 100 if self.is_boss else 40 + self.level * 15
        coins_found = random.randint(12, 28) + self.level * 3
        self.score += reward
        self.coins += coins_found
        self.inventory.append(f"{self.enemy_name} Trophy")

        if self.level == 1:
            self.unlock_achievement("Goblin Slayer")
        if self.level >= 2:
            self.unlock_achievement("Dungeon Veteran")
        if self.is_boss:
            self.boss_defeated = True
            self.unlock_achievement("Dragon Slayer")

        self.clear_buttons()
        self.clear_extra()
        self.update_stats()

        if self.is_boss:
            self.set_story(
                "🏆 Dungeon Conquered!",
                f"You defeated the {self.enemy_name} and conquered the dungeon!\n\n"
                f"Reward: {reward} points and {coins_found} coins.\n"
                "You are a true dungeon champion!"
            )
            self.add_button("View Final Results", self.finish_game, GREEN)
            self.add_button("View Achievements", self.show_achievements, PURPLE)
            return

        self.set_story(
            "🏆 Victory!",
            f"You defeated the {self.enemy_name}!\n\n"
            f"Reward: {reward} points and {coins_found} coins.\n"
            f"{self.enemy_name} Trophy added to your inventory.\n\n"
            "You can visit the shop, prepare, and then continue to the next level."
        )
        self.add_button("Continue to Camp", self.advance_level, GREEN)
        self.add_button("Visit Shop", self.show_shop, GOLD)
        self.add_button("View Inventory", self.show_inventory, BLUE)

    def advance_level(self):
        self.level = min(4, self.level + 1)
        self.player_health = min(self.max_health, self.player_health + 8)
        self.update_stats()
        self.show_hub(
            f"You advance to level {self.level}. You recover 8 health while resting."
        )

    def retreat(self):
        if not self.battle_active:
            return
        self.battle_active = False
        self.show_hub("You retreated from the battle. The enemy remains in this room.")

    # ------------------------------------------------------
    # SHOP AND EQUIPMENT
    # ------------------------------------------------------

    def show_shop(self):
        self.clear_buttons()
        self.clear_extra()
        self.set_story(
            "🛒 Dungeon Shop",
            f"You have {self.coins} coins.\n\n"
            "Potion — 15 coins: restores one potion.\n"
            "Iron Sword — 40 coins: increases attack power by 3.\n"
            "Leather Armor — 35 coins: reduces incoming damage by 2.\n\n"
            "Each equipment upgrade can be purchased once."
        )
        self.add_button("Buy Potion (15)", self.buy_potion, GREEN)
        self.add_button("Buy Iron Sword (40)", self.buy_sword, BLUE)
        self.add_button("Buy Leather Armor (35)", self.buy_armor, PURPLE)
        self.add_button("Return to Camp", self.show_hub)

    def buy_potion(self):
        if self.coins < 15:
            messagebox.showinfo("Not Enough Coins", "You need 15 coins.")
            return
        self.coins -= 15
        self.potions += 1
        self.update_stats()
        self.show_shop()

    def buy_sword(self):
        if "Iron Sword" in self.inventory:
            messagebox.showinfo("Already Owned", "You already own the Iron Sword.")
            return
        if self.coins < 40:
            messagebox.showinfo("Not Enough Coins", "You need 40 coins.")
            return
        self.coins -= 40
        self.attack_power += 3
        self.inventory.append("Iron Sword")
        self.update_stats()
        self.show_shop()

    def buy_armor(self):
        if "Leather Armor" in self.inventory:
            messagebox.showinfo("Already Owned", "You already own Leather Armor.")
            return
        if self.coins < 35:
            messagebox.showinfo("Not Enough Coins", "You need 35 coins.")
            return
        self.coins -= 35
        self.armor += 2
        self.inventory.append("Leather Armor")
        self.update_stats()
        self.show_shop()

    # ------------------------------------------------------
    # INVENTORY AND ACHIEVEMENTS
    # ------------------------------------------------------

    def show_inventory(self):
        self.clear_buttons()
        self.clear_extra()

        items = "\n".join(f"• {item}" for item in self.inventory)
        if not items:
            items = "Your inventory is empty."

        self.set_story(
            "🎒 Inventory",
            f"Adventurer: {self.player_name}\n\n"
            f"{items}\n\n"
            f"Coins: {self.coins}\nPotions: {self.potions}\n"
            f"Attack Power: {self.attack_power}\nArmor: {self.armor}\n"
            f"Health: {self.player_health}/{self.max_health}\nScore: {self.score}"
        )
        self.add_button("Return to Camp", self.show_hub, GREEN)
        self.add_button("Visit Shop", self.show_shop, GOLD)
        self.add_button("Save Game", self.save_game, PURPLE)

    def unlock_achievement(self, name):
        if name not in self.achievements:
            self.achievements.append(name)

    def show_achievements(self):
        self.clear_buttons()
        self.clear_extra()
        all_achievements = [
            ("Goblin Slayer", "Defeat the goblin in Level 1."),
            ("Dungeon Veteran", "Reach and clear Level 2 or beyond."),
            ("Dragon Slayer", "Defeat the final dungeon boss.")
        ]
        lines = []
        for name, description in all_achievements:
            status = "UNLOCKED" if name in self.achievements else "LOCKED"
            lines.append(f"{'✓' if status == 'UNLOCKED' else '🔒'} {name} — {status}\n{description}")
        self.set_story("🏆 Achievements", "\n\n".join(lines))
        self.add_button("Back to Menu", self.show_main_menu, BLUE)
        if self.game_active:
            self.add_button("Return to Camp", self.show_hub, GREEN)

    # ------------------------------------------------------
    # GAME OVER AND QUIT
    # ------------------------------------------------------

    def finish_game(self, message=None):
        self.battle_active = False
        self.game_active = False
        self.clear_buttons()
        self.clear_extra()

        self.high_score = max(self.high_score, self.score)
        self.save_game(show_message=False)
        self.update_stats()

        if message is None:
            message = "Your adventure has come to an end."

        achievements = ", ".join(self.achievements) if self.achievements else "None yet"

        self.set_story(
            "🏰 Adventure Complete",
            f"{message}\n\n"
            f"Adventurer: {self.player_name}\n"
            f"Final Score: {self.score}\n"
            f"Coins Collected: {self.coins}\n"
            f"Personal Best: {self.high_score}\n\n"
            f"Achievements: {achievements}\n\n"
            "Start a new adventure to try for a higher score!"
        )
        self.add_button("🔄 Play Again", self.new_game, GREEN)
        self.add_button("Main Menu", self.show_main_menu, BLUE)
        self.add_button("Quit", self.quit_game, RED)

    def quit_game(self):
        if self.game_active and messagebox.askyesno(
            "Quit Dungeon Quest",
            "Quit the game? Save your progress first if you want to continue later."
        ):
            self.root.destroy()
        elif not self.game_active:
            self.root.destroy()


# ----------------------------------------------------------
# START THE APPLICATION
# ----------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Health.Horizontal.TProgressbar",
        troughcolor=PANEL_LIGHT, background=GREEN,
        bordercolor=PANEL, lightcolor=GREEN, darkcolor=GREEN
    )
    style.configure(
        "Enemy.Horizontal.TProgressbar",
        troughcolor=PANEL_LIGHT, background=RED,
        bordercolor=PANEL, lightcolor=RED, darkcolor=RED
    )

    game = DungeonQuest(root)
    root.mainloop()
