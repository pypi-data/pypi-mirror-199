#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Synonym Generation for Ontologies """


import pandas as pd
from baseblock import BaseObject
from pandas import DataFrame

from owl_builder.autosyns.svc import GenerateEnglishInflections
from owl_builder.autotaxo.bp import AutoTaxoOrchestrator


class AutoSynsOrchestrator(BaseObject):
    """ Orchestrate Synonym Generation for Ontologies """

    def __init__(self):
        """ Change Log:

        Created:
            20-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/5

        """
        BaseObject.__init__(self, __name__)
        self._find_inflections = GenerateEnglishInflections().process

    def _keyterms(self,
                  input_text: str) -> list:
        if ' ' not in input_text:
            return [input_text]

        svc = AutoTaxoOrchestrator()
        keyterms = svc.keyterms(input_text,
                                use_keyterms=True,
                                use_ngrams=True,
                                use_nounchunks=True,
                                use_terms=True)

        unigrams = set()
        for keyterm in keyterms:
            [unigrams.add(x) for x in keyterm.split()]

        return sorted(unigrams)

    def process(self,
                input_text: str) -> list:
        master = []

        for keyterm in self._keyterms(input_text):
            result = self._find_inflections(keyterm)
            if result and len(result):
                master.append(f"{keyterm}~{','.join(result)}")

        return master
