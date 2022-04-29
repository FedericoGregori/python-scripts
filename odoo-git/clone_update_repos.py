# pylint: disable=line-too-long, broad-except
"""
This script downloads repositories in the REPOS dictionary (Odoo addons).

We are clonning shallow copies of the repositories. They are
not meant to be updated.

To unshallow a repository, use:
$ git fetch --unshallow

# Constants to be aware of:
    - REPOS: the list of repositories to be cloned.
    - BASE_DIR: the base directory where the repositories will be cloned.
    - BRANCH: the branch to be used.

# Linux System Requirements (for Odoo Source installation/third party addons in this script):
sudo apt install git python3-pip build-essential wget python3-dev python3-venv python3-wheel libxslt-dev libzip-dev libldap2-dev libsasl2-dev python3-setuptools node-less -y
sudo apt install libjpeg-dev zlib1g-dev libpq-dev swig mupdf libssl-dev libcups2-dev python3-uno -y

Install m2crypto on MacOS:
https://stackoverflow.com/questions/33005354/trouble-installing-m2crypto-with-pip-on-os-x-macos

# Install requirements after cloning:
python3 -m venv venv # Create a virtual environment in case it doesn't exist.
source venv/bin/activate
pip3 install --upgrade pip
pip3 install wheel
cd <MAIN_DIR> # Where MAIN_DIR is the same as the MAIN_DIR used in the script.
for d in */; do cd $d; for dir in */; do cd $dir; if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi; cd ..; done; cd ..; done

# In the requirements install process, you should check if there is any errors.
This depends on the OS and proccessor architecture or system packages dependencies.
In my case (MacOS / M1), I had the following errors:
* ERROR: Failed building wheel for numpy

Be sure to use the same virtualenv when running Odoo.

Author: Federico Gregori <

"""

import os
import sys

################################################################
#                         Constants                            #

REPOS = [
    # CybroOdoo
    "https://github.com/CybroOdoo/CybroAddons.git",
    # FedericoGregori
    "https://github.com/FedericoGregori/account_debt_management.git",
    "https://github.com/FedericoGregori/meli_oerp.git",
    "https://github.com/FedericoGregori/payment_mercadopago.git",
    # Calyx-servicios
    "https://github.com/calyx-servicios/account-analytic.git",
    "https://github.com/calyx-servicios/account-financial-tools.git",
    "https://github.com/calyx-servicios/custom-heben.git",
    "https://github.com/calyx-servicios/iva-digital.git",
    "https://github.com/calyx-servicios/l10n-cl.git",
    "https://github.com/calyx-servicios/l10n-pe.git",
    "https://github.com/calyx-servicios/odoo13-test.git",
    "https://github.com/calyx-servicios/project.git",
    "https://github.com/calyx-servicios/third-party-apps.git",
    "https://github.com/calyx-servicios/third-party-paid.git",
    # gabiiperez
    "https://github.com/gabbiiperez/odoo-jeo-ce.git",
    # ingadhoc
    "https://github.com/ingadhoc/account-financial-tools.git",
    "https://github.com/ingadhoc/account-invoicing.git",
    "https://github.com/ingadhoc/account-payment.git",
    "https://github.com/ingadhoc/aeroo_reports.git",
    "https://github.com/ingadhoc/argentina-reporting.git",
    "https://github.com/ingadhoc/argentina-sale.git",
    "https://github.com/ingadhoc/miscellaneous.git",
    "https://github.com/ingadhoc/odoo-argentina.git",
    "https://github.com/ingadhoc/odoo-argentina-ce.git",
    "https://github.com/ingadhoc/partner.git",
    "https://github.com/ingadhoc/product.git",
    "https://github.com/ingadhoc/project.git",
    "https://github.com/ingadhoc/reporting-engine.git",
    "https://github.com/ingadhoc/sale.git",
    "https://github.com/ingadhoc/stock.git",
    "https://github.com/ingadhoc/website.git",
    # jobiols
    "https://github.com/jobiols/odoo-addons.git",
    # OCA
    "https://github.com/OCA/account-analytic.git",
    "https://github.com/OCA/account-financial-reporting.git",
    "https://github.com/OCA/account-financial-tools.git",
    "https://github.com/OCA/commission.git",
    "https://github.com/OCA/contract.git",
    "https://github.com/OCA/helpdesk.git",
    "https://github.com/OCA/hr-expense.git",
    "https://github.com/OCA/knowledge.git",
    "https://github.com/OCA/management-system.git",
    "https://github.com/OCA/mis-builder.git",
    "https://github.com/OCA/openupgradelib.git",
    "https://github.com/OCA/partner-contact.git",
    "https://github.com/OCA/product-variant.git",
    "https://github.com/OCA/purchase-workflow.git",
    "https://github.com/OCA/queue.git",
    "https://github.com/OCA/reporting-engine.git",
    "https://github.com/OCA/sale-workflow.git",
    "https://github.com/OCA/server-auth.git",
    "https://github.com/OCA/server-tools.git",
    "https://github.com/OCA/server-ux.git",
    "https://github.com/OCA/stock-logistics-warehouse.git",
    "https://github.com/OCA/web.git",
    "https://github.com/OCA/website.git",
    # Openworx
    "https://github.com/Openworx/backend_theme.git",
    # regaby
    "https://github.com/regaby/odoo-custom.git",
]

BRANCH = "13.0"
MAIN_DIR = "custom-addons"


BASE_DIR = "./" + MAIN_DIR
NUM_REPOS = len(REPOS)

################################################################


def get_org_name(url: str) -> str:
    """
    Get the organization name from the url.
    """
    return url.split("/")[3]


def get_orgs() -> set:
    """
    Get the list of organizations from the repositories.
    """
    return set(map(get_org_name, REPOS))


ORGS = get_orgs()


def progress(count: int, total: int, status: str = ""):
    """
    Print the progress bar.
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    progress_bar = "=" * filled_len + "-" * (bar_len - filled_len)

    sys.stdout.write("[%s] %s%%%s\n" % (progress_bar, percents, status))


def create_generic_addons_main_folder() -> bool:
    """
    Create the generic addons main folder.
    """
    if os.path.exists("custom-addons"):
        return False
    os.mkdir("custom-addons")
    return True


create_generic_addons_main_folder()


def create_orgs_folders() -> bool:
    """
    Create the organizations folders.
    """
    for org in ORGS:
        org_dir = os.path.join(BASE_DIR, org)
        if os.path.exists(org_dir):
            continue
        os.mkdir(org_dir)
    return True


def git_action(repository: str) -> bool:
    """
    Clone or pull the repository.
    """
    branch = BRANCH
    repo_dir = repository.split("/")[-1].split(".")[0]
    if os.path.exists(repo_dir):
        os.chdir(repo_dir)
        print("\nUpdating " + repo_dir)
        os.system("git pull")
        os.chdir("../")
    else:
        if repo_dir == "openupgradelib":
            branch = "master"
        print("\n")
        command = f"git clone {repository} -b {branch} --depth 1 > /dev/null"
        os.system(command)
    return True


def clone_repos() -> bool:
    """
    Clone the repositories.
    """
    if create_orgs_folders():
        try:
            idx = 0
            for org in ORGS:
                os.chdir(BASE_DIR + "/" + org)
                repos = list(filter(lambda x, org=org: org in x, REPOS))
                for repository in repos:
                    git_action(repository)
                    idx += 1
                    progress(idx, NUM_REPOS)
                os.chdir("../..")
            return True
        except Exception as err:
            print(err)
            return False


if clone_repos():
    print("\nSuccessfull install. Cloned/updated " + str(len(REPOS)) + " repositories!")
    print(
        "\nAt the docstring of the script you can check how to install python requirements."
    )
    print("\nRemember to update addons_path!")
