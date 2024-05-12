import nda

def main():
    my_regex = ["(((alpha,beta)|,(alpha,Empty)|)&)*",
                "((alpha,beta)|,alpha)|"]
    
    test_nda = nda.non_deterministic_automata(my_regex[1])

    test_nda.print_transitions()

if __name__ == "__main__":
    my_dict = {
        "0": {
            "a" : [1,2,3],
            "alpha" : [4,5,6]
        },
        "1": {
            "b" : [7,8,9]
        }
    }

    if "0" in my_dict:
        print("Its in the dict")

    main()