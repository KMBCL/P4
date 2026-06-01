from controllers.choice import ChoiceStyleKey, Choice


class StylePicker:
    exit_style = "bold red"
    back_style = "bold yellow"
    navigation_style = "bold cyan"
    action_style = "bold green"
    invalid_style = "red"
    input_awaiting_style = "green"

    @classmethod
    def pickup_style(cls, choice: Choice) -> str:
        if choice.style_to_apply == ChoiceStyleKey.EXIT:
            return cls.exit_style

        if choice.style_to_apply == ChoiceStyleKey.BACK:
            return cls.back_style

        if choice.style_to_apply == ChoiceStyleKey.ACTION:
            return cls.action_style

        return cls.navigation_style
