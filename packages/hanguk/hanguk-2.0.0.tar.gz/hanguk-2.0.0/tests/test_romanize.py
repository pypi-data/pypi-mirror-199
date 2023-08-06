import hanguk


def test_romanize():
    assert hanguk.Hanguk('생각').read() == 'saenggak'
