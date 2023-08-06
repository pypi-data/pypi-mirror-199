#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2023-03-24 10:17:53 (ywatanabe)"

import random
import string

from datetime import datetime


def gen_ID(N=8):
    """Generates an ID like 'yyyy-mmdd-wwwwwwww'"""

    now = datetime.now()
    today_str = now.strftime("%Y-%m%d")
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(N)]
    rand_str = "".join(randlst)
    return today_str + "_" + rand_str
