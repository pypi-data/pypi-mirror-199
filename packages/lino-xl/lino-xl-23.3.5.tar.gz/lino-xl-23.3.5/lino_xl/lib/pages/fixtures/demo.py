# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.utils import translation
from lino.api import rt, _
from lino.utils import Cycler
from lino.modlib.comments.fixtures.demo2 import lorem, short_lorem

welcome = _("""Welcome to our great website. We are proud to present
the best content about foo, bar and baz.
""")

BODIES = Cycler([lorem, short_lorem])


def objects():
    Node = rt.models.pages.Page
    nodes = [
        ("en", (
            ("index", "Home", welcome),
            (None, "First part", None),
            (None, "Second part", None),
            (None, "Third part", None),
        )),
        ("de", (
            ("index", "Startseite", welcome),
            ("eins", "Erster Teil", None),
            ("zwei", "Zweiter Teil", None),
        )),
        ("fr", (
            ("index", "Départ", welcome),
            ("un", "Première partie", None),
            ("deux", "Deuxième partie", None),
        )),
        ]

    for language, pages in nodes:
        if not language in rt.settings.SITE.language_dict:
            continue
        kwargs = dict(language=language)
        count = 0
        with translation.override(language):
            for ref, title, body in pages:
                kwargs.update(ref=ref)
                if body is None:
                    body = BODIES.pop()
                    for i in range(count):
                        body += BODIES.pop()
                p = Node(title=title, body=str(body), **kwargs)
                if ref == "index":
                    kwargs.update(parent=p)
                yield p
