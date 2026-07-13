#pragma once
#include <algorithm>
#include "symbolic_utils.h"

class Engine {
    public:
        std::vector<Attack> attacks;
        std::vector<Atom> atoms;
        std::vector<Rule> rules;
        std::vector<Argument> arguments;
        std::vector<ArgumentAdj> argumentadj;
        std::vector<std::string> logs;
        std::unordered_map<std::string, double> int_str;
        std::unordered_map<std::string, std::vector<std::string>> attack_index;
        std::unordered_map<std::string, std::vector<std::string>> inv_attack_index;

        void add_atom(const Atom& atom);
        void add_rule(const Rule& rule);
        void add_argument(const Argument& argument);
        void add_attack(const Attack& attack);
        void build_attack_map();
        void build_argumentadj_vector();

        std::vector<Argument> compute_cycles();
        void compute_argument_strengths();
        void propagate_strengths(double kappa, int iter, float epsilon);
};

