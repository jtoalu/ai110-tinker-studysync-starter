from sessions import find_conflicts


def test_find_conflicts_empty_sessions():
    assert find_conflicts([]) == []


def test_find_conflicts_single_session():
    assert find_conflicts([{"subject": "Calc II", "slot": "08:00"}]) == []


def test_find_conflicts_without_shared_slots():
    sessions = [
        {"subject": "Calc II", "slot": "08:00"},
        {"subject": "Chem Lab", "slot": "09:00"},
    ]
    assert find_conflicts(sessions) == []


def test_find_conflicts_returns_each_matching_pair_once():
    first = {"subject": "Calc II", "slot": "08:00"}
    second = {"subject": "Chem Lab", "slot": "08:00"}
    third = {"subject": "History", "slot": "08:00"}
    fourth = {"subject": "Biology", "slot": "09:00"}

    assert find_conflicts([first, second, third, fourth]) == [
        (first, second),
        (first, third),
        (second, third),
    ]