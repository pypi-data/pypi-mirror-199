# AI Header Generator

AI Header Generator is a Python package that generates headers for your code files using OpenAI's GPT-4. It supports various file types and can be easily customized via a configuration file.


## Software Requirements
- Python 3.8 or higher
- Pip (package installer for Python)
- OpenAI API Key
- Git




## Installation Instructions
* Clone the repository to your local machine: git clone https://github.com/your-username/your-repo.git
* Navigate to the project directory: cd ai-generated-headers
* Create a virtual environment: python -m venv venv
* Activate the virtual environment: source venv/bin/activate (for Unix-based systems) or venv\Scripts\activate (for Windows)
* Install the project dependencies: pip install -r requirements.txt
* Copy the config.ini.sample file to config.ini: cp config.ini.sample config.ini
* Open config.ini and add your OpenAI API Key.
* You're ready to go!

## Usage
To generate headers for your code files, run:

```bash
ai-header-generator
```

To generate a README file based on the generated headers, use the --readme option:

```bash
ai-header-generator --readme
```

To use a custom configuration file, use the --config option:

```bash
ai-header-generator --config path/to/your/config.ini
```

## Configuration
The config.ini file contains the following configuration options:

- api_key: Your OpenAI API key.
folder_path: The path to the folder containing the code files to be analyzed.
- analysis_file_extension: The file extension of the code files to be analyzed (e.g., .sql).
- template_file: The path to the JSON file containing the template for generating headers.

Modify these options to customize the behavior of the AI Header Generator.