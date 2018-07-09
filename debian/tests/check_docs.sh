#!/bin/bash

RESULT=0

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

if ! [ -f /usr/share/doc-base/python3-streamlink-doc ]; then
	echo "Cannot read /usr/share/doc-base/python3-streamlink-doc" >&2
	exit 1
fi

echo "Doc-base file content:"
cat /usr/share/doc-base/python3-streamlink-doc
echo "---------"

echo "Checking Files field"
DOC_FILES_WILDCARD=$(grep Files /usr/share/doc-base/python3-streamlink-doc | sed 's/Files: //')
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
INDEX_HTML_LOCATION=$(grep Index /usr/share/doc-base/python3-streamlink-doc | sed 's/Index: //')

case $INDEX_HTML_LOCATION in /usr/share/doc/*)
	;;
*)
	echo "index.html must be in /usr/share/doc/ but is \"$INDEX_HTML_LOCATION\"" >&2
	exit 2
esac

HTML_BASE_DIR=$(dirname "$INDEX_HTML_LOCATION")

check-file "$INDEX_HTML_LOCATION" || exit 3
check-file "$HTML_BASE_DIR/_static/fonts/FontAwesome.otf" || RESULT=4
check-file "$HTML_BASE_DIR/_static/fonts/fontawesome-webfont.eot" || RESULT=4
check-file "$HTML_BASE_DIR/_static/fonts/fontawesome-webfont.svg" || RESULT=4
check-file "$HTML_BASE_DIR/_static/fonts/fontawesome-webfont.ttf" || RESULT=4
check-file "$HTML_BASE_DIR/_static/fonts/fontawesome-webfont.woff" || RESULT=4
check-file "$HTML_BASE_DIR/_static/js/modernizr.min.js" || RESULT=5

exit "$RESULT"
