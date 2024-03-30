#!/bin/bash

apt-get update
apt-get install -y autoconf automake build-essential cmake git libass-dev libbz2-dev libfontconfig-dev libfreetype-dev libfribidi-dev libharfbuzz-dev libjansson-dev liblzma-dev libmp3lame-dev libnuma-dev libogg-dev libopus-dev libsamplerate0-dev libspeex-dev libtheora-dev libtool libtool-bin libturbojpeg0-dev libvorbis-dev libx264-dev libxml2-dev libvpx-dev m4 make meson nasm ninja-build patch pkg-config tar zlib1g-dev libnvidia-encode
apt-get install -y handbrake-cli
apt-get install -y libimage-exiftool-perl

python3.12 -m pip install --no-cache-dir -r ./requirements-dev.txt