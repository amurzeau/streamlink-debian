# Build procedure

Here are the commands to manage the package:
- Import upstream version and update Debian branch with new upstream release:
  - `gbp import-orig --uscan`

- Refresh patches:
  - `gbp pq rebase`

- Check for important changes that may need other package changes (copyright, new patch, ...):
  - `https://github.com/streamlink/streamlink/compare/<old_tag>...<new_tag>`

- Build and test the package:
  - `debuild`

- Release version:
  - `gbp dch -Ra --commit`

- Build source package and tag Debian branch:
  - `gbp buildpackage --git-tag --git-sign-tags -nc -S`

- Build package using sbuild:
  - `sbuild -As ../streamlink_<version>.dsc -d unstable`
  - `gbp buildpackage "--git-builder=sbuild -v -As -d unstable --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\" --build-failed-commands '%SBUILD_SHELL'"`

- Run lintian:
  - `lintian -EviIL +pedantic  ./streamlink_<version>_amd64.changes`

- Don't forget to push `master` and `upstream` branches along with new tags (`debian/<version>`, `upstream/<version>`)

## For unstable

```sh
# Switch to master branch
git checkout master

# Import latest upstream release
gbp import-orig --uscan

# Update debian/patches
gbp pq rebase

# Go back to master branch
gbp pq switch

# Update debian/changelog
gbp dch -Ra --commit

# Do test build with sbuild
gbp buildpackage "--git-builder=sbuild -v -As -d unstable --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\" --build-failed-commands '%SBUILD_SHELL'"

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
gbp buildpackage "--git-builder=sbuild -v -As -d bullseye-backports --run-lintian --lintian-opts=\"-EviIL +pedantic\" --run-autopkgtest --autopkgtest-root-args= --autopkgtest-opts=\"-- schroot %r-%a-sbuild\" --build-failed-commands '%SBUILD_SHELL' --build-dep-resolver=aptitude"

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

# Changes checks

Check copyrights
Check dependencies in https://streamlink.github.io/install.html
Check doc dependencies:
	- libjs-modernizr
	- fonts-font-awesome
	- fonts-lato
	- fonts-inconsolata
	- fonts-roboto-slab
Check supported players in https://streamlink.github.io/players.html

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
