# Audit — `Result.__bool__` : `is_valid` vs `value is not None`

Every construction site of `Result.valid(...)` / `Result.invalid(...)` in the codebase, cross-referenced with every place a `Result` is used in a boolean context (`if result`, `if not result`, `while result`). Goal: identify which call sites still work if `__bool__` switches from `bool(self._is_valid)` to `self._value is not None`.

**Note on semantics**: the mentor's target is `value is not None`, not `bool(value)`. That distinction matters — some legitimately valid values are falsy (`0`, `""`, `[]`, `{}`). Keep the check as an identity check against `None`, not a truthiness check on the value itself.

## Safe — already pass a value

These construct `Result.valid(...)` with a real value, so switching `__bool__` changes nothing for them.

| Location | Call |
|---|---|
| `service/player.py:32` | `Result.valid(value=unregistered_players)` |
| `service/player.py:56` | `Result.valid(value=similar_players)` |
| `service/player.py:65` | `Result.valid(player)` |
| `service/player.py:96` | `Result.valid(sorted_players)` |
| `controllers/validators/menu.py:11` | `Result.valid(value=menu_number)` (note: value can be `0` — still `is not None`, still truthy, correctly) |
| `service/tournament.py:116` | `Result.valid(data_by_field_name)` |
| `service/tournament.py:159` | `Result.valid(tournament)` |
| `service/tournament.py:173` | `Result.valid(value=similar_tournaments)` |
| `service/tournament.py:209` | `Result.valid(value=tournament.registered_players)` |
| `service/tournament.py:234` | `Result.valid(tournaments)` |
| `service/round.py:136` | `Result.valid(value=round)` |
| `service/round.py:187` | `Result.valid(value=next_round)` |
| `service/player_registration.py:45` | `Result.valid(value=tournament)` |
| `controllers/tournament.py:58` | `Result.valid(value=self.select_tournament_from_list(tournaments))` |
| `controllers/tournament.py:60` | `Result.valid(value=tournaments[0])` |
| `controllers/tournament.py:128` | `Result.valid(value=round)` |
| `controllers/tournament.py:200` | `Result.valid(value=self.select_player_from_list(unregistered_players))` |
| `controllers/tournament.py:204` | `Result.valid(value=unregistered_players[0])` |
| `controllers/tournament.py:216` | `Result.valid(value=tournament)` |

## Breaks — `Result.valid()` with no value, truthiness relied on downstream

These are the ones your mentor's change would flip from truthy to falsy. Each row shows where the missing-value success gets tested.

| Location (constructs) | Call | Tested at | Consequence if unchanged |
|---|---|---|---|
| `service/player.py:75` `can_save` | `Result.valid()` | `service/player.py:83` `if not can_save_resut:` in `create_new_player` | A save-allowed check reads as failed → every `create_new_player` call rejected |
| `service/player.py:88` `create_new_player` | `Result.valid(success_message=...)` | `controllers/player.py:20` `if not create_result:` | Player creation always reports as failed to the controller, even though the player was saved |
| `controllers/validators/menu.py:34` `is_choice_in_range` | `Result.valid()` | `core/core_handler.py:25` `if not user_input_result:` (inside `while True`) | Every in-range menu choice is rejected as invalid → **infinite reprompt loop**, menu becomes unusable |
| `controllers/validators/date.py:13` `validate_date` | `Result.valid()` | `core/core_handler.py:25` (used as `validation_function` for birthdate / start / end date prompts) | Every valid date is rejected → **infinite reprompt loop** on any date entry |
| `controllers/validators/chess_id.py:15` `validate_chess_id` | `Result.valid()` | `core/core_handler.py:25` (used as `validation_function` for chess_id prompt) | Every well-formed chess_id is rejected → **infinite reprompt loop** on player creation |
| `service/round.py:150` `check_registered_players_pairs` | `Result.valid()` | `service/round.py:129` `if not player_pairs_check_result:` in `_set_round_players` | A valid, even-numbered player list reads as invalid → round players never get set |
| `service/round.py:175` placeholder in `prepare_next_round` | `round_players_result: Result = Result.valid()` | `service/round.py:184` `if not round_players_result:` | Only breaks in one branch: when the next round's matches are **already defined** (`are_round_matches_defined` true), the placeholder is never overwritten and gets read as invalid, so `prepare_next_round` returns an invalid `Result` even though there's a legitimate next round to run. Propagates up through `controllers/round.py:77` and `controllers/tournament.py`'s `run_tournament` loop. |
| `service/player_registration.py:30` `check_if_player_already_registered` | `Result.valid()` | `service/player_registration.py:41` `if not already_registered_result:` in `register_player_to_tournament` | "Not already registered" (the OK-to-proceed case) reads as invalid → registration always rejected |
| `controllers/round.py:70` `should_continue_setting_scores` | `Result.valid() if selected_menu_item.value else Result.invalid(...)` | `controllers/tournament.py:125` `if not should_continue_result:` in `TournamentRunner.should_continue` | Choosing "continue" reads as invalid → tournament loop stops prematurely even when the user asked to continue |
| `service/tournament.py:183` `check_chess_id_exists` | `Result.valid()` | *(no live caller found anywhere in the codebase — dead code)* | Not currently reachable, but would have the same failure mode as the others if ever wired up |

## Summary

10 live call sites (+1 dead) construct a "valid" `Result` without a value, and every one of them has its truthiness tested somewhere downstream. All 10 would silently start reporting success as failure the moment `__bool__` switches to `self._value is not None` — three of them (`is_choice_in_range`, `validate_date`, `validate_chess_id`) sit inside `while True` prompt loops, so those specifically would hang the CLI rather than just misreport.
