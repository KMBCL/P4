from models.round import Round, RoundMatch, Score


def flat_rounds(rounds: list[Round]) -> list[RoundMatch]:
    return [round_match for round in rounds for round_match in round.round_matches]


def flat_scores(round_matches: list[RoundMatch]) -> list[Score]:
    return [score for round_match in round_matches for score in round_match.to_list()]


def flat_pairs(round_matches: list[RoundMatch]) -> list[set[str]]:
    return [
        set((round_match.score_a.chess_id, round_match.score_b.chess_id))
        for round_match in round_matches
    ]
