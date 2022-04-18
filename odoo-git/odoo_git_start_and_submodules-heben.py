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

REPOS_MASTER = [
    ## Moldeo Interactive
    {
        "name": "ctmil/account_debt_management",
        "url": "https://github.com/ctmil/account_debt_management.git",
    },
]

REPOS = [
    ###########
    # Generic Repositories
    ###########
    ## CybroOdoo
    {
        "name": "CybroOdoo/CybroAddons",
        "url": "https://github.com/CybroOdoo/CybroAddons.git",
    },
    ## Calyx Servicios
    {
        "name": "calyx-servicios/account-analytic",
        "url": "https://github.com/calyx-servicios/account-analytic.git",
    },
    {
        "name": "calyx-servicios/account-financial-tools",
        "url": "https://github.com/calyx-servicios/account-financial-tools.git",
    },
    {
        "name": "calyx-servicios/l10n-cl",
        "url": "https://github.com/calyx-servicios/l10n-cl.git",
    },
    {
        "name": "calyx-servicios/third-party-apps",
        "url": "https://github.com/calyx-servicios/third-party-apps.git",
    },
    {
        "name": "calyx-servicios/third-party-paid",
        "url": "https://github.com/calyx-servicios/third-party-paid.git",
    },
    ## Moldeo Interactive
    {
        "name": "ctmil/meli_oerp",
        "url": "https://github.com/ctmil/meli_oerp.git",
    },
    {
        "name": "ctmil/payment_mercadopago",
        "url": "https://github.com/ctmil/payment_mercadopago.git",
    },
    ## Jorge Obiols
    {
        "name": "jobiols/odoo-addons",
        "url": "https://github.com/jobiols/odoo-addons.git",
    },
    ## ADHOC
    {
        "name": "ingadhoc/account-financial-tools",
        "url": "https://github.com/ingadhoc/account-financial-tools.git",
    },
    {
        "name": "ingadhoc/account-invoicing",
        "url": "https://github.com/ingadhoc/account-invoicing.git",
    },
    {
        "name": "ingadhoc/account-payment",
        "url": "https://github.com/ingadhoc/account-payment.git",
    },
    {
        "name": "ingadhoc/aeroo_reports",
        "url": "https://github.com/ingadhoc/aeroo_reports.git",
    },
    {
        "name": "ingadhoc/argentina-sale",
        "url": "https://github.com/ingadhoc/argentina-sale.git",
    },
    {
        "name": "ingadhoc/odoo-argentina",
        "url": "https://github.com/ingadhoc/odoo-argentina.git",
    },
    {
        "name": "ingadhoc/odoo-argentina-ce",
        "url": "https://github.com/ingadhoc/odoo-argentina-ce.git",
    },
    {
        "name": "ingadhoc/product",
        "url": "https://github.com/ingadhoc/product.git",
    },
    {
        "name": "ingadhoc/sale",
        "url": "https://github.com/ingadhoc/sale.git",
    },
    {
        "name": "ingadhoc/stock",
        "url": "https://github.com/ingadhoc/stock.git",
    },
    {
        "name": "ingadhoc/website",
        "url": "https://github.com/ingadhoc/website.git",
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
        "name": "OCA/commission",
        "url": "https://github.com/OCA/commission.git",
    },
    {
        "name": "OCA/contract",
        "url": "https://github.com/OCA/contract.git",
    },
    {
        "name": "OCA/hr-expense",
        "url": "https://github.com/OCA/hr-expense.git",
    },
    {
        "name": "OCA/mis-builder",
        "url": "https://github.com/OCA/mis-builder.git",
    },
    {
        "name": "OCA/partner-contact",
        "url": "https://github.com/OCA/partner-contact.git",
    },
    {
        "name": "OCA/product-variant",
        "url": "https://github.com/OCA/product-variant.git",
    },
    {
        "name": "OCA/reporting-engine",
        "url": "https://github.com/OCA/reporting-engine.git",
    },
    {
        "name": "OCA/sale-workflow",
        "url": "https://github.com/OCA/sale-workflow.git",
    },
    {
        "name": "OCA/server-auth",
        "url": "https://github.com/OCA/server-auth.git",
    },
    {
        "name": "OCA/server-tools",
        "url": "https://github.com/OCA/server-tools.git",
    },
    {
        "name": "OCA/server-ux",
        "url": "https://github.com/OCA/server-ux.git",
    },
    {
        "name": "OCA/web",
        "url": "https://github.com/OCA/web.git",
    },
    ## Gabriela Rivero
    {
        "name": "regaby/odoo-custom",
        "url": "https://github.com/regaby/odoo-custom.git",
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
    for submodule in REPOS_MASTER:
        print(f"Adding submodule {submodule['name']}.")
        Submodule.add(
            repo,
            submodule["name"],
            os.path.join(repo_dir, f"submodules/{submodule['name']}"),
            submodule["url"],
            "master",
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
    for submodule in REPOS_MASTER:
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
                "master",
                depth=1,
            )
    try:
        repo.git.commit("-m", "[UPD] Submodules.")
    except GitCommandError as e:
        print(e)
        print("[ERROR] Could not commit. No changes to commit.")

print(f"Checkout submodules to {ODOO_VERSION}.")
for sub in repo.submodules:
    sub.module().git.checkout(sub.branch_name)

print("Done.")
