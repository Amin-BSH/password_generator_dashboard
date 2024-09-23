import random
import string
from abc import ABC, abstractmethod
from typing import Optional, List

import nltk

nltk.download("words")


class PasswordGenerator(ABC):
    """
    Base class for generating passwords.
    """

    @abstractmethod
    def generate(self) -> str:
        """
        Subclasses should override this method to generate a password.

        Returns:
            str: The generated password.
        """
        pass


class RandomPasswordGenerator(PasswordGenerator):
    def __init__(
        self,
        length: int = 10,
        include_number: bool = True,
        include_symbol: bool = False,
    ) -> None:
        """
        Initializes a random password generator.

        Args:
            length (int): Length of the generated password.
            include_number (bool): Whether to include digits in the password.
            include_symbol (bool): Whether to include symbols in the password.
        """
        self.length: int = length
        self.include_number: bool = include_number
        self.include_symbol: bool = include_symbol

        self.characters: str = string.ascii_letters

        if include_number:
            self.characters += string.digits
        if include_symbol:
            self.characters += string.punctuation

    def generate(self) -> str:
        """
        Generates a random password.

        Returns:
            str: The generated password.
        """
        return "".join(random.choice(self.characters) for _ in range(self.length))


class MemorablePasswordGenerator(PasswordGenerator):
    def __init__(
        self,
        num_of_words: int = 5,
        separator: str = "-",
        capitalized_all_words: bool = False,
        capitalized_randomly: bool = False,
        vocabulary: Optional[List[str]] = [],
    ) -> None:
        """
        Initializes a memorable password generator.

        Args:
            num_of_words (int): Number of words in the password.
            separator (str): Separator between words.
            capitalized_all_words (bool): Whether all words should be capitalized.
            capitalized_randomly (bool): Whether words should be randomly capitalized.
            vocabulary (Optional[List[str]]): List of words to choose from.
        """
        if vocabulary is None:
            vocabulary = nltk.corpus.words.words()
        self.num_of_words: int = num_of_words
        self.separator: str = separator
        self.capitalized_all_words: bool = capitalized_all_words
        self.capitalized_randomly: bool = capitalized_randomly
        self.vocabulary: List[str] = vocabulary

    def generate(self) -> str:
        """
        Generates a memorable password.

        Returns:
            str: The generated password.
        """
        passwords_words = [
            random.choice(self.vocabulary) for _ in range(self.num_of_words)
        ]
        if self.capitalized_all_words:
            passwords_words = list(map(lambda x: x.upper(), passwords_words))
        if self.capitalized_randomly:
            passwords_words = list(
                map(
                    lambda x: x.upper() if random.choice([True, False]) else x.lower(),
                    passwords_words,
                )
            )
        if self.separator:
            return self.separator.join(passwords_words)
        else:
            return "".join(passwords_words)


class PinCodeGenerator(PasswordGenerator):
    """
    Class to generate a numeric pin code.
    """

    def __init__(self, length: int = 4) -> None:
        """
        Initializes a numeric pin code generator.

        Args:
            length (int): Length of the generated pin code.
        """
        self.length: int = length

    def generate(self) -> str:
        """
        Generates a numeric pin code.

        Returns:
            str: The generated pin code.
        """
        return "".join(random.choice(string.digits) for _ in range(self.length))


def test_random_password_generator() -> None:
    sample = RandomPasswordGenerator()
    print("Random Password:", sample.generate())


def test_memorable_password_generator() -> None:
    memorable_gen = MemorablePasswordGenerator(
        num_of_words=4,
        separator="-",
        capitalized_all_words=True,
        vocabulary=["Amin", "jj", "Erma"],
    )

    password = memorable_gen.generate()
    print("Memorable Password:", password)
    assert len(password.split("-")) == 4
    assert all(word[0].isupper() for word in password.split("-"))


def test_pin_code_generator():
    pin_gen = PinCodeGenerator(length=4)
    pin = pin_gen.generate()
    print("PIN Code:", pin)
    assert len(pin) == 4
    assert all(char in string.digits for char in pin)


if "__main__" == __name__:
    test_random_password_generator()
    test_memorable_password_generator()
    test_pin_code_generator()
