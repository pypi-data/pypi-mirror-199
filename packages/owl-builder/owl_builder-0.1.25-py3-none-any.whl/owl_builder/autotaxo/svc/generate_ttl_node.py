#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate an Ontology Graph Node in TTL Format """


from functools import lru_cache
from typing import Optional

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from owl_builder.autotaxo.dmo import OpenAIKeytermExtractor
from owl_builder.autosyns.svc import GenerateEnglishInflections


class GenerateTTLNode(BaseObject):
    """ Generate an Ontology Graph Node in TTL Format """

    def __init__(self):
        """
        Created:
            28-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/8
        """
        BaseObject.__init__(self, __name__)
        self._generate_inflections = GenerateEnglishInflections().process

    @staticmethod
    def _to_identifier(entity_name: str) -> str:

        entity_name = entity_name.upper().strip()
        entity_name = entity_name.replace(' ', '_')

        for item in ["'"]:
            entity_name = entity_name.replace(item, "").strip()

        return entity_name

    def _see_alsos(self,
                   entity_name: str) -> Optional[str]:

        results = self._generate_inflections(entity_name)
        if not results:
            return None

        see_alsos = []
        for i in range(len(results)):

            see_also = """rdfs:seeAlso "#TERM" #DELIM"""
            see_also = see_also.replace('#TERM', results[i])

            def get_delim() -> str:
                if i + 1 < len(results):
                    return ';'
                return '.'

            see_also = see_also.replace('#DELIM', get_delim())
            see_alsos.append(see_also)

    def process(self,
                entity_name: str,
                namespace: Optional[str] = "http://graffl.ai/test") -> str:

        template = """
###  #NAMESPACE#IDENTIFIER

:#IDENTIFIER rdf:type owl:Class ;
         
    rdfs:label "#LABEL" #LDELIM
    #SYNONYMS
        """

        node = template.replace('#NAMESPACE', namespace)
        node = node.replace('#IDENTIFIER', self._to_identifier(entity_name))
        node = node.replace('#LABEL', entity_name)

        see_alsos = self._see_alsos(entity_name)
        if see_alsos:
            node = node.replace('#LDELIM', ';')
            node = node.replace('#SYNONYMS', '\n'.join(see_alsos))
        else:
            node = node.replace('#LDELIM', '.')

        return node
