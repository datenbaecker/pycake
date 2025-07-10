import os


def supported_lang():
    return ["en", "de", "fr", "it"]


def get_lang():
    lang = "en"
    lang_env = os.getenv("LANG", "")[:2]
    if lang_env in supported_lang():
        lang = lang_env
    return lang


def get_cake_msg(what, cache_data_path=None, expected=None, argument=None):
    lang = get_lang()

    msg = {
        "delete_cache_data": {
            "en": f"This command deletes all data in '{cache_data_path}'. Do you wish to continue (y/n)?",
            "de": f"Dieser Befehl l\u00f6scht s\u00e4mtliche Daten in '{cache_data_path}'. Willst du fortfahren (j/n)?"
        },
        "cache_data": {
            "en": "Would you like to save the data on your disc? (y/n)",
            "de": "M\u00f6chtest du die Daten lokal speichern? (j/n)"
        },
        "info_cache_data": {
            "en": "`pycake` may save the data on your local disc.\n"
            "This speeds up data loading in subsequent Python session.\n"
            "Specify `cache_data` if you don't want to answer this question in future calls.",
            "de": "`pycake` kann die Daten auf deiner lokalen Festplatte speichern.\n"
            "Das beschleunigt das Laden der Daten in zuk\u00fcnftigen Python-Sessions.\n"
            "Spezifiziere `cache_data` falls du diese Frage zuk\u00fcnftig nicht mehr erhalten m\u00f6chtest."
        },
        "invalid_cache_data_arg": {
            "en": "`cache_data` must be of type `str` or `bool`.",
            "de": "`cache_data` muss vom Typ `str` oder `bool` sein."
        },
        "invalid_cache_dir": {
            "en": f"Directory '{cache_data_path}' does not exist.",
            "de": f"Das Verzeichnis '{cache_data_path}' existiert nicht."
        },
        "downloading": {
            "en": "Downloading data, this takes a while...",
            "de": "Daten werden heruntergeladen. Dieser Vorgang dauert eine Weile..."
        },
        "not_in_menu": {
            "en": "Value for `what` or `flavor` is invalid. Check `menu` for data catalog.",
            "de": "Wert f\u00fcr `what` oder `flavor` ist nicht g\u00fcltig. Siehe `menu` für Datenkatalog."
        },
        "dataprovider_required": {
            "en": "No value for `data_provider` provided."
        },
        "abort_class": {
            "en": f"Expected object of type {expected} for argument {argument}"
        },
        "no_endpoint": {
            "en": "Attribute `endpoint` not found. Did you already edit the object?"
        },
        "no_metadata": {
            "en": "No metadata available for this object."
        },
        "timeout": {
            "en": "The server did not respond in the usual amount of time. Please try again later..."
        }
    }
    rel_msg = msg.get(what, {})
    return rel_msg.get(lang, rel_msg.get("en", f"[Message '{what}' not found]"))


def cake_abort(err, **kwargs):
    message = get_cake_msg(err, **kwargs)
    print(message)


def cake_abort_class(expected, arg):
    cake_abort("abort_class", expected=expected, argument=arg)


def cake_alert(msg, **kwargs):
    message = get_cake_msg(msg, **kwargs)
    print(f"[ALERT] {message}")


def cake_alert_info(msg, **kwargs):
    message = get_cake_msg(msg, **kwargs)
    print(f"[INFO] {message}")
