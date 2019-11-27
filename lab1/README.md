#  📂 bashplay

### Usage

```bash
clone https://github.com/yungvldai/bashplay
cd bashplay/
sudo apt-get install ffmpeg mp3info
sudo chmod a+x filetree.sh
./filetree.sh <directory>
```

### Output

For example

```
user@pc:~/bashp$ ./filetree.sh .
bashp
║ exp
║ ╠═ audio.mp3 - ext: mp3, mime: audio/mpeg; charset=binary, 7601548 bytes, duration: 190 s.
║ ╠═ dog_and_cat.jpg - ext: jpg, mime: image/jpeg; charset=binary, 209021 bytes, size: 1000x485 pxls.
║ ╠═ lorem_ipsum.txt - ext: txt, mime: text/plain; charset=us-ascii, 446 bytes.
║ ╠═ package.json - ext: json, mime: text/plain; charset=us-ascii, 24 bytes.
║ ╚═ video.mp4 - ext: mp4, mime: video/mp4; charset=binary, 12444893 bytes, duration: 18.582000 s.
╠═ files2.sh - ext: sh, mime: text/plain; charset=us-ascii, 535 bytes.
╚═ files.sh - ext: sh, mime: text/plain; charset=utf-8, 1521 bytes.

```

Also, *filetree* creates file `./log.csv`, which contains the same data.
