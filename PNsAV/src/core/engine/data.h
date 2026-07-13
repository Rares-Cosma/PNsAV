#pragma once
#include <string>
#include <vector>
#include <optional>
#include <unordered_map>
#include <cmath>

struct Atom {
    std::string id;
    std::string text;
    std::string kb_type;
    std::string source_quote;
    double strength;
};

struct Rule {
    std::string id;
    std::string conclusion;
    std::vector<std::string> premises;
    std::string type;
    double strength;
};

struct Argument {
    std::string id;
    std::string conclusion;
    std::optional<std::string> top_rule;
    std::vector<std::string> sub_arguments;
    std::string type;
    double strength;
};

struct ArgumentAdj {
    std::string id;
    std::string conclusion;
    std::optional<std::string> top_rule;
    std::vector<std::string> sub_arguments;
    std::string type;
    double strength;
    std::vector<std::string> adj;
};

struct Attack {
    std::string attacker;
    std::string target;
    std::string type;
};