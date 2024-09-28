// dijkstra.cpp
#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using namespace std;

// Define a pair type for the priority queue (distance, node)
typedef pair<int, int> pii;

// Function to perform Dijkstra's algorithm
vector<int> dijkstra(int numNodes, vector<vector<pii>> &adjList, int source) {
    // Initialize distances to infinity
    vector<int> distances(numNodes, numeric_limits<int>::max());
    distances[source] = 0;

    // Priority queue to select the node with the smallest distance
    priority_queue<pii, vector<pii>, std::greater<pii>> pq;
    pq.push({0, source});

    while (!pq.empty()) {
        int currentDist = pq.top().first;
        int currentNode = pq.top().second;
        pq.pop();

        // If the distance is greater than the recorded, skip
        if (currentDist > distances[currentNode])
            continue;

        // Iterate over neighbors
        for (auto &edge : adjList[currentNode]) {
            int neighbor = edge.second;
            int weight = edge.first;

            // If a shorter path is found
            if (currentDist + weight < distances[neighbor]) {
                distances[neighbor] = currentDist + weight;
                pq.push({distances[neighbor], neighbor});
            }
        }
    }

    return distances;
}

int main() {
    // Number of nodes in the graph
    int numNodes = 5;

    // Adjacency list where each pair is (weight, neighbor)
    vector<vector<pii>> adjList(numNodes, vector<pii>());

    // Example graph
    // Node 0 connected to Node 1 (weight 10) and Node 4 (weight 3)
    adjList[0].emplace_back(10, 1);
    adjList[0].emplace_back(3, 4);

    // Node 1 connected to Node 2 (weight 2)
    adjList[1].emplace_back(2, 2);
    adjList[1].emplace_back(1, 4);

    // Node 2 connected to Node 3 (weight 9)
    adjList[2].emplace_back(9, 3);

    // Node 3 connected to Node 2 (weight 7) and Node 4 (weight 2)
    adjList[3].emplace_back(7, 2);
    adjList[3].emplace_back(2, 4);

    // Node 4 connected to Node 1 (weight 4) and Node 3 (weight 8)
    adjList[4].emplace_back(4, 1);
    adjList[4].emplace_back(8, 3);

    int source = 0; // Starting node

    // Perform Dijkstra's algorithm
    vector<int> distances = dijkstra(numNodes, adjList, source);

    // Output the shortest distances from source
    cout << "Shortest distances from node " << source << ":\n";
    for (int i = 0; i < numNodes; ++i) {
        if (distances[i] == numeric_limits<int>::max())
            cout << "Node " << i << ": Unreachable\n";
        else
            cout << "Node " << i << ": " << distances[i] << "\n";
    }

    return 0;
}
