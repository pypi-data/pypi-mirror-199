import os
from collections import defaultdict
import fnmatch
import traceback
import hashlib
import jsonpickle

def read_excludes(topdir, config):
    exclude_dirs = config.get('project', 'exclude_dirs', fallback='').split(', ')
    exclude_files = config.get('project', 'exclude_files', fallback='').split(', ')


    # Read ignore patterns from .gitignore file if it exists
    gitignore_path = os.path.join(topdir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_patterns = f.read().splitlines()
        exclude_files += gitignore_patterns
    return (exclude_files, exclude_dirs)

def generate_tree(topdir, config):
    
    tree_file = os.path.join(topdir, ".project_tree.hex")
    
    if os.path.exists(tree_file):
        with open(tree_file, "rb") as f:
            try:
                tree = jsonpickle.decode(f.read())
                return tree
            except:
                os.remove(tree_file)

    def walkdir(folder, d):
        
        (exclude_files, exclude_dirs) = read_excludes(topdir, config)
        
        if os.path.basename(folder) in exclude_dirs:
            return
        for name in os.listdir(folder):
            try:
                if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_files):
                    continue
                if any(fnmatch.fnmatch(os.path.basename(name), pattern) for pattern in exclude_dirs):
                    continue
                
                path = os.path.join(folder, name)
                
                if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_files):
                    continue
                if any(fnmatch.fnmatch(os.path.basename(name), pattern) for pattern in exclude_dirs):
                    continue
                
                if os.path.islink(path):
                    continue
                if os.path.isdir(path):
                    d[name] = {}
                    walkdir(path, d[name])
                else:
                    d[name] = None
                for name in os.listdir(folder):
                    
                    if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_files):
                        continue
                    if any(fnmatch.fnmatch(os.path.basename(name), pattern) for pattern in exclude_dirs):
                        continue
                
                    if name in {'.', '..'}:
                        continue
                    path = os.path.join(folder, name)
                    if os.path.islink(path):
                        continue
                    if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_files):
                        continue
                    if os.path.isdir(path):
                        d[name] = {}
                        walkdir(path, d[name])
                    else:
                        d[name] = None
                    for name in os.listdir(folder):
                    
                        if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_files):
                            continue
                        if any(fnmatch.fnmatch(os.path.basename(name), pattern) for pattern in exclude_dirs):
                            continue
                    
                        path = os.path.join(folder, name)
                        if os.path.isdir(path):
                                walkdir(path, d[name])
                        else:
                            d[name] = None
            except Exception as e:
                print(f"Error: {e}")
                print(traceback.format_exc())
            #     tb = traceback.extract_tb(e.__traceback__)
            #     folders = set(os.path.dirname(frame.filename) for frame in tb)
            #     files = set(frame.filename for frame in tb)
            #     patterns = set()
            #     for folder in folders:
            #         patterns.add(os.path.basename(folder))
            #     for file in files:
            #         patterns.add(os.path.basename(file))
            #     patterns.add(os.path.basename(path))
            #     print(f"Suggested exclude patterns: {','.join(patterns)}")
            #     return

    tree = defaultdict(dict)
    walkdir(topdir, tree)
    
    # write the serialized data to file
    with open("project_tree.hex", "wb") as f:
        f.write(jsonpickle.encode(tree).encode())
        
    return tree