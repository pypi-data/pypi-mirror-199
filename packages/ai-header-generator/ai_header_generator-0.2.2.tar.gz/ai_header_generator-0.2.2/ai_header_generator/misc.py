import os
from collections import defaultdict
import fnmatch
import traceback
import hashlib
import jsonpickle


def read_excludes(topdir, config):
    exclude_dirs = config.get('project', 'exclude_dirs', fallback='').split(', ')
    exclude_files = config.get('project', 'exclude_files', fallback='').split(', ')
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
                if any(fnmatch.fnmatch(name, pattern) for pattern in exclude_files) or any(fnmatch.fnmatch(os.path.basename(name), pattern) for pattern in exclude_dirs):
                    continue
                path = os.path.join(folder, name)
                if os.path.islink(path) or os.path.isdir(path):
                    d[name] = {}
                    walkdir(path, d[name])
                else:
                    d[name] = None
            except Exception as e:
                print(f"Error: {e}")
                print(traceback.format_exc())
                
    tree = defaultdict(dict)
    walkdir(topdir, tree)
    with open("project_tree.hex", "wb") as f:
        f.write(jsonpickle.encode(tree).encode())
    return tree