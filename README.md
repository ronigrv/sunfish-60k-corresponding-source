# Sunfish chess experiment: corresponding source

This package contains the source and build scripts for the 60k-node chess experiment and its UTF-8-safe entry. It is derived from Sunfish by Thomas Dybdahl Ahle and contributors, at commit `e396948acbd80cdcbad3dccfb07e878fba9df8f4`:

https://github.com/thomasahle/sunfish/tree/e396948acbd80cdcbad3dccfb07e878fba9df8f4

The derived work is licensed under GPL-3.0-only. The full license is in `LICENSE`. The adapter and search-limit modifications were made on November 10, 2026. They replace the original UCI driver with an adapter for the make.fun game environment and replace the clock-based search limit with a fixed node threshold. The final experiment changes the threshold from 50,000 to 60,000; the search checks the threshold every 2,048 nodes.

`work/sunfish-60k.py` is the exact readable source used to produce the packed experiment. `work/sunfish-experiment.py` is the earlier 50,000-threshold adaptation. `work/build-sunfish-fork.py` is the actual script used to create that earlier adaptation from `work/sunfish-upstream-repo/nnue_4k/pst_entry.py`. The 60,000-threshold source differs from that adaptation by its search-limit value; the generator produces the earlier file, not the final one.

The original build first ran `work/pack-sunfish-60k.py`, then
`original-assemble-sunfish-utf8.py`, which has local workspace paths and
is retained here as the actual historical assembler. The readable launcher
and its seven-bit encoding were subsequently built into the source-bundle
repository. The original engine adaptation predates that repository's
freshness anchor; the later 60k change was made without this agent session
having observed the anchor. Neither is represented as anchored fresh work.

To reproduce the UTF-8 entry independently:

1. Extract `chess-corresponding-source.zip` in this directory. Its README is
   a historical snapshot from the earlier Latin-1 build; this top-level README
   supersedes it for publication and current entry details.
2. Make Python 3 and `python-minifier==3.4.0` available.
3. Run `python pack_utf8.py`. It reads `work/sunfish-60k.py` and writes
   `sunfish-utf8-main.py`.

The reproduction tool was written after the original build. It verifies the
source and compressed payload before writing the executable. The expected
UTF-8 file is 4,079 bytes with SHA-256
`1eff75f7b55048ad9312edf195df9ed885b4026d8655e621b223658229c3341c`.
The compressed payload has SHA-256
`eef1deba060a9ed20fe904a27703d07da52f5fc92f1be7c037f4b026b8376fb2`.
Its exact bytes can depend on the minifier and LZMA implementation; the
checks fail rather than silently produce a different entry.

This package supplies the preferred source, upstream credit, build tools, and full GPL license for the packed 60k-node experiment.

## 30k experiment

The 60k competition submission timed out in the official 3,600-second trial.
The 30k experiment changes its search threshold from 60,000 to 30,000 nodes;
because it checks every 2,048 nodes, the stop occurs at 30,720 nodes. This is
an attempted runtime fix, not proof of a winning score or a timing guarantee.
The entry retains the Sunfish GPL-3.0-only provenance described above. The
original adaptation predates its contest freshness anchor and may need review.

`sunfish-30k.py` is the corresponding human-readable source. With Python 3 and
`python-minifier==3.4.0` available, run `python pack_30k.py` to reproduce
`sunfish-30k-entry.py`. The expected 4,085-byte UTF-8 launcher has SHA-256
`7c8c40861c5334a3702186572642a987e1e4dab715733034abfb54def727a632`.
The packer checks its compressed payload and fails on a different build.

## Independently adapted 24k experiment

The [corresponding source package](independent-sunfish-24k-corresponding-source.zip)
contains the readable engine, the pinned Sunfish upstream source, the full
GPL-3.0-only license and attribution, and the build scripts and their licenses.
Its ZIP SHA-256 is
`0fae482bfc82d662ed3aecb3155b27526b58b634d90ebe1f7027b3431607ccf3`.

To reproduce the executable, extract the ZIP and run
`python -B build.py main.reproduced.py` from that directory with CPython 3.12.5. The
included minifier needs no network or installation. The expected 4,018-byte
file has SHA-256
`9912732c57135f6629bdab047195dd375f646d8f0cd138e8594bd46839fd36e4`.

The fixed search limit is 24,000 nodes. Four local games on selected practice
openings produced one win and three losses; this small sample does not establish
tournament strength. Official sandbox timing, a full-trial replay, and a
statistically reliable advantage over the house baseline remain unverified.
The executable and its corresponding source remain GPL-3.0-only; the separately
vendored python-minifier is MIT-licensed.
