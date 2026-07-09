#pragma once
#include "data.h"

class Engine {
    public:
        std::vector<Attack> attacks;
        std::vector<Atom> atoms;
        std::vector<Rule> rules;
        std::vector<Argument> arguments;

        void add_atom(const Atom& atom);
        void add_rule(const Rule& rule);
        void add_argument(const Argument& argument);
        void add_attack(const Attack& attack);
};