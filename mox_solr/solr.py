import requests
import collections
import logging
import dateutil.parser
import pytz
import re
from mox_solr import config


logger = logging.getLogger("mox_solr")
settings = config.settings

solrurl = settings["SOLR_URL"]
schemas = {}


def get(*args, **kwargs):
    # override when testing
    return requests.get(*args, **kwargs)


def post(*args, **kwargs):
    # override when testing
    return requests.post(*args, **kwargs)


def schema(rectype, record):
    # fetch existing fields from solr
    if rectype not in schemas:
        schemas[rectype] = {
            f["name"]: f
            for f in get(
                solrurl + "/solr/" + rectype + "/schema/fields"
            ).json()['fields']
        }
    s = schemas[rectype]

    # add any new fields, infering type
    for k, v in record.items():
        if k in s:
            continue
        s[k] = field = {"name": k, "stored": True, "type": "text_general"}
        if k.endswith("validity.from"):
            field["type"] = "pdates"
        elif k.endswith("validity.to"):
            field["type"] = "pdates"
        elif re.match(r'history\.[0-9]+\.(from|to)', k):
            field["type"] = "pdates"
        logger.debug("adding field to schema %r", field)
        post(
            solrurl+"/solr/"+rectype+"/schema",
            json={"add-field": field}
        )


def flatten(d, parent_key='', sep='.', rectype=""):
    # recursive, how to know top? only caller sends rectype.
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if new_key.endswith("user_settings"):
            continue
        #if isinstance(v, list):
        #    items.extend(flatten({
        #        str(i): iv
        #        for i, iv in enumerate(v)
        #        }, new_key, sep=sep).items())
        #    continue
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif new_key.endswith("validity.from"):
            items.append((new_key, v+"T00:00:00Z"))
        elif new_key.endswith("validity.to"):
            if v:
                items.append((new_key, v + "T00:00:00Z"))
            else:
                items.append((new_key, "9999-12-31T00:00:00Z"))
        elif re.match(r'history\.[0-9]+\.(from|to)', new_key) and v:
            dttz = dateutil.parser.parse(v)
            dtutc = dttz.astimezone(pytz.utc)
            items.append((new_key, dtutc.strftime("%Y-%m-%dT%H:%M:%SZ")))
        elif v:
            items.append((new_key, v))
    retdict = dict(items)
    if rectype and set(retdict) != set(schemas.get(rectype, {})):
        schema(rectype, retdict)
    return retdict


def upsert_orgunit(orgunit):
    logger.debug("upsert orgunit: %s", orgunit["uuid"])
    orgunit["id"] = orgunit["uuid"]
    add("os2mo-orgunit", flatten(orgunit, rectype="os2mo-orgunit"))


def upsert_employee(employee):
    logger.debug("upsert employee: %s", employee["uuid"])
    employee["id"] = employee["uuid"]
    add("os2mo-employee", flatten(employee, rectype="os2mo-employee"))


def add(core, record):
    try:
        res = post(
            solrurl + "/solr/"
            + core + "/update/json/docs?commitWithin=10000",
            headers={"Content-Type": "application/json"},
            json=record
        )
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        raise
