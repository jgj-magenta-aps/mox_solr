import os
import pathlib
import configparser

inipaths = [p for p in [
        pathlib.Path(os.environ.get("MOX_MO_CONFIG", "")),
        pathlib.Path("") / "settings.ini",
        pathlib.Path(__file__).absolute() / "settings.ini",
    ] if p.is_file()
]

if not len(inipaths):
    inifile = ""
else:
    inifile = inipaths[0]

config = configparser.ConfigParser(defaults={
    "MOX_LOG_LEVEL": "10",
    "MOX_LOG_FILE": "",
    "OS2MO_SERVICE_URL": "http://some-os2mo-url:5000/service",
    "OS2MO_SAML_TOKEN": "token-from-saml-slash-api-token",
    "OS2MO_ORG_UUID": "",
    "OS2MO_CA_BUNDLE": "true",
    "SOLR_URL": "http://some-solr-url:8983"
})

config["settings"] = {}

if inifile:
    config.read(str(inifile))

settings = {k.upper(): v for k, v in dict(config["settings"]).items()}

if settings["OS2MO_CA_BUNDLE"].lower() in ["false", ""]:
    settings["OS2MO_CA_BUNDLE"] = False
elif settings["OS2MO_CA_BUNDLE"].lower() in ["true"]:
    settings["OS2MO_CA_BUNDLE"] = True
