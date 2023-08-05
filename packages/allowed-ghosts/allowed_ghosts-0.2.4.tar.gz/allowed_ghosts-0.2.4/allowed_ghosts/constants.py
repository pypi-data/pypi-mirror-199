#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# author        : JV-conseil
# credits       : JV-conseil
# copyright     : Copyright (c) 2019-2023 JV-conseil
#                 All rights reserved
#
# Retrieve the list of your Public Link domains
# https://cloud.sdu.dk/app/public-links
#
# curl 'https://cloud.sdu.dk/api/ingresses/browse?itemsPerPage=100&includeOthers=true&sortDirection=ascending' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Authorization: Bearer ***' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: trailers' --compressed | jq '.items[].specification.domain'
#
# ====================================================

UNAVAILABLE_GHOSTS = frozenset(
    [
        "app-santa-maria-josefina-do-coracao-de-jesus-sancho-de-guerra.cloud.sdu.dk",
    ]
)
