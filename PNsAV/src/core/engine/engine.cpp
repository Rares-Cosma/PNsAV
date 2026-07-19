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

void Engine::build_attack_map() {
    for (const auto& attack : attacks) {
        attack_index[attack.attacker].push_back(attack.target);
        inv_attack_index[attack.target].push_back(attack.attacker);
    }
}

void Engine::build_argumentadj_vector() {
    for (const auto& arg : arguments) {
        ArgumentAdj arg_adj;
        arg_adj.id = arg.id;
        arg_adj.conclusion = arg.conclusion;
        arg_adj.top_rule = arg.top_rule;
        arg_adj.sub_arguments = arg.sub_arguments;
        arg_adj.type = arg.type;
        arg_adj.strength = arg.strength;

        if (attack_index.count(arg.id)) {
            arg_adj.adj = attack_index[arg.id];
        }

        argumentadj.push_back(arg_adj);
    }
}

std::vector<Argument> Engine::compute_cycles() {
    int n = argumentadj.size();
    std::vector<bool> visited(n, false);
    std::vector<bool> recStack(n, false);

    std::unordered_map<std::string, int> id_to_index;
    for (int i = 0; i < n; i++) {
        id_to_index[argumentadj[i].id] = i;
    }

    for (int i = 0; i < n; i++) {
        if (!visited[i] && is_cycle(visited, recStack, i, argumentadj, id_to_index)) {
            std::vector<Argument> cycle_args;
            
            for (int j = 0; j < n; j++) {
                if (recStack[j]) {
                    cycle_args.push_back(arguments[j]); 
                }
            }
            return cycle_args;
        }
    }

    return {};
}

void Engine::compute_argument_strengths() {
    for (auto& arg : arguments) {
        if (arg.type=="atomic") {
            auto it = std::find_if(atoms.begin(), atoms.end(), [&arg](const Atom& atom) {
                return atom.id == arg.conclusion;
            });
            if (it != atoms.end()) {
                arg.strength = it->strength;
            }
        } else {
            double top_rule_strength = 0.0;
            auto it = std::find_if(rules.begin(), rules.end(), [&arg](const Rule& rule) {
                return rule.id == arg.top_rule.value_or("");
            });
            if (it != rules.end()) {
                top_rule_strength = it->strength;
            }
            double min_subarg_strength = 1.0;
            for (const auto& sub_arg_id : arg.sub_arguments) {
                auto sub_it = std::find_if(arguments.begin(), arguments.end(), [&sub_arg_id](const Argument& sub_arg) {
                    return sub_arg.id == sub_arg_id;
                });
                if (sub_it != arguments.end()) {
                    min_subarg_strength = std::min(min_subarg_strength, sub_it->strength);
                }
            }
            arg.strength = top_rule_strength * min_subarg_strength;
        }
        int_str[arg.id] = arg.strength;
    }
}

int Engine::propagate_strengths(double kappa, int iter, float epsilon){
    std::unordered_map<std::string, double> new_strength;
    if (iter>0) {
        for (int i = 0; i < iter; i++){
            for (auto& arg: arguments) {
                double alpha = 0.0;
                if (inv_attack_index.count(arg.id)) {
                    for (auto& att_arg: inv_attack_index[arg.id]) {
                        auto it = std::find_if(arguments.begin(), arguments.end(), [&att_arg](const Argument& index_arg) {
                            return index_arg.id == att_arg;
                        });
                        if (it != arguments.end()) {
                            alpha -= it->strength;
                        }
                    }
                }
                new_strength[arg.id] = std::clamp(int_str[arg.id] + kappa * std::tanh(alpha), 0.0, 1.0);
            }
            for (auto& arg : arguments) {
                arg.strength = new_strength[arg.id];
            }
        }
        return iter;
    } else {
        int safe_cap = 100000;
        float max_move = epsilon;
        while (max_move >= epsilon && safe_cap-- > 0) {
            max_move = 0.0;
            for (auto& arg: arguments) {
                double alpha = 0.0;
                if (inv_attack_index.count(arg.id)) {
                    for (auto& att_arg: inv_attack_index[arg.id]) {
                        auto it = std::find_if(arguments.begin(), arguments.end(), [&att_arg](const Argument& index_arg) {
                            return index_arg.id == att_arg;
                        });
                        if (it != arguments.end()) {
                            alpha -= it->strength;
                        }
                    }
                }
                float move = std::abs(arg.strength - (int_str[arg.id] + kappa * std::tanh(alpha)));
                if (move > max_move) max_move = move;
                new_strength[arg.id] = std::clamp(int_str[arg.id] + kappa * std::tanh(alpha), 0.0, 1.0);
            }
            for (auto& arg : arguments) {
                arg.strength = new_strength[arg.id];
            }
        }
        return 10000-safe_cap;
    }
}
