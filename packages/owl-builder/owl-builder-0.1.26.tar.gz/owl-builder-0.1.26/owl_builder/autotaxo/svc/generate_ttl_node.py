#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate an Ontology Graph Node in TTL Format """


from functools import partial
from typing import Optional

from datetime import datetime
from baseblock import BaseObject
from baseblock import TextUtils

from owl_builder.autosyns.svc import GenerateEnglishInflections

from rdflib.graph import Graph
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS, XSD


class GenerateTTLNode(BaseObject):
    """ Generate an Ontology Graph Node in TTL Format """

    def __init__(self,
                 model_name: str = "gpt-4"):
        """ Change Log

        Created:
            28-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/8

        model_name (str, optional). defaults to "GPT-4"
        """
        BaseObject.__init__(self, __name__)
        self._model_name = model_name
        self._generate_inflections = partial(
            GenerateEnglishInflections().process,
            model=self._model_name)

    @staticmethod
    def _to_identifier(entity_name: str) -> str:

        entity_name = entity_name.upper().strip()
        entity_name = entity_name.replace(' ', '_')

        for item in ["'"]:
            entity_name = entity_name.replace(item, "").strip()

        return entity_name

    def _version(self) -> str:
        text = "Generated on #TIME using #MODEL"

        text = text.replace('#TIME', str(datetime.now())[:-10])
        text = text.replace('#MODEL', self._model_name.upper().strip())

        return text

    def process(self,
                entity_name: str,
                namespace: Optional[str] = "http://graffl.ai/test") -> str:

        entity_id = self._to_identifier(entity_name)
        entity_label = TextUtils.title_case(entity_name)

        synonyms = self._generate_inflections(input_text=entity_name)

        g = Graph()

        g.add((
            URIRef(f"{namespace}/{entity_id}"),
            RDF.type,
            OWL.Class
        ))

        g.add((
            URIRef(f"{namespace}/{entity_id}"),
            RDFS.label,
            Literal(entity_label, datatype=XSD.string)
        ))

        g.add((
            URIRef(f"{namespace}/{entity_id}"),
            OWL.versionInfo,
            Literal(self._version(), datatype=XSD.string)
        ))

        if synonyms and len(synonyms):
            for synonym in synonyms:
                g.add((
                    URIRef(f"{namespace}/{entity_id}"),
                    RDFS.seeAlso,
                    Literal(synonym, datatype=XSD.string)
                ))

        return g.serialize(format="turtle")
