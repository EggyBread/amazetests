import heapq
import sys
from PIL import Image
import time

def AStar(start, goal, neighbor_nodes, dist_between, heuristic_cost_estimate):
    def reconstruct_path(came_from, current_node):
        path = [current_node]
        while current_node in came_from:
            current_node = came_from[current_node]
            path.append(current_node)
        return list(reversed(path))

    g_score = {start: 0}
    f_score = {start: g_score[start] + heuristic_cost_estimate(start, goal)}
    openheap = [(f_score[start], start)]
    openset = {start}
    came_from = dict()

    while openset:
        _, current = heapq.heappop(openheap)
        openset.remove(current)
        if current == goal:
            return reconstruct_path(came_from, goal)
        closedset.add(current)
        for neighbor in neighbor_nodes(current):
            tentative_g_score = (
                g_score[current] + dist_between(current, neighbor)
            )
            if neighbor in closedset and tentative_g_score >= g_score[neighbor]:
                continue
            if neighbor not in openset or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                # TODO: there might be an implementation error:
                # is the heap updated when the f_score of a node is changed? 
                f_score[neighbor] = (
                    g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                )
                if neighbor not in openset:
                    heapq.heappush(openheap, (f_score[neighbor], neighbor))
                    openset.add(neighbor)
    print "no path found :("

def is_blocked(p):
    x,y = p
    pixel = path_pixels[x,y]
    if any(c < 225 for c in pixel):
        return True
def von_neumann_neighbors(p):
    x, y = p
    neighbors = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
    return [p for p in neighbors if not is_blocked(p)]
def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
def squared_euclidean(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

start = (400, 984)
goal = (398, 25)

# invoke: python mazesolver.py <mazefile> <outputfile>[.jpg|.png|etc.]

path_img = Image.open(sys.argv[1])
path_pixels = path_img.load()

closedset = set()

start_time = time.time()
path = AStar(start,
             goal,
             von_neumann_neighbors,
             manhattan,
             manhattan,
             #lambda p1,p2 : 4*manhattan(p1,p2),
             #squared_euclidean,
             )
print time.time() - start_time

for position in closedset:
    x,y = position
    path_pixels[x,y] = (127,127,127)

for position in path:
    x,y = position
    path_pixels[x,y] = (255,0,0) # red

path_img.save(sys.argv[2])