import requests
import datetime
import json
import collections
import logging
logger = logging.getLogger("mox_solr")

solrurl = "http://solr-24194:8983"
schemas = {"os2mo":{},"lora":{}}

def post(*args, **kwargs):
    # override when testing
    return requests.post(*args, **kwargs)

def schema(rectype, record):
    # post fields
    s = schemas[rectype]
    for k,v in record.items():
        s[k] = field = { "name": k, "stored": True, "type": "text_general"}
        if k.endswith("validity.from"):
            field["type"] = "pdates"
        elif k.endswith("validity.to"):
            field["type"] = "pdates"
        res = post(
            solrurl+"/solr/" + rectype + "/schema",
            json={"add-field": field})

def flatten(d, parent_key='', sep='.', rectype=""):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if new_key.endswith("user_settings"):
            continue
        if isinstance(v, list):
            items.extend(flatten({str(i):iv for i,iv in enumerate(v)}, new_key, sep=sep).items())
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif new_key.endswith("validity.from"):
            items.append((new_key, v +"T00:00:00Z"))
        elif new_key.endswith("validity.to"):
            if v:
                items.append((new_key, v +"T00:00:00Z"))
            else:
                items.append((new_key, "9999-12-31T00:00:00Z"))
        else:
            items.append((new_key, v))
    retdict = dict(items)
    if rectype and set(retdict) != set(schemas[rectype]):
        schema(rectype, retdict)
    return retdict

import pprint
def upsert_orgunit(orgunit):
    logger.debug("upsert orgunit: %s", orgunit["uuid"])
    orgunit["id"] = orgunit["uuid"]
    add("os2mo", [flatten(orgunit)])

def upsert_employee(employee):
    logger.debug("upsert employee: %s", employee["uuid"])
    employee["id"] = employee["uuid"]
    add("os2mo", [flatten(employee)])


def add(core, records):
    payload = ",\n".join(['"add": { "doc": %s }' % json.dumps(r) for r in records])
    payload = "{\n%s\n}"% payload
    return post(solrurl + "/solr/"
                + core + "/update?commitWithin=10000",
                headers={"Content-Type": "application/json"},
                data=payload)

