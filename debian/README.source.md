# Build procedure

Here are the commands to manage the package

## For unstable

```sh
# Switch to master branch
git checkout master

# Import upstream version and update Debian branch with new upstream release
gbp import-orig --uscan

# Update debian/patches
gbp pq rebase

# Go back to master branch
gbp pq switch

# Check licenses changes and update debian/copyright
find . \( -path './.git' -o -path './debian' \) -prune -o -type f -print0 | xargs -0  grep -i '\bCopyright\b'

# Check for new dependencies
git diff upstream^..upstream docs-requirements.txt dev-requirements.txt pyproject.toml docs/install.rst

# Check for new supported players
git diff upstream^..upstream docs/players.rst

# Check for important changes that may need other package changes (copyright, new patch, ...):
#  `https://github.com/streamlink/streamlink/compare/<old_tag>...<new_tag>`

# Update debian/changelog
gbp dch -Ra --commit

# Do test build with sbuild
gbp buildpackage "--git-builder=sbuild -v -As -d unstable --no-clean-source --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\" --build-failed-commands '%SBUILD_SHELL'"

# Check for build warnings or errors
grep -Pi 'error|warn' ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version)_amd64.build

# Diff with previous package version
diffoscope ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version -c1 -o1)_all.deb ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version)_all.deb --text-color=always | less -r -s
diffoscope ../build-area/python3-streamlink_$(dpkg-parsechangelog --show-field Version -c1 -o1)_all.deb ../build-area/python3-streamlink_$(dpkg-parsechangelog --show-field Version)_all.deb --text-color=always | less -r -s
diffoscope ../build-area/python3-streamlink-doc_$(dpkg-parsechangelog --show-field Version -c1 -o1)_all.deb ../build-area/python3-streamlink-doc_$(dpkg-parsechangelog --show-field Version)_all.deb --text-color=always | less -r -s

# Tag commit
gbp tag --sign-tags

# Push to git repository
git push origin experimental master upstream pristine-tar bullseye-backports --tags

# Push to mentors FTP
dput mentors ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version)_amd64.changes
```

## For experimental

```sh
# Update debian/changelog
gbp dch -Ra --commit -Dexperimental

# Do test build with sbuild (using experimental as an alias to unstable schroot)
gbp buildpackage "--git-builder=sbuild -v -As -d experimental --no-clean-source --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\" --build-failed-commands '%SBUILD_SHELL'" --extra-repository='deb http://deb.debian.org/debian experimental main' --build-dep-resolver=aspcud
```

The rest is identical to unstable.


## For backports

```sh
# Switch to backport branch
git checkout <backport-branch>

# Merge master branch
git merge master

# Update debian/changelog
gbp dch -Ra --bpo --commit

# Do test build with sbuild
gbp buildpackage "--git-builder=sbuild -v -As -d bullseye-backports --no-clean-source --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\" --build-failed-commands '%SBUILD_SHELL' --build-dep-resolver=aptitude"

# Check for build warnings or errors
grep -Pi 'error|warn' ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version)_amd64.build

# Diff with previous package version
diffoscope ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version -c1 -o1)_all.deb ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version)_all.deb --text-color=always | less -r -s
diffoscope ../build-area/python3-streamlink_$(dpkg-parsechangelog --show-field Version -c1 -o1)_all.deb ../build-area/python3-streamlink_$(dpkg-parsechangelog --show-field Version)_all.deb --text-color=always | less -r -s
diffoscope ../build-area/python3-streamlink-doc_$(dpkg-parsechangelog --show-field Version -c1 -o1)_all.deb ../build-area/python3-streamlink-doc_$(dpkg-parsechangelog --show-field Version)_all.deb --text-color=always | less -r -s

# Tag commit
gbp tag --sign-tags

# Push to git repository
git push origin experimental master upstream pristine-tar bullseye-backports --tags

# Push to mentors FTP
dput mentors ../build-area/streamlink_$(dpkg-parsechangelog --show-field Version)_amd64.changes

```

# Building package from streamlink unreleased version

- Checkout master (andd update it if needed)
- Ensure git status return no modification (no dirty working copy)
- Generate python tarball: python3 ./setup.py sdist
- Import with gbp and filtering: `gbp import-orig --interactive --verbose --rollback ../streamlink_0.14.2-170-g3946184.orig.tar.gz --filter-pristine-tar --filter=docs/_themes/sphinx_rtd_theme_violet/static/fonts`


# Packages structure

## streamlink

This package contains the command line tool which use the public Python module available in python3-streamlink package.

This package contains the Python module `streamlink_cli` which is private and so goes to /usr/share/streamlink.
The command line script is also in /usr/share/streamlink so it can find the Python module.
/usr/bin/streamlink is a symlink to the command line script.

See also an advice about why not putting the command line script in /usr/bin:
  https://lists.debian.org/debian-python/2016/05/msg00046.html

As recommended in dh_installman manpage, manpage installation is defined in streamlink.manpages.

## python3-streamlink

This package contains the public Python module `streamlink`.

## python3-streamlink-doc

This package contains streamlink documentation in html format.
