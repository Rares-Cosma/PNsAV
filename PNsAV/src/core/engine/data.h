#pragma once
#include <string>
#include <vector>
#include <optional>
#include <unordered_map>

struct Atom {
    std::string id;
    std::string text;
    std::string kb_type;
    std::string source_quote;
};

struct Rule {
    std::string id;
    std::string conclusion;
    std::vector<std::string> premises;
    std::string type;
};

struct Argument {
    std::string id;
    std::string conclusion;
    std::optional<std::string> top_rule;
    std::vector<std::string> sub_arguments;
    std::string type;
};

struct Attack {
    std::string attacker;
    std::string target;
    std::string type;
};