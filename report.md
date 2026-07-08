# Architecture audit — status as of 2026-07-01

Full audit of `architecture_cleaning` branch (models/repository/service/core/controllers/view/menu), updated after your latest round of fixes. Status column reflects current code, not the original audit snapshot.

## Fixed since the report

| Location | Was | Status |
|---|---|---|
| `repository/round.py` | `round_match_to_json` wrote `player_score_a` twice, never `player_score_b` | **Fixed** — now serializes `player_score_b` correctly |
| `controllers/player.py` `create_new_player` | Missing `return` after error render → fell through to success render | **Fixed** — `return None` added |
| `controllers/player.py` `show_players` | Missing `return` after error render → unguarded `.get_value()` crash | **Fixed** — `return None` added |
| `controllers/player.py` | Dead, cut-off commented `show_player` method | **Fixed** — removed |
| `service/round.py` `prepare_players` | `players = tournament.registered_players` aliased the model's list; `shuffle` mutated it in place | **Fixed** — now `.copy()` before shuffle |
| `service/round.py` `is_first_round` | Unguarded `first_round[0]` → `IndexError` | **Partially fixed** — now an explicit `raise ValueError(...)` if missing. No longer an accidental `IndexError`, but still crashes instead of returning a `Result` like the rest of the app. Worth a conscious decision: is this a genuine invariant violation (fail fast is fine) or a reachable state (should be a `Result`)? |
| `core/core_data_repository.py` | Duplicate `CoreDataRepository` alongside `repository/repository.py`, with diverging filter logic; also the class whose deleted `Model.from_json/to_json` contract it depended on | **Fixed** — file deleted entirely. Resolves the "two parallel repository implementations" and the dangling `from_json`/`to_json` contract findings in one move. Confirmed nothing else imports it. |
| `controllers/round.py` `get_incomplete_matches` | Called `round.is_round_score_complete()` / `round_match.is_score_complete()`, methods that lived on the model | **Fixed** — now delegates to `round_service.get_incomplete_round_matches(round)`. Also fixes a latent bug: `round_match.score_a.chess_id` (wrong attribute, would've crashed) → `round_match.player_score_a.player.chess_id` |
| `service/tournament.py` | Unused imports `RoundJSON`, `RoundMatchJSON` | **Fixed** |
| `service/player_registration.py` | Unused imports `combinations`, `random`, `json`, `Round`, `RoundMatch` | **Fixed** |
| `service/round_match.py` | Unused imports `PLAYER_DIR`, `to_players` | **Fixed** |
| `service/tournament.py` | Duplicated payload-loading calls in `_get_tournaments` and `get_tournament_by_pk` | **New improvement** (not previously flagged) — deduplicated into `_load_related_tournament_models` |

## Still open — priority order

### 1. Scoring is still not written anywhere (highest priority)
`models/round.py` `RoundMatch.set_score` is still just `pass`. The old `calculate_match_score` / `give_score_b_value` logic that actually computed score values was **deleted**, not restored, in this pass — so this isn't fixed, the surrounding code just changed shape around it.

Concrete consequence: `PlayerScore.is_score_not_set` (new, in `models/score.py`) checks `score == INITIAL_SCORE`. Since `set_score` never writes, every match stays "not set" forever, so `RoundService.get_incomplete_round_matches` will always report every match as incomplete, so `get_next_round`/`prepare_next_round` will never advance a round past its first match-setting. This is the same root cause flagged before — it's now one layer deeper (the write path, not the read/comparison path) but it's the same missing piece: nothing ever calls `PlayerScore.score_value = ...`.

### 2. `PlayerRegistration.to_players` — errors still silently swallowed
`pk_errors` (now really chess_id errors) is built up but never returned or surfaced. Callers can't know a chess_id failed to resolve. Still inconsistent with the `Result` pattern used everywhere else.

### 3. Dead code remaining
- `service/player_registration.py` — `extract_registered_players` still defined, still no caller.
- `service/round.py` `make_pairs` — `picked_up_players` still built, never read or returned.
- `service/round_match.py` `prepare_players_dict` — `players = players` no-op self-assignment still there.

### 4. `service/round_match.py` `build_round_match`
Still raises a bare `ValueError` instead of returning `Result.invalid`, inconsistent with the railway pattern elsewhere.

### 5. Naming
`PlayerRegistration.to_players(registered_raw_players)` / loop var `raw_registered_player` — still named as if holding raw dicts or pks; they hold chess_id strings.

## Not re-verified this pass
Everything flagged in the original 6-way audit outside the changed files (`controllers/tournament.py` duplication and typos, `menu/session_context.py` raw `ValueError`, `repository/build.py` singleton wiring, `core/result.py` `None`-vs-invalid ambiguity, `models/tournament.py` dual payload/hydrated representation, `service/player.py` leftover error-message copy, etc.) — none of those files changed in this diff, so their status is unchanged from the original report.

---
*Start here tomorrow: item 1 (scoring). Everything else about round-completion detection is now correctly wired — it's just waiting on `set_score` to actually set something.*
