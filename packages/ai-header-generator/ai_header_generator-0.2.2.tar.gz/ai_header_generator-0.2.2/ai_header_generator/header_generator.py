import openai
import os
import json
import glob
import configparser
from .misc import generate_tree
import jsonpickle
from .misc import read_excludes
from tqdm import tqdm
import fnmatch
from pathlib import Path

class MetaGenerator:
    """_summary_
    """    
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = self.config.get("openai", "api_key")
        self.project_folder = self.config.get("project", "folder_path")
        self.template_file = self.config.get("project", "template_file")
        # self.ignore_patterns = self.config.get("project", "ignore_patterns").split(",")
        openai.api_key = self.api_key
        self._read_template()

    def _read_template(self, file=None):
        """_summary_

        Returns:
            _type_: _description_
        """
        if file:
            self.template_file = file   
        
        with open(self.template_file, "r") as f:
            template = json.load(f)
        self.analysis_file_extension = template.get("analysis_file_extension")
        if json_structure := template.get("json_structure"):
            json_structure_str = json.dumps(json_structure, indent=2)
            template["prompt"] = template["prompt"].replace("$json", json_structure_str)
        self.template = template

    def generate_meta(self, prompt):
        """_summary_

        Args:
            prompt (_type_): _description_

        Returns:
            _type_: _description_
        """        
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                stop=["\\n"],
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response.choices[0].text
        except Exception as e:
            print("Error: Could not generate header.")
            print(e)
            return None

    def process_file(self, file):
        """_summary_

        Args:
            file (_type_): _description_

        Returns:
            _type_: _description_
        """        
        try:
            with open(file, "r", encoding='utf-8') as f:
                code = f.read()
        
        except UnicodeDecodeError:
            print(f"Error: Could not decode following file: {file}")
            return 0
        
        except IOError:
            print(f"Error: Could not read code file: {file}")
            return 0
        
        if len(code) > 2000:
            code = code[:1900]
            # TODO: find way to process a big file
        
        project_tree = generate_tree(self.project_folder, self.config)
        
        prompt = self.template["prompt"].format(code=code, filename=os.path.basename(file), project_tree=project_tree)
    
        print("-"*100)
        print("- prompt: " + prompt)
    
        if header := self.generate_meta(prompt):
            header_postfix = self.template.get("header_postfix", "_header.txt")
            header_filename = f"{os.path.splitext(file)[0]}{header_postfix}"
            
            print("-"*100)
            print("- meta: " + header_filename)
            print(header)
            
            try:
                with open(header_filename, "w", encoding='utf-8') as f:
                    f.write(header)
            except IOError:
                print(f"Error: Could not write header file: {header_filename}")
                return 0
        return 1

    def _skip_file(self, file):
        """_summary_

        Args:
            file (_type_): _description_

        Returns:
            _type_: _description_
        """        
        # Skip excluded directories
        # TODO: Handle skipping files in a more graceful way
        skip = False
        for pattern in self.exclude_dirs:
            if any(fnmatch.fnmatch(part, pattern) for part in Path(file).resolve().relative_to(self.project_folder).parts for pattern in self.exclude_dirs):
                skip = True
            if pattern in file:
                skip = True
        return skip

    def process_files(self):
        """_summary_
        """        
        analysis_files = glob.glob(f"{self.project_folder}/**/*{self.analysis_file_extension}", recursive=True)
        
        (self.exclude_files, self.exclude_dirs) = read_excludes(".", self.config)
        
        # exclude files
        analysis_files = [file for file in analysis_files if not any(fnmatch.fnmatch(file, pattern) for pattern in self.exclude_files)]
        
        # skip/exclude files in excluded folder
        analysis_files = [file for file in analysis_files if not self._skip_file(file)]
        
        # Initialize progress bar
        pbar = tqdm(total=len(analysis_files), desc="Processing Files")
        
        for file in analysis_files:
            
            print("-"*100)
            print(f" -- file: {file}")
            

            if self.process_file(file) == 0:
                continue
            
            pbar.update(1)

    def generate_readme(self, output_file="README.md"):
        """_summary_

        Args:
            output_file (str, optional): _description_. Defaults to "README.md".
        """        
        header_files = glob.glob(f"{self.project_folder}/**/*_header.txt", recursive=True)
        readme_content = []
        for file in header_files:
            try:
                with open(file, "r") as f:
                    content = f.read()
            except IOError:
                print(f"Error: Could not read header file: {file}")
                continue
            readme_content.append(content)
        readme_text = "\n\n".join(readme_content)
        prompt = self.template["readme_prompt"].format(headers=readme_text)
        if readme_generated := self.generate_meta(prompt):
            try:
                with open(output_file, "w") as f:
                    f.write(readme_generated)
            except IOError:
                print(f"Error: Could not write README file: {output_file}")