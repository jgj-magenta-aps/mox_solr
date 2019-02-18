# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from mox_solr import os2mo, solr, config


settings = config.settings

# set warning-level for all loggers
[
    logging.getLogger(i).setLevel(logging.WARNING)
    for i in logging.root.manager.loggerDict
]

logging.basicConfig(level=int(settings["MOX_LOG_LEVEL"]),
                    filename=settings["MOX_LOG_FILE"])
logger = logging.getLogger("mox_solr")
logger.setLevel(int(settings["MOX_LOG_LEVEL"]))


def sync_solr_orgunits():
    os2mo_uuids = set(os2mo.org_unit_uuids())
    for i in os2mo_uuids:
        orgunit = os2mo.get_solr_orgunit(i)
        solr.upsert_orgunit(orgunit)


def sync_solr_users():
    os2mo_uuids = set(os2mo.user_uuids())
    for i in os2mo_uuids:
        employee = os2mo.get_solr_employee(i)
        solr.upsert_employee(employee)


if __name__ == "__main__":
    if not settings["OS2MO_ORG_UUID"]:
        settings["OS2MO_ORG_UUID"] = os2mo.os2mo_get(
            "{BASE}/o/"
        ).json()[0]["uuid"]
    sync_solr_orgunits()
    sync_solr_users()
