#!/bin/sh

NEW_VERSION=$(sed -nr 's/streamlink \((.*)\).*/\1/p' debian/changelog | sed -n '1 p')
NEW_VERSION_UPSTREAM=$(echo "$NEW_VERSION" | sed -r 's/(.*)-.*/\1/')

RFS_INTROLINE="for a new
upstream version ${NEW_VERSION_UPSTREAM}"

PACKAGES_LIST="  python3-streamlink - Python module for extracting video streams from
various websites
  python3-streamlink-doc - CLI for extracting video streams from
various websites (documentation)
  streamlink - CLI for extracting video streams from various websites
to a video player
"

CHANGELOG_INTROLINE="Changes since the last upload to unstable:"


if git symbolic-ref HEAD | grep -q backports; then
    DISTRIBUTION=$(git symbolic-ref HEAD | sed -r 's#refs/heads/(.*)-backports#\1#')
    OLD_VERSION=$(sed -nr "s/streamlink \((.*)\) ${DISTRIBUTION}-backports.*/\1/p" debian/changelog | sed -n '2 p')
    TESTING_VERSION=$(sed -nr "s/streamlink \((.*)\) unstable.*/\1/p" debian/changelog | sed -n '1 p')
    ADDITIONAL_FIELDS="X-Debbugs-CC: debian-backports@lists.debian.org"
    RFS_INTROLINE="into Debian
${DISTRIBUTION}-backports repository"
    CHANGELOG_INTROLINE="Changes since the previous backported version in ${DISTRIBUTION}:"
    CHANGELOG_BACKPORT="
Differences from testing package ($TESTING_VERSION):
  * d/patches: reintroduce pytest 7 patch to add missing
    ExceptionInfo.group_contains method.

"
else
    OLD_VERSION=$(sed -nr 's/streamlink \((.*)\) unstable.*/\1/p' debian/changelog | sed -n '2 p')
    ADDITIONAL_FIELDS=""
    CHANGELOG_BACKPORT=""
fi

ESCAPED_OLD_VERSION=$(echo "$OLD_VERSION" | sed -r 's/([][+\()*/])/\\\1/g')
CHANGELOG=$(sed -r "/^streamlink \($ESCAPED_OLD_VERSION\)/,\$d" debian/changelog)

MAIL_SUBJECT="RFS: streamlink/${NEW_VERSION} -- CLI for extracting video streams from various websites to a video player"
MAIL_BODY="Package: sponsorship-requests
Severity: normal
${ADDITIONAL_FIELDS}

Dear mentors,

I am looking for a sponsor for my package \"streamlink\" ${RFS_INTROLINE}.

  * Package name    : streamlink
    Version         : ${NEW_VERSION}
    Upstream Author : Streamlink Team
  * URL             : https://streamlink.github.io/
  * License         : BSD-2-clause, Apache-2.0, MIT/Expat, SIL-OFL-1.1
  * Vcs             : https://salsa.debian.org/amurzeau/streamlink/
    Section         : python

It builds those binary packages:
${PACKAGES_LIST}

To access further information about this package, please visit the
following URL:

  https://mentors.debian.net/package/streamlink/

Alternatively, you can download the package with 'dget' using this command:

  dget -x https://mentors.debian.net/debian/pool/main/s/streamlink/streamlink_${NEW_VERSION}.dsc

${CHANGELOG_BACKPORT}
${CHANGELOG_INTROLINE}
${CHANGELOG}

Regards,
"

if [ -n "$DISPLAY" ] && command -v thunderbird > /dev/null; then
    thunderbird -compose "subject='$MAIL_SUBJECT',to='submit@bugs.debian.org',body='$MAIL_BODY'"
else
    echo "submit@bugs.debian.org"
    echo "$MAIL_SUBJECT"
    echo
    echo "$MAIL_BODY"
fi
