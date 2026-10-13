"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    # TODO: use csv.DictReader to read csv_path into a list of dicts.
    # TODO: convert row["distance_miles"] to float and row["seats_available"] to int for each row.
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        spots = list(csv.DictReader(csv_file))

    for spot in spots:
        spot["distance_miles"] = float(spot["distance_miles"])
        spot["seats_available"] = int(spot["seats_available"])

    return spots


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    # TODO: implement additive/weighted scoring using at least noise_level
    # (compare using NOISE_ORDER), distance_miles vs max_distance, and
    # seats_available vs min_seats. Append a short string to `reasons` for
    # each factor that contributed, whether it helped or hurt the score.
    score = 0
    reasons = []

    if NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]]:
        score += 1
        reasons.append("quiet enough")
    else:
        score -= 1
        reasons.append("too noisy")

    if spot["distance_miles"] <= profile["max_distance"]:
        score += 1
        reasons.append("close enough")
    else:
        score -= 1
        reasons.append("too far")

    if spot["seats_available"] >= profile["min_seats"]:
        score += 1
        reasons.append("enough seats")
    else:
        score -= 1
        reasons.append("not enough seats")

    return score, reasons

def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    # TODO: score every spot with score_study_spot(), then use
    # sorted(..., key=..., reverse=True)[:k] to keep only the top k.
    raise NotImplementedError


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    # TODO: for each (spot, score, reasons) tuple, print a readable line, e.g.:
    # "1. Innovation Commons -- Score: 5.0 -- Because: quiet enough, close enough"
    raise NotImplementedError


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    print(f"Loaded {len(spots)} study spots from CSV.")
    for number, spot in enumerate(spots, start=1):
        print(
            f"{number}. {spot['name']} — "
            f"Noise: {spot['noise_level']}, "
            f"Distance: {spot['distance_miles']} miles, "
            f"Seats available: {spot['seats_available']}"
        )    
    print(f"type of distance_miles: {type(spots[0]['distance_miles'])}")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    print(
        "Study Profile: "
        f"Max noise: {profile['max_noise']}, "
        f"Max distance: {profile['max_distance']} miles, "
        f"Minimum seats: {profile['min_seats']}"
    )    
    assert spots, "No study spots were loaded from the CSV."

    spot_numbers = (1, 3, 5)
    assert len(spots) >= max(spot_numbers), "The CSV must contain at least 5 spots."

    for spot_number in spot_numbers:
        spot = spots[spot_number - 1]
        score, reasons = score_study_spot(profile, spot)

        expected_score = 0
        expected_reasons = []

        if NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]]:
            expected_score += 1
            expected_reasons.append("quiet enough")
        else:
            expected_score -= 1
            expected_reasons.append("too noisy")

        if spot["distance_miles"] <= profile["max_distance"]:
            expected_score += 1
            expected_reasons.append("close enough")
        else:
            expected_score -= 1
            expected_reasons.append("too far")

        if spot["seats_available"] >= profile["min_seats"]:
            expected_score += 1
            expected_reasons.append("enough seats")
        else:
            expected_score -= 1
            expected_reasons.append("not enough seats")

        assert score == expected_score, f"Unexpected score for spot #{spot_number}: {spot['name']}"
        assert reasons == expected_reasons, f"Unexpected reasons for spot #{spot_number}: {spot['name']}"
        print(f"PASS: Spot #{spot_number} ({spot['name']}) -- Score: {score} -- Because: {', '.join(reasons)}")
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)
