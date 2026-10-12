import pytest
from generated.navigation_logic import decide_next_move

def test_goal_ahead_clear():
    state = {
        'goal_ahead': True,
        'front_blocked': False,
        'goal_on_left': False,
        'goal_on_right': False,
        'left_blocked': False,
        'right_blocked': False
    }
    assert decide_next_move(state) == 'FORWARD'

def test_goal_left_clear():
    state = {
        'goal_on_left': True,
        'left_blocked': False,
        'goal_ahead': False,
        'front_blocked': False,
        'goal_on_right': False,
        'right_blocked': False
    }
    assert decide_next_move(state) == 'LEFT'

def test_goal_right_clear():
    state = {
        'goal_on_right': True,
        'right_blocked': False,
        'goal_ahead': False,
        'front_blocked': False,
        'goal_on_left': False,
        'left_blocked': False
    }
    assert decide_next_move(state) == 'RIGHT'

def test_goal_ahead_blocked_left_clear():
    state = {
        'goal_ahead': True,
        'front_blocked': True,
        'goal_on_left': False,
        'goal_on_right': False,
        'left_blocked': False,
        'right_blocked': True
    }
    assert decide_next_move(state) == 'LEFT'

def test_goal_ahead_blocked_right_clear():
    state = {
        'goal_ahead': True,
        'front_blocked': True,
        'goal_on_left': False,
        'goal_on_right': False,
        'left_blocked': True,
        'right_blocked': False
    }
    assert decide_next_move(state) == 'RIGHT'

def test_goal_left_blocked_right_clear():
    state = {
        'goal_on_left': True,
        'left_blocked': True,
        'goal_on_right': False,
        'goal_ahead': False,
        'front_blocked': False,
        'right_blocked': False
    }
    assert decide_next_move(state) == 'RIGHT'

def test_goal_left_blocked_right_blocked_front_clear():
    state = {
        'goal_on_left': True,
        'left_blocked': True,
        'goal_on_right': False,
        'goal_ahead': False,
        'front_blocked': False,
        'right_blocked': True
    }
    assert decide_next_move(state) == 'FORWARD'

def test_all_blocked():
    state = {
        'goal_ahead': False,
        'front_blocked': True,
        'goal_on_left': False,
        'goal_on_right': False,
        'left_blocked': True,
        'right_blocked': True
    }
    assert decide_next_move(state) == 'STOP'

def test_no_goal_front_clear():
    state = {
        'goal_ahead': False,
        'front_blocked': False,
        'goal_on_left': False,
        'goal_on_right': False,
        'left_blocked': False,
        'right_blocked': False
    }
    assert decide_next_move(state) == 'FORWARD'