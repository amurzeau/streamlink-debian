#!/bin/sh

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
ls -l $DOC_FILES_WILDCARD
echo "---------"

DOC_FILES_COUNT=$(ls -1 $DOC_FILES_WILDCARD | wc -l)
if ! [ $DOC_FILES_COUNT -gt 0 ]; then
	echo "$DOC_FILES_COUNT file found in $DOC_FILES_WILDCARD" >&2
	exit 2
fi

echo "Checking Index field"
INDEX_HTML_LOCATION=$(grep Index /usr/share/doc-base/python3-streamlink-doc | sed 's/Index: //')

case $INDEX_HTML_LOCATION in /usr/share/doc/*)
	;;
*)
	echo "index.html must be in /usr/share/doc/ but is \"$INDEX_HTML_LOCATION\"" >&2
	exit 2
esac

echo "Checking $INDEX_HTML_LOCATION file"
if ! [ -f "$INDEX_HTML_LOCATION" ]; then
	echo "File \"$INDEX_HTML_LOCATION\" does not exists" >&2
	exit 3
fi

echo "Checking fonts symlinks:"
HTML_BASE_DIR=$(dirname "$INDEX_HTML_LOCATION")
FONTS_NAME="FontAwesome.otf fontawesome-webfont.eot fontawesome-webfont.svg fontawesome-webfont.ttf fontawesome-webfont.woff"
for  font in $FONTS_NAME; do
	echo "Checking $HTML_BASE_DIR/_static/fonts/$font"
	if ! [ -f "$HTML_BASE_DIR/_static/fonts/$font" ]; then
		echo "Missing font: \"$HTML_BASE_DIR/_static/fonts/$font\"" >&2
		exit 4
	fi
done

