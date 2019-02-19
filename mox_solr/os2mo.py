# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import logging

from mox_solr.config import settings


logger = logging.getLogger("mox_solr")
os2mo_headers = {
    "SESSION": settings["OS2MO_SAML_TOKEN"]
}


def os2mo_url(url):
    """format url like {BASE}/o/{ORG}/e
    """
    url = url.format(
        BASE=settings["OS2MO_SERVICE_URL"],
        ORG=settings["OS2MO_ORG_UUID"],
    )
    return url


def os2mo_get(url, **params):
    url = os2mo_url(url)
    try:
        r = requests.get(
            url,
            headers=os2mo_headers,
            params=params,
            verify=settings["OS2MO_CA_BUNDLE"]
        )
        r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)
        raise


def user_uuids():
    return [e["uuid"] for e in os2mo_get("{BASE}/o/{ORG}/e").json()["items"]]


def get_solr_employee(uuid):
    employee = os2mo_get("{BASE}/e/" + uuid + "/").json()
    employee["id"] = employee["uuid"]
    apply_all_details(employee, "e")
    apply_history(employee, "e")
    return employee


def org_unit_uuids():
    return [e["uuid"] for e in os2mo_get("{BASE}/o/{ORG}/ou").json()["items"]]


def get_solr_orgunit(uuid):
    orgunit = os2mo_get("{BASE}/ou/" + uuid + "/").json()
    orgunit["id"] = orgunit["uuid"]
    apply_all_details(orgunit, "ou")
    apply_history(orgunit, "ou")
    return orgunit


def apply_all_details(obj, objtyp):
    for d, has_detail in os2mo_get(
            "{BASE}/" + objtyp + "/" + obj["uuid"] + "/details"
    ).json().items():
        if has_detail:
            obj.setdefault(
                "details", {}
            ).setdefault(
                d, []
            ).extend(
                os2mo_get(
                    "{BASE}/" + objtyp + "/" + obj["uuid"] + "/details/" + d
                ).json()
            )

def apply_history(obj, objtyp):
    obj["history"] = os2mo_get(
        "{BASE}/" + objtyp + "/" + obj["uuid"] + "/history"
        ).json()
