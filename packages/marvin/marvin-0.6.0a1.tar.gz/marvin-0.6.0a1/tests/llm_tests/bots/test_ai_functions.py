from marvin import ai_fn
from marvin.utilities.tests import assert_llm


class TestAIFunctions:
    def test_rng(self):
        @ai_fn
        def rng() -> float:
            """generate a random number between 0 and 1"""

        x = rng()
        assert isinstance(x, float)
        assert 0 <= x <= 1

    def test_rng_with_limits(self):
        @ai_fn
        def rng(min: float, max: float) -> float:
            """generate a random number between min and max"""

        x = rng(20, 21)
        assert 20 <= x <= 21

    def test_list_of_fruits(self):
        @ai_fn
        def list_fruits(n: int) -> list[str]:
            """generate a list of n fruits"""

        x = list_fruits(3)
        assert isinstance(x, list)
        assert len(x) == 3
        assert all(isinstance(fruit, str) for fruit in x)
        assert_llm(x, "a list of fruits")

    def test_list_of_fruits_calling_ai_fn_with_no_args(self):
        @ai_fn()
        def list_fruits(n: int) -> list[str]:
            """generate a list of n fruits"""

        x = list_fruits(3)
        assert isinstance(x, list)
        assert len(x) == 3
        assert all(isinstance(fruit, str) for fruit in x)
        assert_llm(x, "a list of fruits")

    def test_generate_fake_people_data(self):
        @ai_fn
        def fake_people(n: int) -> list[dict]:
            """
            Generates n examples of fake data representing people,
            each with a name and an age.
            """

        x = fake_people(3)
        assert isinstance(x, list)
        assert len(x) == 3
        assert all(isinstance(person, dict) for person in x)
        assert all("name" in person for person in x)
        assert all("age" in person for person in x)
        assert_llm(x, "a list of fake people")

    def test_generate_rhyming_words(self):
        @ai_fn
        def rhymes(word: str) -> str:
            """generate a word that rhymes with the given word"""

        x = rhymes("blue")
        assert isinstance(x, str)
        assert x != "blue"
        assert_llm(x, "a word that rhymes with blue")

    def test_generate_rhyming_words_with_n(self):
        @ai_fn
        def rhymes(word: str, n: int) -> list[str]:
            """generate a word that rhymes with the given word"""

        x = rhymes("blue", 3)
        assert isinstance(x, list)
        assert len(x) == 3
        assert all(isinstance(word, str) for word in x)
        assert all(word != "blue" for word in x)
        assert_llm(x, "a list of words that rhyme with blue")


class TestBool:
    def test_bool_response(self):
        @ai_fn
        def is_blue(word: str) -> bool:
            """returns True if the word is blue"""

        x = is_blue("blue")
        assert isinstance(x, bool)
        assert x is True

        y = is_blue("green")
        assert isinstance(y, bool)
        assert y is False

    def test_bool_response_issue_55(self):
        # hinting `True` or `False` in a nested bool broke JSON parsing that
        # expected lowercase
        @ai_fn
        def classify_sentiment(messages: list[str]) -> list[bool]:
            """
            Given a list of messages, classifies each one as
            positive (True) or negative (False) and returns
            a corresponding list
            """

        result = classify_sentiment(["i love pizza", "i hate pizza"])
        assert result == [True, False]
