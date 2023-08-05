def print_contents(repo, contents, indent_level=0):
    for content in contents:
        if content.type == "dir":
            print("  " * indent_level + f"📁 {content.name}")
            sub_contents = repo.get_contents(content.path)
            print_contents(repo, sub_contents, indent_level + 1)
        else:
            print("  " * indent_level + f"📄 {content.name}")