def main(output_path, structure, modules=None):
    if structure == "basic":
        create_basic_structure(output_path)
    elif structure == "intermediate":
        create_intermediate_structure(output_path)
    elif structure == "advanced":
        create_advanced_structure(output_path)
    elif structure == "extended":
        create_extended_structure(output_path)
    elif structure == "modular":
        module_names = modules if modules else ["utils", "services", "models"]
        create_modular_structure(output_path, module_names)
    else:
        print(f"Invalid structure '{structure}'. Choose from 'basic', 'intermediate', 'advanced', 'extended', or 'modular'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a project structure.")
    parser.add_argument("output_path", help="The desired output path for the project structure.")
    parser.add_argument("structure", help="The project structure to create: basic, intermediate, advanced, extended, or modular.")
    parser.add_argument("-m", "--modules", nargs="*", help="The list of module names for the 'modular' structure option.")

    args = parser.parse_args()

    main(args.output_path, args.structure, args.modules)