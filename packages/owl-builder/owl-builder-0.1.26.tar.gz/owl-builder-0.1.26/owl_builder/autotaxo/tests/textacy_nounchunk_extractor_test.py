from owl_builder.autotaxo.dmo import TextacyNounChunkExtractor
from owl_builder.autotaxo.dto import load_model

model = load_model()


def test_component():

    input_text = """
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.
    """.strip()

    dmo = TextacyNounChunkExtractor(model)
    assert dmo

    results = dmo.process(input_text=input_text,
                          min_freq=1)

    print(results)


def main():
    test_component()


if __name__ == "__main__":
    main()
