#include "symbolic_utils.h"

bool is_cycle(std::vector<bool>& visited, std::vector<bool>& recStack, int idx, 
              std::vector<ArgumentAdj>& arg_adj, const std::unordered_map<std::string, int>& id_to_index, 
              std::vector<int>& parent, int& cycle_end) {
    if (recStack[idx]) {
        cycle_end = idx;
        return true;  
    }
    if (visited[idx]) return false;

    recStack[idx] = true;
    visited[idx] = true;

    for (const auto& neighbor_id : arg_adj[idx].adj) {
        auto it = id_to_index.find(neighbor_id);
        if (it != id_to_index.end()) {
            int neighbor_idx = it->second;
            parent[neighbor_idx] = idx;
            if (is_cycle(visited, recStack, neighbor_idx, arg_adj, id_to_index, parent, cycle_end)) {
                return true;
            }
        }
    }
    recStack[idx] = false;
    return false;
}