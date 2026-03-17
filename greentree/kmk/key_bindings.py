from kmk.keys import KC


class KB:
    """keybinding class. Some of these shortcuts require different kmk modules
    and since we don't know when this library will be imported, we will create it only
    after all modules are appended in the external script."""

    def __init__(self):
        self.COPY = KC.LGUI(KC.C)
        self.PASTE = KC.LGUI(KC.V)
        self.CUT = KC.LGUI(KC.X)
        self.COPY_DT_PASTE = KC.TD(self.COPY, self.PASTE)

        self.TOP_LEFT_SCREEN__DT__LEFT_HALF_SCREEN = KC.TD(
            KC.LCTRL(KC.LALT(KC.U)),
            KC.LCTRL(KC.LALT(KC.LEFT)),
            KC.LCTRL(KC.LALT(KC.E)),
        )
        self.TOP_RIGHT_SCREEN__DT__RIGHT_HALF_SCREEN = KC.TD(
            KC.LCTRL(KC.LALT(KC.I)),
            KC.LCTRL(KC.LALT(KC.RIGHT)),
            KC.LCTRL(KC.LALT(KC.T)),
        )
        self.BOTTOM_LEFT_SCREEN__DT__FULL_SCREEN = KC.TD(
            KC.LCTRL(KC.LALT(KC.J)),
            KC.LCTRL(KC.LALT(KC.C)),
        )
        self.BOTTOM_RIGHT_SCREEN__DT__CENTER_SCREEN = KC.TD(
            KC.LCTRL(KC.LALT(KC.K)),
            KC.LCTRL(KC.LALT(KC.ENTER)),
        )

        self.XNAPPER_SCREENSHOT = KC.LCTRL(KC.LALT(KC.LGUI(KC.N4)))
        self.HOLD_LAYER_ONE = KC.MO(1)  # Activates layer 1 when held
        self.CLOSE_WINDOW = KC.LGUI(KC.W)
        self.BROSWER_NEW_TAB = KC.LGUI(KC.T)
