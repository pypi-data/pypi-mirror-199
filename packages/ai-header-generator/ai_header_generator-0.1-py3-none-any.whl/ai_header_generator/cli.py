import argparse
from .header_generator import MetaGenerator


def main():
    """ [insert]
    """    
    parser = argparse.ArgumentParser(description="AI-based header generator for code files.")

    parser.add_argument("--config", help="Path to the configuration file.", default="config.ini")

    parser.add_argument("--readme", help="Generate a README file based on the generated headers.", action="store_true")

    parser.add_argument("--template", help="JSON template query.")
    
    parser.add_argument("--file", help="Path to a specific code file to generate a header for.")
    
    
    args = parser.parse_args()

    generator = MetaGenerator(config_file=args.config)
    
    # Use the specified template if provided, otherwise use the default template
    try:
        if args.template:
            generator._read_template(file=args.template)
    except Exception as e:
        print("Error occurred while reading template file: ", e)
        exit(1)
    if args.file:
        generator.process_file(args.file)
    else:
        generator.process_files()
        
    if args.readme:
        generator.generate_readme()


if __name__ == "__main__":
    main()