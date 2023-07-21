from asciimatics.screen import Screen


def get_default_palette():
    return {
        "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "shadow": (Screen.COLOUR_BLACK, None, Screen.COLOUR_BLACK),
        "disabled": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "invalid": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_RED),
        "label": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "borders": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "scroll": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "title": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "readonly": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_readonly": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "button": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_YELLOW),
        "control": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_control": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_focus_control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_field": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
    }

def get_warning_palette():
    return {
        "background": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "shadow": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "borders": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "scroll": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "edit_text": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "readonly": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "focus_readonly": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "button": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "control": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "selected_control": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "focus_control": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "field": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "selected_field": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "focus_field": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLACK),

        "invalid": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_RED),
        "label": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "title": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "selected_focus_field": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "focus_edit_text": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "focus_button": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "selected_focus_control": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "disabled": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    }
