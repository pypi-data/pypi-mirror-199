import json
from pathlib import Path

import pytest
from dirty_equals import HasLen, HasAttributes, IsList, IsPartialDict
from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_openai_completion.openai_completion import (
    OpenAICompletionProcessor,
    OpenAICompletionParameters,
    OpenAIModel, flatten_document,
)


def test_openai_completion_basic():
    model = OpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == OpenAICompletionParameters


def test_flatten_doc():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/complexdoc.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        flatten = flatten_document(doc)
        assert flatten == IsPartialDict(text=doc.text,
                                        title=doc.title,
                                        metadata_foo=doc.metadata['foo'],
                                        altTexts_0_name=doc.altTexts[0].name)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in OpenAIModel])
def test_openai_prompt(model):
    parameters = OpenAICompletionParameters(
        model=model,
        max_tokens=120, completion_altText="completion"
    )
    processor = OpenAICompletionProcessor()
    docs_with_prompts = [
        (Document(
            identifier="1",
            text="séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"}), "Peux tu écrire un article de presse concernant: $text"),
        (Document(
            identifier="2",
            text="j'habite dans une maison",
            metadata={"language": "fr"}), "Peux tu me donner des phrases similaires à: $text"),
        (Document(
            identifier="3",
            text="il est né le 21 janvier 2000",
            metadata={"language": "fr"}),
         "Peux tu me donner des phrases similaires en changeant le format de date à: $text"),
        (Document(
            identifier="4",
            text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
                Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
                L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
                « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
                Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
                Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
                Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
                « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
                Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
                Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
                """,
            metadata={"language": "fr"}), "Peux résumer dans un style journalistique le texte suivant: $text"),
        (Document(
            identifier="5",
            text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
            metadata={"language": "en"}),
         "Can you find the names of people, organizations and locations in the following text:\n\n $text")
    ]
    docs = []
    for doc, prompt in docs_with_prompts:
        parameters.prompt = prompt
        doc0 = processor.process([doc], parameters)[0]
        docs.append(doc0)
        assert doc0.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"en_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in OpenAIModel])
def test_openai_text(model):
    parameters = OpenAICompletionParameters(
        model=model,
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"fr_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
