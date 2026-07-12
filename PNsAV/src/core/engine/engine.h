#pragma once
#include <algorithm>
#include "symbolic_utils.h"
#include "math_utils.h"

class Engine {
    public:
        std::vector<Attack> attacks;
        std::vector<Atom> atoms;
        std::vector<Rule> rules;
        std::vector<Argument> arguments;
        std::vector<ArgumentAdj> argumentadj;

        void add_atom(const Atom& atom);
        void add_rule(const Rule& rule);
        void add_argument(const Argument& argument);
        void add_attack(const Attack& attack);
        void build_argumentadj_vector();

        std::vector<Argument> compute_cycles();
        void compute_argument_strengths();
};

