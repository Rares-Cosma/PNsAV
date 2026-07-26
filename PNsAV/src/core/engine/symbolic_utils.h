#pragma once
#include "data.h"

bool is_cycle(std::vector<bool>& visited, std::vector<bool>& recStack, int idx, 
              std::vector<ArgumentAdj>& arg_adj, const std::unordered_map<std::string, int>& id_to_index, 
              std::vector<int>& parent, int& cycle_end);