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
        .def_readwrite("source_quote", &Atom::source_quote);

    py::class_<Rule>(m, "Rule")
        .def(py::init<>())
        .def_readwrite("id", &Rule::id)
        .def_readwrite("conclusion", &Rule::conclusion)
        .def_readwrite("premises", &Rule::premises)
        .def_readwrite("type", &Rule::type);

    py::class_<Argument>(m, "Argument")
        .def(py::init<>())
        .def_readwrite("id", &Argument::id)
        .def_readwrite("conclusion", &Argument::conclusion)
        .def_readwrite("top_rule", &Argument::top_rule)
        .def_readwrite("sub_arguments", &Argument::sub_arguments)
        .def_readwrite("type", &Argument::type);

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
        .def_readwrite("atoms", &Engine::atoms)
        .def_readwrite("rules", &Engine::rules)
        .def_readwrite("arguments", &Engine::arguments)
        .def_readwrite("attacks", &Engine::attacks);
}