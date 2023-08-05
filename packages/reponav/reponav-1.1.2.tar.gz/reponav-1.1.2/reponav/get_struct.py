from github import Github
import re
from . import print_contents

def get_struct(repo): # pass username/repo or https://github.com/username/repo

    if re.match(r"https?://github.com/(.*)/(.*)", repo):
        repo = re.match(r"https?://github.com/(.*)/(.*)", repo).group(1) + "/" + re.match(r"https?://github.com/(.*)/(.*)", repo).group(2)

    g = Github()
    repo = g.get_repo(repo)
    print(f"Repository: {repo.full_name}\n")
    contents = repo.get_contents("")

    print_contents.print_contents(repo, contents, 0)
