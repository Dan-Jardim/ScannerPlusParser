import nda

def main():
    test_nda = nda.non_deterministic_automata("(((a,b)+,(a,E)+).)*")

    test_nda.print_transitions()

if __name__ == "__main__":
    main()