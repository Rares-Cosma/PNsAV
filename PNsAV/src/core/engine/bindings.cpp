#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "engine.h"
namespace py = pybind11;

PYBIND11_MODULE(ArgEngine, m) {
    py::class_<Atom>(m, "Atom")
        .def(py::init<>())
        .def_readwrite("id", &Atom::id)
        .def_readwrite("text", &Atom::text)
        .def_readwrite("kb_type", &Atom::kb_type)
        .def_readwrite("source_quote", &Atom::source_quote)
        .def_readwrite("strength", &Atom::strength);

    py::class_<Rule>(m, "Rule")
        .def(py::init<>())
        .def_readwrite("id", &Rule::id)
        .def_readwrite("conclusion", &Rule::conclusion)
        .def_readwrite("premises", &Rule::premises)
        .def_readwrite("type", &Rule::type)
        .def_readwrite("strength", &Rule::strength);

    py::class_<Argument>(m, "Argument")
        .def(py::init<>())
        .def_readwrite("id", &Argument::id)
        .def_readwrite("conclusion", &Argument::conclusion)
        .def_readwrite("top_rule", &Argument::top_rule)
        .def_readwrite("sub_arguments", &Argument::sub_arguments)
        .def_readwrite("type", &Argument::type)
        .def_readwrite("strength", &Argument::strength);

    py::class_<ArgumentAdj>(m, "ArgumentAdj")
        .def(py::init<>())
        .def_readwrite("id", &ArgumentAdj::id)
        .def_readwrite("conclusion", &ArgumentAdj::conclusion)
        .def_readwrite("top_rule", &ArgumentAdj::top_rule)
        .def_readwrite("sub_arguments", &ArgumentAdj::sub_arguments)
        .def_readwrite("type", &ArgumentAdj::type)
        .def_readwrite("strength", &ArgumentAdj::strength)
        .def_readwrite("adj", &ArgumentAdj::adj);

    py::class_<Attack>(m, "Attack")
        .def(py::init<>())
        .def_readwrite("attacker", &Attack::attacker)
        .def_readwrite("target", &Attack::target)
        .def_readwrite("type", &Attack::type);

    py::class_<Engine>(m, "Engine")
        .def(py::init<>())
        .def("add_atom", &Engine::add_atom)
        .def("add_rule", &Engine::add_rule)
        .def("add_argument", &Engine::add_argument)
        .def("add_attack", &Engine::add_attack)
        .def("build_argumentadj_vector", &Engine::build_argumentadj_vector)
        .def("compute_cycles", &Engine::compute_cycles)
        .def("compute_argument_strengths", &Engine::compute_argument_strengths)
        .def_readwrite("atoms", &Engine::atoms)
        .def_readwrite("rules", &Engine::rules)
        .def_readwrite("arguments", &Engine::arguments)
        .def_readwrite("attacks", &Engine::attacks)
        .def_readwrite("argumentadj", &Engine::argumentadj);

}