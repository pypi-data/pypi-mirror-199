# Check yo' self (dibbity deb remix)

Which online repositories does my system rely on?

## Status

Very early prototype.

## Usage

```
Usage: checkyoself [OPTIONS]

  Before you wreck yo' self. Cause unknown sources are bad for your health.

  Returns a list of online repositories that your system relies on. Verbose
  mode additionally lists the software that uses them.

Options:
  --help  Show this message and exit.
```

## Sample output

These are the repositories that your system might download additional
components from.

```
* deb.debian.org
* dl.flathub.org
* http://ppa.launchpad.net
* pypi.org
```

## Sample output (verbose)

These are the sources that might access the repositories:

```
* deb.debian.org
   * /etc/apt/sources.list.d/buster-backports.list
* dl.flathub.org
   * flatpak
* http://ppa.launchpad.net
   * /etc/apt/sources.list.d/micahflee-ubuntu-ppa-bionic.list
   * /etc/apt/sources.list.d/papirus.list
* pypi.org
   * apt:python3-pip
```

## Scope

- Packages installed by `apt` \[1\]
- Knowledge base limited to packages found in Debian stable, PureOS stable
    and/or Ubuntu LTS \[1\]
- Best effort. We don't know what we don't know.
- No advisory stance (libre? security practices? domain owner?)
- Packages with hard-coded repositories or default configurations, not packages
    like `wget` that perform arbitrary downloads or packages like `telnet` that
    perform arbitrary communication.
- Known default repositories only \[2\]

##### Exceptions and additions

- \[1\] We report on the online repositories of non-deb packages from very
    significant software authors. For example `aws` from Amazon relies on
    `aws.amazon.com`
- \[2\] We report on the configuration values of `apt` and `flatpak`, not just
    their defaults.

## Additional notes

- Inspired by, but not quite the same as,
    [vrms](https://salsa.debian.org/debian/vrms)

- Not a substitute for inspecting which domains your machine is *actually*
    connecting to.

- Intended to inspire recording this information at the time of packaging, and
    alerting the user at the time of installation: "foo relies on bar.com, do you
    want to install it? Y/N"

<!-- start @generated footer -->

# Development environment

## Install prerequisites

- Python 3.10
- pdm
- make

## Instructions

- Fork the upstream repository.
- `git clone [fork-url]`
- `cd [project-folder]`
- Run `make develop` to initialise your development environment.

You can use any text editor or IDE that supports virtualenv / pdm. See the
Makefile for toolchain details.

Please `make test` and `make lint` before submitting changes.

## Make targets

```
USAGE: make [target]

help    : Show this message.
develop : Set up Python development environment.
run     : Run from source.
clean   : Remove all build artefacts.
test    : Run tests and generate coverage report.
lint    : Fix or warn about linting errors.
build   : Clean, test, lint, then generate new build artefacts.
publish : Upload build artefacts to PyPI.
```

# Sharing and contributions

```
Check yo' self (dibbity deb remix)
https://lofidevops.neocities.org
Copyright 2020 David Seaward and contributors
SPDX-License-Identifier: AGPL-3.0-or-later
```

Shared under AGPL-3.0-or-later. We adhere to the Contributor Covenant 2.1, and
certify origin per DCO 1.1 with a signed-off-by line. Contributions under the
same terms are welcome.
