#!/bin/bash

# Usage: ./decompress.sh <filename>
FILE="data7.bin"

while true; do
    TYPE=$(file "$FILE")
    if echo "$TYPE" | grep -q 'bzip2 compressed data'; then
        mv "$FILE" "$FILE.bz2"
        bunzip2 "$FILE.bz2"
        FILE="${FILE%.*}"
    elif echo "$TYPE" | grep -q 'gzip compressed data'; then
        mv "$FILE" "$FILE.gz"
        gunzip "$FILE.gz"
        FILE="${FILE%.*}"
    elif echo "$TYPE" | grep -q 'tar archive'; then
        mv "$FILE" "$FILE.tar"
        tar -xf "$FILE.tar"
        # Find the extracted file (assume only one file/folder extracted)
        FILE=$(tar -tf "$FILE.tar" | head -n 1)
        rm "$FILE.tar"
    else
        echo "Decompression complete: $FILE"
        break
    fi
done