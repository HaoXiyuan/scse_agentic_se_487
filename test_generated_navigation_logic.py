## A typical test case: 
""" {
    "goal_ahead": True,
    "goal_on_left": False,
    "goal_on_right": False,
    "front_blocked": False,
    "left_blocked": False,
    "right_blocked": False
},
"FORWARD" """
## Use the above test case to create more test cases for all the possible states

from artifacts.navigation_logic import decide_next_move


TEST_CASES = [
    # Goal ahead, front clear -> FORWARD
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "FORWARD"),

    # Goal on left, left clear -> LEFT
    ({"goal_ahead": False, "goal_on_left": True, "goal_on_right": False,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "LEFT"),

    # Goal on right, right clear -> RIGHT
    ({"goal_ahead": False, "goal_on_left": False, "goal_on_right": True,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "RIGHT"),

    # Goal ahead but front blocked, left clear -> LEFT
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": True, "left_blocked": False, "right_blocked": False},
     "LEFT"),

    # Goal ahead but front blocked, left blocked, right clear -> RIGHT
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": True, "left_blocked": True, "right_blocked": False},
     "RIGHT"),

    # All blocked -> STOP
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": True, "left_blocked": True, "right_blocked": True},
     "STOP"),

    # No goal in front, but front clear -> FORWARD
    ({"goal_ahead": False, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "FORWARD"),
]


def test_decide_next_move():
    for state, expected in TEST_CASES:
        result = decide_next_move(state)
        assert result in {"FORWARD", "LEFT", "RIGHT", "STOP"}, \
            f"Invalid action: {result}"
        assert result == expected, \
            f"State {state}: expected {expected}, got {result}"
    print(f"All {len(TEST_CASES)} test cases passed.")


if __name__ == "__main__":
    test_decide_next_move()