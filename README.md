# Sunfish chess experiment: corresponding source

This local package contains the source and build scripts for the packed 60k-node chess experiment in `outputs/sunfish-60k-main.py`. It is derived from Sunfish by Thomas Dybdahl Ahle and contributors, at commit `e396948acbd80cdcbad3dccfb07e878fba9df8f4`:

https://github.com/thomasahle/sunfish/tree/e396948acbd80cdcbad3dccfb07e878fba9df8f4

The derived work is licensed under GPL-3.0-only. The full license is in `LICENSE`. The adapter and search-limit modifications were made on November 10, 2026. They replace the original UCI driver with an adapter for the make.fun game environment and replace the clock-based search limit with a fixed node threshold. The final experiment changes the threshold from 50,000 to 60,000; the search checks the threshold every 2,048 nodes.

`work/sunfish-60k.py` is the exact readable source used to produce the packed experiment. `work/sunfish-experiment.py` is the earlier 50,000-threshold adaptation. `work/build-sunfish-fork.py` is the actual script used to create that earlier adaptation from `work/sunfish-upstream-repo/nnue_4k/pst_entry.py`. The 60,000-threshold source differs from that adaptation by its search-limit value; the generator produces the earlier file, not the final one.

To reproduce the packed file from this directory, run `python work/pack-sunfish-60k.py`. This script uses `python_minifier` version 3.4.0 and Python's standard `lzma` library. Install or otherwise make that free, general-purpose minifier available to Python first. The script writes `outputs/sunfish-60k-main.py`. With the locally available minifier, the resulting SHA-256 is `d3a8afc8adb157528100378e0cb3691c3517b63ee34f2a4f74b1645db35705af`, matching the local candidate.

This package supplies the preferred source, upstream credit, build tools, and full GPL license for the packed 60k-node experiment.
