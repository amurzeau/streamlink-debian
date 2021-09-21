#!/bin/bash

set -e

RESULT=0

DOCBASE_DATA=$(/usr/sbin/install-docs -s python3-streamlink-doc)

check-file() {
	local TARGET_FILE="$1"
	echo -n "Checking file $TARGET_FILE"
	if ! [ -f "$TARGET_FILE" ]; then
		echo " MISSING"
		return 1
	else
		echo " OK"
	fi
	return 0
}

if [ -z "$DOCBASE_DATA" ]; then
	echo "Cannot read install-docs -s python3-streamlink-doc" >&2
	exit 1
fi

echo "Doc-base file content:"
echo "$DOCBASE_DATA"
echo "---------"

echo "Checking Files field"
DOC_FILES_WILDCARD=$(grep Files <<<"$DOCBASE_DATA" | sed 's/Files: //')
echo "Content of $DOC_FILES_WILDCARD:"
# no quotes intended: doc-base file use wildcards and we want them to be expanded
# shellcheck disable=SC2086
ls -l $DOC_FILES_WILDCARD
echo "---------"

# shellcheck disable=SC2206
DOC_FILES_COUNT=( $DOC_FILES_WILDCARD )
if ! [ -f "${DOC_FILES_COUNT[0]}" ]; then
	echo "$DOC_FILES_WILDCARD match no files" >&2
	exit 2
fi

echo "Checking files:"
INDEX_HTML_LOCATION=$(grep Index <<<"$DOCBASE_DATA" | sed 's/Index: //')

case $INDEX_HTML_LOCATION in /usr/share/doc/*)
	;;
*)
	echo "index.html must be in /usr/share/doc/ but is \"$INDEX_HTML_LOCATION\"" >&2
	exit 2
esac

check-file "$INDEX_HTML_LOCATION" || exit 3

exit "$RESULT"
