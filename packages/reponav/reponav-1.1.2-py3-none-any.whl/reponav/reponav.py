def get_struct(repo): # pass username/repo or https://github.com/username/repo
    from github import Github
    import re

    if re.match(r"https?://github.com/(.*)/(.*)", repo):
        repo = re.match(r"https?://github.com/(.*)/(.*)", repo).group(1) + "/" + re.match(r"https?://github.com/(.*)/(.*)", repo).group(2)

    g = Github()
    repo = g.get_repo(repo)
    print(f"Repository: {repo.full_name}\n")
    contents = repo.get_contents("")

    print_contents(repo, contents, 0)

def print_contents(repo, contents, indent_level=0):
    for content in contents:
        if content.type == "dir":
            print("  " * indent_level + f"📁 {content.name}")
            sub_contents = repo.get_contents(content.path)
            print_contents(repo, sub_contents, indent_level + 1)
        else:
            print("  " * indent_level + f"📄 {content.name}")