# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from app import app
from etfs import Etf
from flask import render_template


@app.route("/")
def Index():
    all_etfs = Etf.query.all()
    print(all_etfs)
    return render_template("index.html", etfs=all_etfs)
