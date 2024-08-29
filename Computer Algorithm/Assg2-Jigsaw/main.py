import pygame
import random
import heapq
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Set up window and grid size
WINDOW_SIZE = (832, 832)  # The size of the Pygame window
TILE_SIZE = 32  # Size of each puzzle tile
GRID_SIZE = 26  # Number of tiles along each dimension

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Jigsaw Puzzle")

# Huffman Node class for compression
class HuffmanNode:
    def __init__(self, char, freq):  # Correctly defined __init__ method
        self.char = char  # Character or None for internal nodes
        self.freq = freq  # Frequency of the character
        self.left = None  # Left child
        self.right = None  # Right child
    
    def __lt__(self, other):  # Needed for heap operations
        return self.freq < other.freq

# Build Huffman Tree for data compression
def build_huffman_tree(data):
    # Calculate frequency of each character
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1
    
    # Create a priority queue (heap) of Huffman nodes
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    # Build the tree by merging the two smallest nodes until one remains
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

# Generate Huffman codes from the tree
def generate_huffman_codes(root, code="", mapping=None):
    if mapping is None:
        mapping = {}
    
    if root is None:
        return
    
    if root.char is not None:
        mapping[root.char] = code
    
    generate_huffman_codes(root.left, code + "0", mapping)
    generate_huffman_codes(root.right, code + "1", mapping)
    
    return mapping

# Class representing a puzzle tile
class Tile:
    def __init__(self, id, image):
        self.id = id  # Unique ID for the tile
        self.image = image  # Image representing the tile
        self.rotation = 0  # Current rotation of the tile

    # Rotate the tile by 90 degrees
    def rotate(self):
        self.rotation = (self.rotation + 90) % 360
        self.image = pygame.transform.rotate(self.image, 90)

# Recorder class to track and compress puzzle moves
class JigsawRecorder:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.moves = []  # List of recorded moves
        self.huffman_codes = None
    
    # Record a move made by the player
    def record_move(self, tile_id, old_x, old_y, new_x, new_y, rotation):
        move = (tile_id, old_x, old_y, new_x, new_y, rotation)
        self.moves.append(move)
    
    # Compress the recorded moves using Huffman coding
    def compress_moves(self):
        move_data = "".join(str(m) for m in self.moves)
        huffman_tree = build_huffman_tree(move_data)
        self.huffman_codes = generate_huffman_codes(huffman_tree)
        
        compressed_data = ""
        for char in move_data:
            compressed_data += self.huffman_codes[char]
        
        return compressed_data
    
    # Decompress the Huffman-compressed moves
    def decompress_moves(self, compressed_data):
        reverse_mapping = {code: char for char, code in self.huffman_codes.items()}
        current_code = ""
        decompressed_data = ""
        
        for bit in compressed_data:
            current_code += bit
            if current_code in reverse_mapping:
                decompressed_data += reverse_mapping[current_code]
                current_code = ""
        
        return decompressed_data

    def get_moves(self):
        return self.moves

# Create the jigsaw puzzle tiles from an image
def create_puzzle(image_path):
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, WINDOW_SIZE)
    tiles = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            tile_surface.blit(original_image, (0, 0), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            tile = Tile(i * GRID_SIZE + j, tile_surface)
            if random.choice([True, False]):  # Randomly rotate some tiles
                tile.rotate()
            tiles.append(tile)
    random.shuffle(tiles)  # Shuffle the tiles
    return tiles

# Draw the puzzle on the screen
def draw_puzzle(tiles):
    for i, tile in enumerate(tiles):
        x = (i % GRID_SIZE) * TILE_SIZE
        y = (i // GRID_SIZE) * TILE_SIZE
        screen.blit(tile.image, (x, y))
    pygame.display.flip()

# Main function to run the game
def main():
    tiles = create_puzzle(r"/home/shreyas/TY_IT/Computer Algorithm/Assg2-Jigsaw/image.jpg")
    recorder = JigsawRecorder(tiles)

    selected_tile = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
                index = tile_y * GRID_SIZE + tile_x
                if event.button == 1:  # Left click to select or swap tiles
                    if selected_tile is None:
                        selected_tile = (index, tile_x, tile_y)
                    else:
                        old_index, old_x, old_y = selected_tile
                        tiles[old_index], tiles[index] = tiles[index], tiles[old_index]
                        recorder.record_move(tiles[index].id, old_x, old_y, tile_x, tile_y, tiles[index].rotation)
                        selected_tile = None
                elif event.button == 3:  # Right click to rotate tile
                    tiles[index].rotate()
                    recorder.record_move(tiles[index].id, tile_x, tile_y, tile_x, tile_y, tiles[index].rotation)

        screen.fill(BLACK)
        draw_puzzle(tiles)
        
        if selected_tile:
            x, y = selected_tile[1] * TILE_SIZE, selected_tile[2] * TILE_SIZE
            pygame.draw.rect(screen, RED, (x, y, TILE_SIZE, TILE_SIZE), 2)
        
        pygame.display.flip()

    pygame.quit()

    print("Recorded moves:")
    for move in recorder.get_moves():
        print(move)

    compressed_data = recorder.compress_moves()
    print("Compressed moves:", compressed_data)

    decompressed_data = recorder.decompress_moves(compressed_data)
    print("Decompressed moves:", decompressed_data)

# Run the main function
if __name__ == "__main__":
    main()
