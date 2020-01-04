import json
import logging
from typing import Any
from typing import Text, Optional, Dict

import questionary
from prompt_toolkit.styles import Style
from rasa.cli import utils as cli_utils
from rasa.core.channels import console
from rasa.core.interpreter import INTENT_MESSAGE_PREFIX

from saai.shell.settings import sett
import subprocess

logger = logging.getLogger(__name__)

DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS = 10


def _bot_output(
    message: Dict[Text, Any], color=cli_utils.bcolors.OKBLUE
) -> Optional[questionary.Question]:
    from sagas.nlu.tts_utils import say_lang
    # from sagas.kit.analysis_kit import AnalysisKit

    if ("text" in message) and not ("buttons" in message):
        text=message.get("text")
        cli_utils.print_color(text, color=color)
        say_lang(text, sett.lang, False)
        # AnalysisKit().console_vis(text, sett.lang)

    if "image" in message:
        cli_utils.print_color("Image: " + message.get("image"), color=color)

    if "attachment" in message:
        cli_utils.print_color("Attachment: " + message.get("attachment"), color=color)

    if "buttons" in message:
        choices = cli_utils.button_choices_from_message_data(
            message, allow_free_text_input=True
        )

        question = questionary.select(
            message.get("text"),
            choices,
            style=Style([("qmark", "#6d91d3"), ("", "#6d91d3"), ("answer", "#b373d6")]),
        )
        return question

    if "elements" in message:
        cli_utils.print_color("Elements:", color=color)
        for idx, element in enumerate(message.get("elements")):
            cli_utils.print_color(
                cli_utils.element_to_string(element, idx), color=color
            )

    if "quick_replies" in message:
        cli_utils.print_color("Quick Replies:", color=color)
        for idx, element in enumerate(message.get("quick_replies")):
            cli_utils.print_color(cli_utils.button_to_string(element, idx), color=color)

    if "custom" in message:
        cli_utils.print_color("Custom json:", color=color)
        cli_utils.print_color(json.dumps(message.get("custom"), indent=2), color=color)

def _user_input(button_question: questionary.Question) -> Optional[Text]:
    exit_text = INTENT_MESSAGE_PREFIX + "stop"

    if button_question is not None:
        response = cli_utils.payload_from_button_question(button_question)
        if response == cli_utils.FREE_TEXT_INPUT_PROMPT:
            # Re-prompt user with a free text input
            response = _user_input(None)
    else:
        response = questionary.text(
            "",
            qmark="Your input ->",
            style=Style([("qmark", "#b373d6"), ("", "#b373d6")]),
        ).ask()

    text= response.strip() if response is not None else None
    if not sett.is_disable_analyse:
        if text is not None and not text.startswith(INTENT_MESSAGE_PREFIX):
            subprocess.call(['sagas', 'vis', text, sett.lang])
    return text

def inject():
    console.print_bot_output=_bot_output
    console.get_user_input=_user_input

def shell_main():
    from rasa.__main__ import main
    from sagas.tool.loggers import init_logger

    init_logger()

    inject()
    main()

# $ python -m saai.shell shell
if __name__ == "__main__":
    shell_main()

