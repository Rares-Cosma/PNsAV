#include "symbolic_utils.h"

bool find_cycles_dfs(
    const std::string& start,
    const std::string& current,
    std::unordered_map<std::string, std::vector<std::string>>& adj,
    std::unordered_set<std::string>& blocked,
    std::vector<std::string>& path,
    std::vector<std::vector<std::string>>& cycles
) {
    bool found_cycle = false;
    path.push_back(current);
    blocked.insert(current);

    if (adj.count(current)) {
        for (const std::string& neighbor : adj[current]) {
            if (neighbor == start) {
                cycles.push_back(path);
                found_cycle = true;
            } else if (neighbor > start && blocked.find(neighbor) == blocked.end()) {
                if (find_cycles_dfs(start, neighbor, adj, blocked, path, cycles)) {
                    found_cycle = true;
                }
            }
        }
    }

    path.pop_back();
    blocked.erase(current);
    
    return found_cycle;
}