import nda

def main():
    my_regex = ["(((alpha,beta)|,(alpha,delta)|)&)*",
                "((alpha,beta)|,alpha)|"]
    
    test_nfa = nda.NondeterministicFiniteAutomata(my_regex[0])

    nda.fill_symbols_transition(test_nfa)
    nda.remove_empty_transitions(test_nfa)

    #test_nfa.print_transitions()

    test_dfa = nda.DeterministicFiniteAutomata(test_nfa)

    test_dfa.print_automata()

if __name__ == "__main__":
    main()