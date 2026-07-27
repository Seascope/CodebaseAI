import os
import shutil
import tempfile
from git import Repo
from pathlib import Path

def is_binary(file_path):
    # A simple heuristic to check if a file is binary
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read(1024)
            return False
    except UnicodeDecodeError:
        return True

def clone_and_parse_repo(repo_url: str):
    repos_dir = Path("repos")
    repos_dir.mkdir(exist_ok=True)
    
    # Extract repo name from URL
    repo_name = repo_url.rstrip('/').split('/')[-1]
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]
    
    repo_path = repos_dir / repo_name
    
    # Clone repo if it doesn't exist, else pull
    if not repo_path.exists():
        Repo.clone_from(repo_url, repo_path)
    else:
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        
    parsed_files = []
    
    # Walk through the repository and parse files
    for root, dirs, files in os.walk(repo_path):
        # Ignore .git directory
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            file_path = Path(root) / file
            
            # Skip binary files
            if is_binary(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    parsed_files.append({
                        "path": str(file_path.relative_to(repo_path)),
                        "content": content
                    })
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")
                
    return repo_name, parsed_files
