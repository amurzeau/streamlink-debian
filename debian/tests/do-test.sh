#!/bin/sh

set -x

test_program=${1:-"streamlink"}

cd ${AUTOPKGTEST_TMP:-"."}

# This test does:
# - Generate a AES-128 encrypted HLS fake stream from /dev/urandom to playlist.m3u8 and
#   stream0000x.ts
# - Generate a master HLS playlist with only one stream quality existing (1080p)
# - Execute streamlink (or its alternative name via $test_program) on that
#   stream using the best quality (which must match the 1080p quality)
# - Tell streamlink to output stream to stream_output.ts
# - Concat all source stream files (stream0000x.ts) and compare the result with
#   streamlink result
# - Echo a statement if there is no differences

# Notes:
# - An encrypted stream is used to test the use of the python encryption library (like pycrypto).
# - The encrypted stream is not padded as streamlink does not remove any padding.
# - An audio stream with language=en is used so streamlink code using pycountry is triggered

echo "Generating HLS stream data" &&
for i in 0 1 2 3; do dd if=/dev/zero of=stream$i.ts bs=1K count=20 status=none; done &&
dd if=/dev/urandom of=encryption_key.key bs=16 count=1 &&
for i in 0 1 2 3; do openssl aes-128-cbc -e -in stream$i.ts -out stream$i.ts.enc -iv 67452301674523016745230167452301 -K $(hexdump encryption_key.key -e '/1 "%02X"') -nosalt -nopad; done &&
cat > playlist.m3u8 << EOF &&
#EXTM3U
#EXT-X-VERSION:5
#EXT-X-TARGETDURATION:3
#ID3-EQUIV-TDTG:2018-01-01T18:20:05
#EXT-X-MEDIA-SEQUENCE:1688
#EXT-X-TWITCH-ELAPSED-SECS:3367.800
#EXT-X-TWITCH-TOTAL-SECS:3379.943
#EXT-X-KEY:METHOD=AES-128,URI="encryption_key.key",IV=0x67452301674523016745230167452301,KEYFORMAT=identity,KEYFORMATVERSIONS=1
#EXTINF:1.667,
stream0.ts.enc
#EXTINF:2.000,
stream1.ts.enc
#EXTINF:2.000,
stream2.ts.enc
#EXTINF:2.000,
stream3.ts.enc
#EXT-X-ENDLIST
EOF
echo "Generating HLS master playlist" &&
cat > master.m3u8 << EOF &&
#EXTM3U
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="720p30",NAME="720p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2299652,RESOLUTION=1280x720,CODECS="avc1.77.31,mp4a.40.2",VIDEO="720p30"
720p.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="480p30",NAME="480p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1354652,RESOLUTION=852x480,CODECS="avc1.77.31,mp4a.40.2",VIDEO="480p30"
480p.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="360p30",NAME="360p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=630000,RESOLUTION=640x360,CODECS="avc1.77.31,mp4a.40.2",VIDEO="360p30"
360p.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="160p30",NAME="160p",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=230000,RESOLUTION=284x160,CODECS="avc1.77.31,mp4a.40.2",VIDEO="160p30"
160p.m3u8
#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="chunked",NAME="1080p (source)",AUTOSELECT=YES,DEFAULT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3982010,RESOLUTION=1920x1080,CODECS="avc1.4D4029,mp4a.40.2",VIDEO="chunked"
playlist.m3u8
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio_only",NAME="audio_only",AUTOSELECT=YES,DEFAULT=NO,LANGUAGE="en"
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=90145,CODECS="mp4a.40.2",VIDEO="audio_only"
audio_only.m3u8
EOF
echo "Starting $test_program" &&
"$test_program" -l debug --config=nonexisting --hls-audio-select en "hlsvariant://file://./master.m3u8" best -f -o output_stream.ts &&
echo "Comparing output to expected output" &&
cat stream*.ts > expected_stream.ts &&
diff expected_stream.ts output_stream.ts &&
echo "#### OK, Test successful, parsed stream output match expected output"
