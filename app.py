import tkinter as tk
import os
import webbrowser
from tkinter import ttk
import customtkinter as ctk
import threading
import re
from CTkMessagebox import CTkMessagebox

assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Credit to official CustomTkinter GitHub thread for this banger utility to center window
def CenterWindowToDisplay(
    Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __contains__(self, word):
        return self.search(word)
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return True

class WordamentSolver:
    def __init__(self):
        self.trie = Trie()
        self.board = []
        self.special_tiles = {}
        self.letter_values = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
            'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
            'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
        }
# Problem here is tile value isn't a constant and there are various multipliers. The multipliers might be constants for word length, but conditionals apply in outlier circumstances
# These values are as close as it's gonna get unless I actually implement OCR that isn't drunk and take real-time values off tiles 
    def load_dictionary(self, file_path):
        with open(file_path, 'r') as f:
            for word in f:
                self.trie.insert(word.strip())

       


    def set_board(self, board, special_tiles):
        self.board = [[tile.upper() for tile in row] for row in board]
        for (i, j), tile in special_tiles.items():
            if '/' in tile:
                self.board[i][j] = tile.split('/')  # Store as a list of possible characters
            else:
                self.board[i][j] = tile

    def calculate_word_value(self, word):
        return sum(self.letter_values.get(letter.upper(), 0) for letter in word)

    def solve(self):
        self.words = []
        self.visited = set()
        
        for i in range(4):
            for j in range(4):
                self.iterative_dfs(i, j, "", set())
        
        return sorted(list(set(self.words)), key=lambda x: (-len(x), x))

    def iterative_dfs(self, i, j, current_word, visited):
        stack = [(i, j, current_word, visited)]
        
        while stack:
            i, j, current_word, visited = stack.pop()
            
            if (i, j) in visited:
                continue
            
            visited = visited.copy()
            visited.add((i, j))
            
            tile = self.board[i][j]
            if isinstance(tile, list):  # Handle either/or tiles
                possible_chars = tile
            else:
                possible_chars = [tile]
            
            for char in possible_chars:
                new_word = current_word + char
                
                if new_word in self.trie:
                    if len(new_word) >= 3 and new_word in self.trie:  
                        self.words.append((new_word, len(new_word), self.calculate_word_value(new_word)))
                
                if self.trie.starts_with(new_word):
                    for ni, nj in self.get_neighbors(i, j):
                        if (ni, nj) not in visited:
                            stack.append((ni, nj, new_word, visited))

    def get_neighbors(self, i, j):
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < 4 and 0 <= nj < 4 and (di != 0 or dj != 0):
                    neighbors.append((ni, nj))
        return neighbors  


class WordamentGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Wordament Solver")
        self.root.geometry(CenterWindowToDisplay(self.root, 630, 700, 1.0))
        load_font = os.path.join(assets, "Segoe-Sans-Text.ttf")
        self.entry_font = (ctk.CTkFont(family=load_font, size=26))
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            foreground="#ffffff",
            background="#2b2b2b",
            fieldbackground="#2b2b2b",
        )
        style.map("Treeview", background=[("selected", "#2b2b2b")])


        self.solver = WordamentSolver()
        self.solver.load_dictionary(os.path.join(assets, "wordament_dictionary.txt"))

        self.words = []
        self.create_widgets()

    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
      

        # frame (top left)
        board_frame = ctk.CTkFrame(self.root, bg_color="transparent")
        board_frame.grid(row=0, column=0, padx=5, pady=5)
        board_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform="both")
        board_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="both")

        self.entry_vars = [[ctk.StringVar() for _ in range(4)] for _ in range(4)]

        self.entries = []
        for i in range(4):
            row = []
            for j in range(4):
                entry = ctk.CTkEntry(board_frame, width=80, height=80, justify='center', font=self.entry_font, textvariable=self.entry_vars[i][j])
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.grid_rowconfigure((0, 1, 2, 3), weight=1)
                entry.grid_columnconfigure((0, 1, 2, 3), weight=1)
                #entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.validate_input(e, r, c))
                row.append(entry)
                self.entry_vars[i][j].trace_add('write', lambda *args, r=i, c=j: self.validate_input(r, c))
            self.entries.append(row)

        # frame (top right)
        button_frame = ctk.CTkFrame(self.root, bg_color="transparent", fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


        self.solve_button = ctk.CTkButton(button_frame, text="Solve", command=self.solve, text_color="#000000", fg_color="#00a500", hover_color="#00c100")
        self.solve_button.place(relx=0.5, rely=0.3, anchor="center")
        #self.solve_button.pack(pady=5, padx=5, anchor="center", expand=True)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_board, text_color="#000000", fg_color="#c6b040", hover_color="#dfc649")
        self.clear_button.place(relx=0.5, rely=0.5, anchor="center")
        #self.clear_button.pack(pady=5, padx=5, anchor="center", expand=True)

        self.quit_button = ctk.CTkButton(button_frame, text="Quit", command=self.quit_app, text_color="#000000", fg_color="#a80000", hover_color="#c30000")
        self.quit_button.place(relx=0.5, rely=0.7, anchor="center")
        #self.quit_button.pack(pady=5, padx=5, anchor="center", expand=True)

        # Treeview frame (bottom, spanning width)
        tree_frame = ctk.CTkFrame(self.root)
        tree_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create actual Treeview
        self.tree = ttk.Treeview(tree_frame, columns=('Word', 'Length', 'Value'), show='headings', selectmode="none", style='Treeview')
        self.tree.heading('Word', text='Word', command=lambda: self.treeview_sort_column('Word', False))
        self.tree.heading('Length', text='Length', command=lambda: self.treeview_sort_column('Length', False))
        self.tree.heading('Value', text='Value', command=lambda: self.treeview_sort_column('Value', False))
        self.tree.column('Word', width=200)
        self.tree.column('Length', width=80, anchor='center')
        self.tree.column('Value', width=80, anchor='center')
        self.tree.pack(side=tk.LEFT, expand=True, fill="both")

        # Scrollbar for Treeview, had trouble keeping it slim and padded on y axis
        scrollbar = ctk.CTkScrollbar(tree_frame, orientation="vertical", command=self.tree.yview, border_spacing=2, width=5)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y", ipadx=4)

        # Configure tag for alternating row colors
        self.tree.tag_configure('oddrow', background='#2a2d2e')
        self.tree.tag_configure('evenrow', background='#212325')

    def validate_input(self, row, col):
        value = self.entry_vars[row][col].get().upper()
        
        # This needs work for sure
        filtered_value = "".join(char for char in value if not char.isdigit())[:4].upper()
        
        # Ditto
        if len(filtered_value) > 1:
            if filtered_value.startswith('-') or filtered_value.endswith('-'):
                filtered_value = filtered_value[:4]  # Allow up to 4 characters for prefix/suffix tiles
            elif '/' in filtered_value:
                filtered_value = filtered_value[:3]  # Limit to 3 characters for tiles with '/', But filter needs to not allow / at start or end. See actual implementation below
            elif len(filtered_value) == 4 and filtered_value.endswith('-'):
                filtered_value = filtered_value[:3]  # Limit to 3 characters + special for tiles like MIS-
            elif len(filtered_value) == 2:    
                filtered_value = filtered_value[:2]
        else:
            filtered_value = filtered_value[:1]  
        
        # Update the entry
        self.entries[row][col].delete(0, tk.END)
        self.entries[row][col].insert(0, filtered_value)
        
    def error_message(self):    # Great utility for CTK 
        CTkMessagebox(
            title="Error",
            message="Properly fill in all tiles",
            icon="warning",
            justify="center",
            font=(self.entry_font, 14),
            button_height=30,
            button_width=50,
            icon_size=(26, 26),
        )

    def solve(self):
        board = [[entry.get().upper() for entry in row] for row in self.entries]
        special_tiles = {}
        for i in range(4):
            for j in range(4):
                tile = board[i][j]
                if re.match(r'^[A-Z]{2,3}-$', tile) or \
                   re.match(r'^-[A-Z]{2,3}$', tile) or \
                   re.match(r'^[A-Z]{2,3}$', tile) or \
                   '/' in tile:
                    special_tiles[(i, j)] = tile
                elif len(tile) != 1:
                    self.error_message()
                    return
        self.solver.set_board(board, special_tiles)
        
        def solve_thread():
            self.words = self.solver.solve()
            self.root.after(0, self.display_results)

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert('', 'end', values=('Solving...', '', ''))
        threading.Thread(target=solve_thread, daemon=True).start() # totally uncessary threading operation

    def display_results(self):
    # Sort by length by default
        sorted_words = sorted(self.words, key=lambda x: (-x[1], x[0]))
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, (word, length, value) in enumerate(sorted_words):
            tag = 'oddrow' if i % 2 else 'evenrow'
            self.tree.insert('', 'end', values=(word, length, value), tags=(tag,))

    def quit_app(self):
        self.root.destroy()

    def clear_board(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.entries[0][0].focus_set()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        if col == 'Word':
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)
        elif col in ['Length', 'Value']:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
            self.tree.item(k, tags=('oddrow' if index % 2 else 'evenrow',))

        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WordamentGUI()
    app.run()