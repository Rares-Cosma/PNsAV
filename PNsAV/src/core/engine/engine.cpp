#include "engine.h"

void Engine::add_atom(const Atom& atom) {
    atoms.push_back(atom);
}

void Engine::add_rule(const Rule& rule) {
    rules.push_back(rule);
}

void Engine::add_argument(const Argument& argument) {
    arguments.push_back(argument);
}

void Engine::add_attack(const Attack& attack) {
    attacks.push_back(attack);
}

