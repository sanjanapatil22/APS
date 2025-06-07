from heapq import heappush, heappop, heapify
import numpy as np

def beam_search(grid, start_pos, products_dict, beam_width=3, max_depth=10):
    """
    Beam Search for Top-N Product Recommendations on a CERT-style grid.

    Args:
        grid (2D array): Product grid (each cell has a product ID or None)
        start_pos (tuple): (row, col) of the starting product
        products_dict (dict): Mapping from product ID to product info
        beam_width (int): Number of best paths to retain at each step
        max_depth (int): Maximum number of steps to explore

    Returns:
        List of top recommended product IDs and their paths
    """

    def heuristic(p1, p2):
        # Semantic similarity
        semantic = calculate_similarity(products_dict[p1], products_dict[p2])
        # Popularity score
        rating_score = products_dict[p2].get('rating', 0)
        # Final heuristic (negative for max-heap behavior)
        return -(semantic + rating_score)

    def get_neighbors(pos):
        row, col = pos
        neighbors = []
        if row > 0: neighbors.append((row - 1, col))
        if row < len(grid) - 1: neighbors.append((row + 1, col))
        if col > 0: neighbors.append((row, col - 1))
        if col < len(grid[0]) - 1: neighbors.append((row, col + 1))
        return neighbors

    # Beam = list of tuples: (score, [path positions])
    start_product = grid[start_pos[0]][start_pos[1]]
    beam = [(-1.0, [start_pos])]  # initialize with dummy low score
    visited = set()

    for _ in range(max_depth):
        new_beam = []
        for score, path in beam:
            current_pos = path[-1]
            current_product = grid[current_pos[0]][current_pos[1]]
            if current_product is None: continue

            for neighbor in get_neighbors(current_pos):
                if neighbor in visited:
                    continue
                neighbor_product = grid[neighbor[0]][neighbor[1]]
                if neighbor_product is None: continue

                new_score = heuristic(start_product, neighbor_product)
                new_beam.append((new_score, path + [neighbor]))
                visited.add(neighbor)

        # Select top-k candidates
        new_beam.sort()
        beam = new_beam[:beam_width]

        if not beam:
            break

    # Collect top-N recommendations
    recommendations = []
    for score, path in beam:
        final_pos = path[-1]
        pid = grid[final_pos[0]][final_pos[1]]
        if pid and pid != start_product:
            recommendations.append(pid)

    return recommendations
#----------------------
from sklearn.metrics.pairwise import cosine_similarity

def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def calculate_similarity(prod1, prod2):
    emb1 = get_bert_embedding(prod1['about_product'])
    emb2 = get_bert_embedding(prod2['about_product'])
    return cosine_similarity([emb1], [emb2])[0][0]
#----------------------
start_position = (3, 2)  # starting product cell
top_recommendations = beam_search(grid, start_position, products_dict, beam_width=5, max_depth=8)
print(top_recommendations)
