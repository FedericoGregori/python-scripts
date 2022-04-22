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
    # Odoo CE Chile Localization
    {
        "name": "dansanti/l10n-cl/facturacion_electronica",
        "url": "https://gitlab.com/dansanti/facturacion_electronica.git",
    },
    {
        "name": "dansanti/l10n-cl/l10n_cl_fe",
        "url": "https://gitlab.com/dansanti/l10n_cl_fe.git",
    },
    {
        "name": "dansanti/l10n-cl/l10n_cl_dte_factoring",
        "url": "https://gitlab.com/dansanti/l10n_cl_dte_factoring.git",
    },
    {
        "name": "dansanti/l10n-cl/l10n_cl_dte_point_of_sale",
        "url": "https://gitlab.com/dansanti/l10n_cl_dte_point_of_sale.git",
    },
    {
        "name": "dansanti/l10n-cl/l10n_cl_stock_picking",
        "url": "https://gitlab.com/dansanti/l10n_cl_stock_picking.git",
    },
    ###########
    # Generic Repositories
    ###########
    ## Calyx Servicios
    {
        "name": "calyx-servicios/third-party-paid",
        "url": "https://github.com/calyx-servicios/third-party-paid.git",
    },
    ## Cybrosys
    {
        "name": "CybroOdoo/CybroAddons",
        "url": "https://github.com/CybroOdoo/CybroAddons.git",
    },
    ## OCA
    {
        "name": "OCA/account-analytic",
        "url": "https://github.com/OCA/account-analytic.git",
    },
    {
        "name": "OCA/account-financial-reporting",
        "url": "https://github.com/OCA/account-financial-reporting.git",
    },
    {
        "name": "OCA/account-financial-tools",
        "url": "https://github.com/OCA/account-financial-tools.git",
    },
    {
        "name": "OCA/account-reconcile",
        "url": "https://github.com/OCA/account-reconcile.git",
    },
    {
        "name": "OCA/bank-statement-import",
        "url": "https://github.com/OCA/bank-statement-import.git",
    },
    {
        "name": "OCA/contract",
        "url": "https://github.com/OCA/contract.git",
    },
    {
        "name": "OCA/reporting-engine",
        "url": "https://github.com/OCA/reporting-engine.git",
    },
    {
        "name": "OCA/server-ux",
        "url": "https://github.com/OCA/server-ux.git",
    },
    {
        "name": "OCA/web",
        "url": "https://github.com/OCA/web.git",
    },
    ## Yenthe666
    {
        "name": "Yenthe/auto-backup",
        "url": "https://github.com/Yenthe666/auto_backup.git",
    },
]

ODOO_VERSION = sys.argv[1]
if not ODOO_VERSION:
    print("Please provide the Odoo version.")
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
        if submodule["name"] == "dansanti/l10n-cl/facturacion_electronica":
            Submodule.add(
                repo,
                submodule["name"],
                os.path.join(repo_dir, f"submodules/{submodule['name']}"),
                submodule["url"],
                depth=1,
            )
            continue

        Submodule.add(
            repo,
            submodule["name"],
            os.path.join(repo_dir, f"submodules/{submodule['name']}"),
            submodule["url"],
            ODOO_VERSION,
            depth=1,
        )
    try:
        repo.git.commit("-m", "[ADD] Submodules.")
    except GitCommandError as e:
        print(e)
        print("[ERROR] Could not commit. No changes to commit.")
else:
    repo.git.checkout(ODOO_VERSION)
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
    try:
        repo.git.commit("-m", "[UPD] Submodules.")
    except GitCommandError as e:
        print(e)
        print("[ERROR] Could not commit. No changes to commit.")

print(f"Checkout submodules to {ODOO_VERSION}.")
for sub in repo.submodules:
    if sub.name == "dansanti/l10n-cl/facturacion_electronica":
        sub.module().git.checkout("master")
        continue
    sub.module().git.checkout(ODOO_VERSION)

print("Done.")
