import nda

def main():
    my_regex = ["(((a,b)|,(a,d)|)&)*",
                "((a,b)|,a)|",
                "([0-9])+"]
    
    test_nfa = nda.NondeterministicFiniteAutomata(my_regex[2])

    nda.fill_symbols_transition(test_nfa)
    nda.remove_empty_transitions(test_nfa)

    #test_nfa.print_transitions()

    test_dfa = nda.DeterministicFiniteAutomata(test_nfa)

    test_dfa.print_automata()

if __name__ == "__main__":
    main()