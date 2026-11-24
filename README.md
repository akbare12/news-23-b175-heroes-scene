# THE WORLD TODAY — Monday 23 November 2026

[![THE WORLD TODAY](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b175-heroes-scene/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b175-heroes-scene/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout that hit Asian markets, Guterres' call to regulate AI before it's too late, and the US lead over China at a record low — plus 28 more stories, a world map with 13 pins, and a date check that keeps other days' news out.

## How it is made

- `draw.py` — draws `entry.png` (1024×1024) with PIL.
- `main.py` — stdlib-only entry point: verifies `entry.png` (PNG header, chunk CRCs, sha256, size) and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`.
- Run: `python3 draw.py && python3 main.py`
