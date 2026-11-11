from app.models.misconception import MisconceptionState


def determine_next_state(
    current_state: MisconceptionState,
    misconception_detected: bool
) -> MisconceptionState:

    if current_state == MisconceptionState.POSSIBLE:
        if misconception_detected:
            return MisconceptionState.PERSISTENT

        return MisconceptionState.IMPROVING


    if current_state == MisconceptionState.PERSISTENT:
        if misconception_detected:
            return MisconceptionState.PERSISTENT

        return MisconceptionState.IMPROVING


    if current_state == MisconceptionState.IMPROVING:
        if misconception_detected:
            return MisconceptionState.PERSISTENT

        return MisconceptionState.RESOLVED


    if current_state == MisconceptionState.RESOLVED:
        if misconception_detected:
            return MisconceptionState.RECURRENCE

        return MisconceptionState.RESOLVED


    if current_state == MisconceptionState.RECURRENCE:
        if misconception_detected:
            return MisconceptionState.RECURRENCE

        return MisconceptionState.IMPROVING


    return current_state