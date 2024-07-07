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
    with open(filename, 'r') as file:
        for word in file:
            trie.insert(word.strip().lower())
    return trie

def get_board_input():
    board = []
    print("Enter the Wordament board, row by row.")
    print("Use spaces between tiles and press Enter after each row.")
    print("For special tiles, use '**-' for prefixes, '-**' for suffixes, '*/*' for either/or, and '**' for double letters.")
    for i in range(4):
        while True:
            row = input(f"Enter row {i+1}: ").strip().upper().split()
            if len(row) == 4:
                board.append(row)
                break
            else:
                print("Please enter exactly 4 tiles.")
    return board

def solve_wordament(board, dictionary_file):
    trie = read_dictionary(dictionary_file)

    def process_tile(tile):
        if '/' in tile:
            return tile.split('/')
        elif '-' in tile:
            if tile.startswith('-'):
                return ['', tile[1:]]
            elif tile.endswith('-'):
                return [tile[:-1], '']
            else:
                return tile.split('-')
        elif len(tile) == 2 and tile.isalpha():  # Handle double letter tiles
            return [tile]
        return [tile]

    def dfs(i, j, prefix, suffix, path, visited, node):
        current_word = prefix + ''.join(path) + suffix
        if node.is_end and len(current_word) > 1:
            words.add(current_word)
        
        for di, dj in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < 4 and 0 <= nj < 4 and (ni, nj) not in visited:
                tile_options = process_tile(board[ni][nj])
                for option in tile_options:
                    new_prefix = prefix
                    new_suffix = suffix
                    new_path = path[:]
                    new_node = node
                    if option.endswith('-'):
                        new_suffix = option[:-1] + new_suffix
                    elif option.startswith('-'):
                        new_prefix += option[1:]
                    else:
                        new_path.append(option)
                        for char in option.lower():
                            if char in new_node.children:
                                new_node = new_node.children[char]
                            else:
                                break
                        else:
                            dfs(ni, nj, new_prefix, new_suffix, new_path, visited | {(ni, nj)}, new_node)

    words = set()
    for i in range(4):
        for j in range(4):
            tile_options = process_tile(board[i][j])
            for option in tile_options:
                if option.endswith('-'):
                    dfs(i, j, '', option[:-1], [], {(i, j)}, trie.root)
                elif option.startswith('-'):
                    dfs(i, j, option[1:], '', [], {(i, j)}, trie.root)
                else:
                    node = trie.root
                    for char in option.lower():
                        if char in node.children:
                            node = node.children[char]
                        else:
                            break
                    else:
                        dfs(i, j, '', '', [option], {(i, j)}, node)
    
    return sorted(list(words), key=len, reverse=False)

# Main execution
dictionary_file = 'wordament_dictionary.txt'  # Path to your dictionary file
board = get_board_input()
result = solve_wordament(board, dictionary_file)

print("\nFound words (sorted by length):")
for word in result:
    print(word)
