import customtkinter as ctk
from tkinter import ttk
import threading
from PIL import Image
from CTkMessagebox import CTkMessagebox

assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True


def read_dictionary(filename):
    trie = Trie()
    with open(filename, "r") as file:
        for word in file:
            trie.insert(word.strip().lower())
    return trie


def solve_wordament(board, dictionary_file):
    trie = read_dictionary(dictionary_file)

    def process_tile(tile):
        if "/" in tile:
            return tile.split("/")
        elif tile.startswith("-"):
            return ["", tile[1:]]
        elif tile.endswith("-"):
            return [tile[:-1], ""]
        elif "-" in tile:
            prefix, suffix = tile.split("-")
            return [prefix, suffix]
        else:
            return [tile]

    def dfs(i, j, prefix, suffix, path, visited, node):
        current_word = prefix + "".join(path) + suffix
        if node.is_end and len(current_word) > 1:
            words.add(current_word)

        for di, dj in [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]:
            ni, nj = i + di, j + dj
            if 0 <= ni < 4 and 0 <= nj < 4 and (ni, nj) not in visited:
                tile_options = process_tile(board[ni][nj])
                for option in tile_options:
                    new_prefix = prefix
                    new_suffix = suffix
                    new_path = path[:]
                    new_node = node
                    if option.endswith("-"):
                        new_suffix = option[:-1] + new_suffix
                    elif option.startswith("-"):
                        new_prefix += option[1:]
                    else:
                        new_path.append(option)
                        for char in option.lower():
                            if char in new_node.children:
                                new_node = new_node.children[char]
                            else:
                                break
                        else:
                            dfs(
                                ni,
                                nj,
                                new_prefix,
                                new_suffix,
                                new_path,
                                visited | {(ni, nj)},
                                new_node,
                            )

    words = set()
    for i in range(4):
        for j in range(4):
            tile_options = process_tile(board[i][j])
            for option in tile_options:
                if option.endswith("-"):
                    dfs(i, j, "", option[:-1], [], {(i, j)}, trie.root)
                elif option.startswith("-"):
                    dfs(i, j, option[1:], "", [], {(i, j)}, trie.root)
                else:
                    node = trie.root
                    for char in option.lower():
                        if char in node.children:
                            node = node.children[char]
                        else:
                            break
                    else:
                        dfs(i, j, "", "", [option], {(i, j)}, node)

    return sorted(list(words), key=len, reverse=True)


def CenterWindowToDisplay(
    Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0
):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


class TopWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(CenterWindowToDisplay(self, 300, 400, self._get_window_scaling()))
        self.resizable(False, False)
        self.minsize(200, 400)
        self.title("Help")


        self.help_text = ctk.CTkTextbox(
            self,
            width=300,
            height=400,
            border_width=1,
            corner_radius=3,
            bg_color="#2b2b2b",
        )
        self.help_text.insert(index="end", text="Enter a 4x4 board left to right, top to bottom." + "\n" + "Enter board exactly as shown on tiles. No spaces." + "\n" + "Example: \n" + "\n" + f"[EN-] [A] [P] [T]" + "\n" + f"[T] [R] [O] [-LY]" + "\n" + f"[W] [Y] [MO] [S]" + "\n" + f"[T] [C/U] [R] [T]" + "\n")
        self.help_text.configure(state="disabled")
        self.help_text.pack()


class WordamentSolverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        global icon_label, icon_image
        
        self.entryfont = (os.path.join(assets + "Segoe-Sans-Text.ttf"), 26)
        icon_size = 24
        icon_path = os.path.join(assets, "Info.png")
        icon_image = ctk.CTkImage(Image.open(icon_path), size=(icon_size, icon_size))
        icon_label = ctk.CTkLabel(self, text="", image=icon_image)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            foreground="#ffffff",
            background="#2b2b2b",
            fieldbackground="#2b2b2b",
        )
        style.map("Treeview", background=[("selected", "#2b2b2b")])

        self.title("Wordament Solver")
        self.geometry(CenterWindowToDisplay(self, 388, 700, self._get_window_scaling()))
        self.resizable(False, False)
        self.minsize(375, 700)

        self.bg_color = "#2b2b2b"
        self.configure(fg_color=self.bg_color)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Board input frame
        self.board_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.board_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # Configure grid of the board_frame
        for i in range(4):
            self.board_frame.grid_columnconfigure(i, weight=1, uniform="both")
            self.board_frame.grid_rowconfigure(i, weight=1)

        # Create a StringVar for each entry
        self.entry_vars = [[ctk.StringVar() for _ in range(4)] for _ in range(4)]

        self.board_entries = []
        for i in range(4):
            row_entries = []
            for j in range(4):
                entry = ctk.CTkEntry(
                    self.board_frame,
                    width=80,
                    height=80,
                    font=self.entryfont,
                    justify="center",
                    textvariable=self.entry_vars[i][j],
                )
                entry.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                row_entries.append(entry)
                # Add trace to StringVar
                self.entry_vars[i][j].trace_add(
                    "write", lambda *args, r=i, c=j: self.validate_entry(r, c)
                )
            self.board_entries.append(row_entries)

        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1, uniform="all")
        self.button_frame.grid_columnconfigure(1, weight=1, uniform="all")
        self.button_frame.grid_rowconfigure(2, weight=1)

        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            width=120,
            command=self.clear_entries,
            fg_color="#bd2c08",
            hover_color="#b54124",
        )
        self.clear_button.grid(row=0, column=0, padx=(0, 0), pady=5, sticky="ew")

        # Help button
        self.help_button = ctk.CTkButton(
            self.button_frame,
            text="",
            command=self.help,
            fg_color="#2b2b2b",
            bg_color="#2b2b2b",
            compound="left",
            hover_color="#2b2b2b",
            image=icon_image,
            width=24,
            height=24,
            anchor="center",
        )
        self.help_button.grid(
            row=0, column=1, padx=0, pady=2, ipadx=0, ipady=0, sticky="ew"
        )

        # Solve button
        self.solve_button = ctk.CTkButton(
            self.button_frame, text="Solve", width=120, command=self.solve_board
        )
        self.solve_button.grid(row=0, column=2, padx=(0, 0), pady=2, sticky="ew")

        self.results_text = ctk.CTkTextbox(
            self, width=310, height=450, border_width=1, corner_radius=3
        )

        self.results_text.insert(
            index="end",
            text="                                 Results will be shown here",
        )
        self.results_text.grid(row=2, column=0, padx=12, pady=(0, 10), sticky="nsew")
        self.results_text.configure(state="disabled")

    topwindow = None

    def error_message(self):
        CTkMessagebox(
            title="Error",
            message="   All tiles must be filled",
            icon="warning",
            justify="center",
            font=("Arial", 14),
            button_height=30,
            button_width=90,
            icon_size=(30, 30),
        )

    def help(self):
        if self.topwindow is None or not self.topwindow.winfo_exists():
            self.topwindow = TopWindow(self)
        else:
            self.topwindow.focus()

        self.solve_button.configure(state="normal", text="Solve")

    def validate_entry(self, row, col):
        value = self.entry_vars[row][col].get()
        # Remove digits and limit to 4 characters
        valid_value = "".join(char for char in value if not char.isdigit())[:4].upper()
        if valid_value != value:
            self.entry_vars[row][col].set(valid_value)

    def clear_entries(self):
        # Clear all entries
        for row in self.entry_vars:
            for var in row:
                var.set("")

        # Set focus to the top-left entry
        self.board_entries[0][0].focus_set()

    def get_board(self):
        board = []
        for row in self.entry_vars:
            board_row = []
            for var in row:
                value = var.get().strip().upper()
                if not value:
                    raise ValueError("All tiles must be filled")
                board_row.append(value)
            board.append(board_row)
        return board

    def solve_board(self):
        try:
            board = self.get_board()
        except ValueError:
            self.error_message()
            return

        self.solve_button.configure(state="disabled", text="Solving...")
        # Run the solver in a separate thread
        threading.Thread(target=self.run_solver, args=(board,), daemon=True).start()

    def run_solver(self, board):
        dictionary_file = "wordament_dictionary.txt"  # need a proper dictionary
        result = solve_wordament(board, dictionary_file)

        self.results_tree = ttk.Treeview(
            self, columns=("Word", "Length"), show="headings"
        )
        self.results_tree.heading("Word", text="Word")
        self.results_tree.heading("Length", text="Length")
        self.results_tree.column("Word", anchor="w")
        self.results_tree.column("Length", anchor="center", width=100)
        self.results_tree.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tree_scroll = ctk.CTkScrollbar(
            self,
            orientation="vertical",
            button_hover_color="#87afd7",
            command=self.results_tree.yview,
        )
        self.tree_scroll.grid(row=2, column=1, sticky="ns")
        self.results_tree.configure(yscrollcommand=self.tree_scroll.set)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Insert new results
        for word in sorted(result, key=len, reverse=True):
            self.results_tree.insert("", "end", values=(word, len(word)))

        self.after(0, self.update_solve_button)

    def update_solve_button(self):
        self.solve_button.configure(state="normal", text="Solve")


##if os.name == "posix":
   # ctk.deactivate_automatic_dpi_awareness()

if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    app = WordamentSolverApp()
    app.mainloop()
