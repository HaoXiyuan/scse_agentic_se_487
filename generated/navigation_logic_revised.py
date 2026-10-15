def decide_next_move(state):
    # First, check if the goal is in front and the path is clear
    if state['goal_ahead'] and not state['front_blocked']:
        return "FORWARD"
    # Then, check if the goal is on the left and the path is clear
    if state['goal_on_left'] and not state['left_blocked']:
        return "LEFT"
    # Then, check if the goal is on the right and the path is clear
    if state['goal_on_right'] and not state['right_blocked']:
        return "RIGHT"
    # If no goal direction is viable, try to move left first
    if not state['left_blocked']:
        return "LEFT"
    # Then, try to move right
    if not state['right_blocked']:
        return "RIGHT"
    # Finally, try to move forward if all else fails
    if not state['front_blocked']:
        return "FORWARD"
    # If all paths are blocked, stop
    return "STOP"