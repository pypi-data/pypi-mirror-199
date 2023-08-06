# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2020 David Seaward and contributors
from importlib import resources

# noinspection PyPackageRequirements
import apt  # must be installed externally
import click
import os
import shutil
import parse
import subprocess
from ruamel.yaml import YAML

# EMPTY COLLECTION VARIABLE

ALL_DOMAINS = {}

# DECLARE KNOWLEDGE BASE VARIABLES

PACKAGE_LIST = YAML().load(resources.read_text("checkyoself.kb", "apt.yml"))
BIN_LIST = YAML().load(resources.read_text("checkyoself.kb", "bin.yml"))

# HOME-BASED FOLDERS

HOME_FOLDER = os.path.expanduser("~")
HOME_LOCAL_BIN = os.path.expanduser("~/.local/bin")


def domains_append(domain, value):
    if domain.startswith("www."):
        domain = domain[4:]

    if domain not in ALL_DOMAINS:
        ALL_DOMAINS[domain] = []

    if value not in ALL_DOMAINS[domain]:
        ALL_DOMAINS[domain].append(value)


def domains_list():
    full_list = sorted(ALL_DOMAINS.keys())
    for key in full_list:
        if key != "unknown":
            yield key

    if "unknown" in full_list:
        yield "unknown"


def domains_print(verbose=False):
    if verbose:
        for key in domains_list():
            print("* " + key)
            for value in sorted(ALL_DOMAINS[key]):
                print("   * " + value)
    else:
        print("* " + "\n* ".join(domains_list()))


def recursive_scandir(path):
    for element in os.scandir(path):
        if element.is_dir(follow_symlinks=False):
            for element in recursive_scandir(element):
                yield element
        else:
            yield element


def get_deb_sources():
    for element in recursive_scandir("/etc/apt/"):
        if element.is_file() and element.name.endswith(".list"):
            yield element


def get_packages():
    cache = apt.Cache()
    for pkg in cache:
        if pkg.installed and pkg.name in PACKAGE_LIST:
            yield pkg.name


def get_domains_from_text(text):
    # find and yield tidied https domains
    https_results = parse.findall("https://{domain}/", text)
    for result in https_results:
        domain = result["domain"]
        if domain.startswith("www."):
            domain = domain[4:]
        yield domain

    # find and yield raw http-without-s domains
    http_unsecured_results = parse.findall("http://{domain}/", text)
    for result in http_unsecured_results:
        yield "http://" + result["domain"]


@click.command()
def check():
    """
    Before you wreck yo' self. Cause unknown sources are bad for your health.

    Returns a list of online repositories that your system relies on. Verbose
    mode additionally lists the software that uses them.
    """

    # GET DOMAINS FROM APT SOURCES

    for element in get_deb_sources():
        with open(element) as f:
            for domain in get_domains_from_text(f.read()):
                domains_append(domain, element.path)

    # GET DOMAINS FROM FLATPAK SOURCES

    if shutil.which("flatpak") is not None:
        result = subprocess.run(
            ["flatpak", "remotes", "--show-details", "--show-disabled"],
            capture_output=True,
        )
        for domain in get_domains_from_text(str(result.stdout)):
            domains_append(domain, "flatpak")

    # LOOK UP DOMAINS FOR RECOGNISED PACKAGES

    for name in get_packages():
        for domain in PACKAGE_LIST[name]:
            domains_append(domain, "apt:" + name)

    # LOOK UP DOMAINS FOR RECOGNISED BINARIES

    for name in BIN_LIST.keys():
        path = shutil.which(name)
        if path is not None:
            for domain in BIN_LIST[name]:
                domains_append(domain, path.replace(HOME_FOLDER, "~"))

    # LIST LOCAL INSTALLATIONS NOT IN LISTS

    for path in [HOME_LOCAL_BIN, "/usr/local/bin"]:
        for element in os.scandir(path):
            if element.is_file(follow_symlinks=True):
                if element.name not in BIN_LIST and element.name not in PACKAGE_LIST:
                    domains_append("unknown", element.path.replace(HOME_FOLDER, "~"))

    for element in os.scandir("/opt"):
        if element.is_dir(follow_symlinks=False):
            if element.name not in BIN_LIST and element.name not in PACKAGE_LIST:
                domains_append("unknown", element.path)

    domains_print(verbose=True)
