import pytest

from ai_header_generator.header_generator import MetaGenerator
import argparse

@pytest.mark.parametrize("test_input, expected_output", [

    ({"config": "config.ini", "readme": False}, 0),

    ({"config": "config.ini", "readme": True}, 1)

])

def test_main(test_input, expected_output):

    args = argparse.Namespace(**test_input)

    generator = MetaGenerator(config_file=args.config)

    generator.process_files()


    if args.readme:
        generator.generate_readme()

        assert len(generator.readme_files) == expected_output