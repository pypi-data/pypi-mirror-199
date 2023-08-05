import json
import re
from pathlib import Path

import pytest
from dirty_equals import HasLen, IsPartialDict, IsStr, IsList, Contains, HasAttributes
from pymultirole_plugins.v1.schema import Document, Annotation
from pytest_check import check

from pyprocessors_afp_entities.afp_entities import (
    AFPEntitiesProcessor,
    AFPEntitiesParameters,
    ConsolidationType,
    group_annotations,
    is_suspicious,
)


def test_model():
    model = AFPEntitiesProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AFPEntitiesParameters


# Arrange
@pytest.fixture
def original_doc():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


# Arrange
@pytest.fixture
def original_doc_en():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_en-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


def by_linking(a: Annotation):
    if a.terms:
        links = sorted({t.lexicon.split("_")[0] for t in a.terms})
        return "+".join(links)
    else:
        return "candidate"


def test_afp_entities_fr(original_doc):
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso.annotations, by_linking)
    assert len(conso_groups["candidate"]) == 8
    assert len(conso_groups["person"]) == 2
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Frank Garnier",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        IsPartialDict(
            label="AFPPerson",
            text="Werner Baumann",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=2,
    )
    assert len(conso_groups["wikidata"]) == 10
    assert len(conso_groups["location+wikidata"]) == 1
    assert len(conso_groups["organization+wikidata"]) == 2


def test_afp_entities_whitelist():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test-whitelist2.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso.annotations, by_linking)
    assert len(conso_groups["candidate"]) == 2
    assert len(conso_groups["person"]) == 2
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Máxima des Pays-Bas",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        IsPartialDict(
            label="AFPPerson",
            text="Lil Nas X",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=2,
    )
    assert len(conso_groups["location+wikidata"]) == 10
    assert len(conso_groups["organization+wikidata"]) == 3
    assert len(conso_groups["person+wikidata"]) == 1
    assert len(conso_groups["wikidata"]) == 1
    assert len(conso_groups["location"]) == 2


def test_afp_entities_suspicious():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_es-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert len(conso.annotations) < len(original_doc.annotations)
    for a in conso.annotations:
        assert not is_suspicious(a)


def test_afp_entities_en(original_doc_en):
    # linker
    doc = original_doc_en.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )


def get_bug_documents(bug):
    datadir = Path(__file__).parent / "data"
    docs = []
    for bug_file in datadir.glob(f"{bug}*.json"):
        with bug_file.open("r") as fin:
            doc = json.load(fin)
            doc['identifier'] = bug_file.stem
            docs.append(Document(**doc))
    return docs


# [AFP] "Elisabeth Borne" is not linked to its AFP referential identifier
def test_SHERPA_1735():
    docs = get_bug_documents("SHERPA-1735")
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process(docs, parameters)
    doc1 = next((d for d in docs if d.identifier.endswith("-1")))
    assert doc1.annotations == Contains(HasAttributes(label="AFPPerson", text="Elisabeth Borne"))


# [AFP] Sometimes the wikidata ID is not present in the output despite the fact that the named entity is extracted
# individually by Entity-fishing
def test_SHERPA_1741():
    docs = get_bug_documents("SHERPA-1741")
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process(docs, parameters)

    # El mafioso más buscado de Italia, el siciliano Matteo Messina Denaro
    doc1 = next((d for d in docs if d.identifier.endswith("-1")))
    italia = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc1.annotations if a.text == "Italia")
    with check:
        assert italia == IsPartialDict(label="AFPLocation", text="Italia",
                                       terms=Contains(
                                           # IsPartialDict(lexicon="wikidata"),
                                           IsPartialDict(lexicon="location",
                                                         identifier='afplocation:99')))

    # dijo este viernes a la radio France Inter el embajador francés
    doc2 = next((d for d in docs if d.identifier.endswith("-2")))
    france_inter = next(
        a.dict(exclude_none=True, exclude_unset=True) for a in doc2.annotations if a.text == "France Inter")
    with check:
        assert france_inter == IsPartialDict(label="AFPOrganization", text="France Inter",
                                             terms=Contains(IsPartialDict(lexicon="wikidata"),
                                                            IsPartialDict(lexicon="organization",
                                                                          identifier='afporganization:4251')))

    # Mayra Goulart, profesora de Ciencias Políticas de la Universidad Federal de Rio de Janeiro
    doc3 = next((d for d in docs if d.identifier.endswith("-3")))
    universidad = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc3.annotations if
                       a.text == "Universidad Federal de Rio de Janeiro")
    with check:
        assert universidad == IsPartialDict(label="Organization", text="Universidad Federal de Rio de Janeiro",
                                            terms=IsList(IsPartialDict(lexicon="wikidata"),
                                                         length=1))

    # Especialmente expuesta se encuentran las ciudades de Jekabpils y Plavinas
    doc4 = next((d for d in docs if d.identifier.endswith("-4")))
    plavinas = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc4.annotations if
                    a.text == "Plavinas")
    with check:
        assert plavinas == IsPartialDict(label="Location", text="Plavinas")

    # afirmó la internacional francesa Alice Finot
    doc5 = next((d for d in docs if d.identifier.endswith("-5")))
    alice_finot = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc5.annotations if
                       a.text == "Alice Finot")
    with check:
        assert alice_finot == IsPartialDict(label="AFPPerson", text="Alice Finot",
                                            terms=Contains(
                                                # IsPartialDict(lexicon="wikidata"),
                                                IsPartialDict(lexicon="person",
                                                              identifier='afpperson:1888395')
                                            ))


# [AFP] Entities labelled as Witness should not be present in the final output
def test_SHERPA_1742():
    docs = get_bug_documents("SHERPA-1742")
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process(docs, parameters)

    for doc in docs:
        forbidden = [a for a in doc.annotations if a.labelName in ["witness", 'loc_org', 'signature']]
        assert forbidden == HasLen(0)


# [AFP] Some whitelisted entities are not linked to their kb counterpart
def test_SHERPA_1761():
    docs = get_bug_documents("SHERPA-1761")
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    reina_maxima = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
                        a.text == "reina Máxima")
    with check:
        assert reina_maxima == IsPartialDict(label="AFPPerson", text="reina Máxima",
                                             terms=Contains(
                                                 IsPartialDict(lexicon="person",
                                                               identifier='afpperson:93542')
                                             ))
