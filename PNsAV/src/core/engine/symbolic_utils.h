#pragma once
#include <unordered_set>
#include "data.h"

bool find_cycles_dfs(
    const std::string& start,
    const std::string& current,
    std::unordered_map<std::string, std::vector<std::string>>& adj,
    std::unordered_set<std::string>& blocked,
    std::vector<std::string>& path,
    std::vector<std::vector<std::string>>& cycles
);