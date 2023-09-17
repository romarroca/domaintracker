def domain_mutations(domain):
    mutations = set()
    main_part = domain  
    
    for i in range(len(main_part)):
        for c in "aeiou":
            mutated = main_part[:i] + c + main_part[i+1:]
            mutations.add(mutated)
            
    for i in range(len(main_part)):
        mutated = main_part[:i] + main_part[i+1:]
        mutations.add(mutated)
        
    for i in range(len(main_part) - 1):
        mutated = list(main_part)
        mutated[i], mutated[i+1] = mutated[i+1], mutated[i]
        mutations.add(''.join(mutated))

    for i in range(len(main_part) + 1):
        for c in "aeiou":
            mutated = main_part[:i] + c + main_part[i:]
            mutations.add(mutated)

    return mutations

def generate_homographs(word):
    homograph_map = {
        'e': ['е'],
        't': ['т'], 
        's': ['ѕ']
    }
    generated_words = [word]

    for char, replacements in homograph_map.items():
        new_words = []
        for generated in generated_words:
            if char in generated:
                for replacement in replacements:
                    new_words.append(generated.replace(char, replacement))
        generated_words.extend(new_words)

    return generated_words

def generate_domain_list(keyword):
    print("Choose the TLDs list:")
    print("1: Common TLDs")
    print("2: Comprehensive TLDs")
    
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        tld_file = 'tlds-common.txt'
    elif choice == '2':
        tld_file = 'tlds-comprehensive-list.txt'
    else:
        print("Invalid choice. Using common TLDs by default.")
        tld_file = 'tlds-common.txt'

    tlds = []
    suffixes = ["", "-us", "-uk", "-eu", "-asia"]
    numbered = [f"{keyword}{str(i).zfill(2)}" for i in range(1, 11)]
    output_file = f"{keyword}_generated_domains.txt"

    with open(tld_file, 'r') as f:
        tlds = f.read().splitlines()

    with open(output_file, 'w', encoding='utf-8') as f:
        for tld in tlds:
            for base_name in [keyword] + numbered:
                mutations = domain_mutations(base_name)
                combined = set(list(mutations))
                for variant in combined:
                    for suffix in suffixes:
                        generated_domain = f"{variant}{suffix}.{tld}"
                        f.write(f"{generated_domain}\n")

    print(f"Generated domain list saved in {output_file}")

if __name__ == "__main__":
    keyword = input("Enter the keyword to generate domain list: ")
    generate_domain_list(keyword)
