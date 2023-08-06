# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2023-02-27
#


import miaou


miaou.generate(
    site_url="http://localhost:21250/zentao",
    # dev_url="http://localhost:21830/dev-api-index.html",
    username="admin",
    password="Lton2008@",
    combined_print=True,
    output_path=".",
    scanner="selenium",
    # scanner="api",
)


# end
