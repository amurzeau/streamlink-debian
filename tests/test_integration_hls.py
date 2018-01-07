import sys
import os
if sys.version_info[0:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

try:
    from unittest.mock import patch, ANY
except ImportError:
    from mock import patch, ANY
from Crypto.Cipher import AES
from binascii import hexlify
from subprocess import call
from pkg_resources import load_entry_point

def pkcs7_encode(data, keySize):
    val = keySize - (len(data) % keySize)
    return b''.join([data, bytes(bytearray(val * [val]))])

def encrypt(data, key, iv):
    aesCipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = aesCipher.encrypt(pkcs7_encode(data, len(key)))
    return encrypted_data

class TestIntegration(unittest.TestCase):
    """
    Test that when invoked for the command line arguments are parsed as expected
    """
    fileToRemove = []

    @patch('sys.stdin')
    @patch('sys.argv')
    def start_streamlink(self, args, mock_argv, mock_stdin):
        tracer = sys.gettrace()
        if tracer is not None:
            print("Detected coverage, running streamlink from inside this python instance")
            mock_argv.__getitem__.side_effect = lambda x: args[x]
            mock_stdin = None
            try:
                load_entry_point('streamlink==0.9.0', 'console_scripts', 'streamlink')()
            except SystemExit as exc:
                self.assertEqual(exc.code, 0)
        else:
            print("Running streamlink as a subprocess")
            self.assertEqual(call(args), 0)

    def writeFile(self, name, data):
        with open(name, 'wb') as fout:
            fout.write(data)
        self.fileToRemove.append(name)

    def readFile(self, name):
        with open(name, 'rb') as fin:
            data = fin.read()
        self.fileToRemove.append(name)
        return data

    def tearDown(self):
        # Remove left over files
        # Don't error out when we can't remove them
        # (which can be the case when running streamlink without subprocess)
        for file in self.fileToRemove:
            print("Removing {0}".format(file))
            try:
                os.remove(file)
            except OSError as e:
                print("Error while closing {0}: {1}".format(file, e))


    def test_encrypted_hls_stream(self):
        # Encryption parameters
        aesKey = os.urandom(16)
        aesIv = os.urandom(16)
        # Generate stream data files
        clearStreams = [ os.urandom(1024) for i in range(4) ]
        encryptedStreams = [ encrypt(clearStream, aesKey, aesIv) for clearStream in clearStreams ]

        # Write stream data files
        for i, encryptedStream in enumerate(encryptedStreams):
            self.writeFile("stream{0}.ts.enc".format(i), encryptedStream)

        # Write encrytion key
        self.writeFile("encryption_key.key", aesKey)

        # Write HLS playlist
        self.writeFile("playlist.m3u8", """\
#EXTM3U
#EXT-X-VERSION:5
#EXT-X-TARGETDURATION:3
#ID3-EQUIV-TDTG:2018-01-01T18:20:05
#EXT-X-MEDIA-SEQUENCE:1688
#EXT-X-TWITCH-ELAPSED-SECS:3367.800
#EXT-X-TWITCH-TOTAL-SECS:3379.943
#EXT-X-KEY:METHOD=AES-128,URI="encryption_key.key",IV=0x{0},KEYFORMAT=identity,KEYFORMATVERSIONS=1
#EXTINF:1.667,
stream0.ts.enc
#EXTINF:2.000,
stream1.ts.enc
#EXTINF:2.000,
stream2.ts.enc
#EXTINF:2.000,
stream3.ts.enc
#EXT-X-ENDLIST
""".format(hexlify(aesIv).decode("UTF-8")).encode("UTF-8"))

        # Write HLS master playlist
        self.writeFile("master.m3u8", """\
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
""".encode("UTF-8"))

        self.writeFile("player.py", """
import sys
import requests
r = requests.get(sys.argv[1])
with open("output_stream.ts", "wb") as f:
    f.write(r.content)
""".encode("UTF-8"))

        # Start streamlink on the generated stream
        self.start_streamlink([
            "streamlink",
            "-l",
            "debug",
            "--config=nonexisting",
            "--hls-audio-select", "en",
            "--player="+sys.executable+" player.py",
            "-v",
            "--player-http",
            "--player-continuous-http",
            "hlsvariant://file://./master.m3u8",
            "best"
        ])

        # Retrieve streamlink output
        streamlinkResult = self.readFile("output_stream.ts")

        # Check result
        expectedResult = b''.join(clearStreams)
        self.assertEqual(streamlinkResult, expectedResult)


if __name__ == "__main__":
    unittest.main()
