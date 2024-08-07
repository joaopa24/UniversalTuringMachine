from automata.fa.nfa import NFA

my_nfa = NFA(
    states={"q0", "q1", "q2"},
    input_symbols={"a", "b"},
    transitions={
        "q0": {"a": {"q1"}},
        "q1": {"a": {"q1"}, "": {"q2"}},
        "q2": {"b": {"q0"}},
    },
    initial_state="q0",
    final_states={"q1"},
)

my_nfa.show_diagram(my_nfa)