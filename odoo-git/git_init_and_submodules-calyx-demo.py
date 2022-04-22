# pylint: disable=print-used
import os
import sys

try:
    from git import Repo, Submodule, UpdateProgress
    from git.exc import InvalidGitRepositoryError, GitCommandError
except ImportError as e:
    import subprocess

    # Upgrade Python
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    # Pip packages installer
    subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])
    # Install GitPython
    from git import Repo, Submodule, UpdateProgress
    from git.exc import InvalidGitRepositoryError, GitCommandError

REPOS = [
    ###########
    # Generic Repositories
    ###########
    ## CybroOdoo
    {
        "name": "CybroOdoo/CybroAddons",
        "url": "https://github.com/CybroOdoo/CybroAddons.git",
    },
    ## ADHOC
    {
        "name": "ingadhoc/account-financial-tools",
        "url": "https://github.com/ingadhoc/account-financial-tools.git",
    },
    {
        "name": "ingadhoc/account-payment",
        "url": "https://github.com/ingadhoc/account-payment.git",
    },
    {
        "name": "ingadhoc/odoo-argentina",
        "url": "https://github.com/ingadhoc/odoo-argentina.git",
    },
    {
        "name": "ingadhoc/odoo-argentina-ee",
        "url": "https://github.com/ingadhoc/odoo-argentina-ee.git",
    },
    {
        "name": "ingadhoc/product",
        "url": "https://github.com/ingadhoc/product.git",
    },
]

try:
    ODOO_VERSION = sys.argv[1]
except IndexError:
    print("Please provide the Odoo version as the first argument.")
    sys.exit(1)

repo_dir = os.path.dirname(os.path.abspath(__file__))

try:
    repo = Repo(repo_dir)
except InvalidGitRepositoryError as e:
    repo = False


if repo is False:
    # Init repository
    repo = Repo.init(repo_dir)
    repo.git.branch("-m", ODOO_VERSION)

    # Add submodules
    for submodule in REPOS:
        print(f"Adding submodule {submodule['name']}.")
        Submodule.add(
            repo,
            submodule["name"],
            os.path.join(repo_dir, f"submodules/{submodule['name']}"),
            submodule["url"],
            ODOO_VERSION,
            depth=1,
        )
    # try:
    #     repo.git.commit("-m", "[ADD] Submodules.")
    # except GitCommandError as e:
    #     print(e)
    #     print("[ERROR] Could not commit. No changes to commit.")
else:
    # repo.git.checkout(ODOO_VERSION)
    if repo.remotes:
        repo.remotes.origin.fetch()
        repo.remotes.origin.pull()

    for submodule in REPOS:
        if submodule["name"] in repo.submodules:
            print(f"Updating submodule {submodule['name']}.")
            sm_progress = UpdateProgress()
            submodule = repo.submodule(submodule["name"])
            submodule.update(
                init=True,
                recursive=True,
                progress=sm_progress,
            )
            if sm_progress.error_lines:
                print(sm_progress.error_lines)
                sys.exit(1)
        else:
            print(f"Adding submodule {submodule['name']}.")
            Submodule.add(
                repo,
                submodule["name"],
                os.path.join(repo_dir, f"submodules/{submodule['name']}"),
                submodule["url"],
                ODOO_VERSION,
                depth=1,
            )
    # try:
    #     repo.git.commit("-m", "[UPD] Submodules.")
    # except GitCommandError as e:
    #     print(e)
    #     print("[ERROR] Could not commit. No changes to commit.")

print(f"Checkout submodules to {ODOO_VERSION}.")
for sub in repo.submodules:
    sub.module().git.checkout(ODOO_VERSION)

print("Done.")
