import json
import unittest
from unittest.mock import patch

from src.simple_password.get.simple_password_get import generate_simple_password, PW_SYMBOLS_LIST, handler


# pylint:disable=too-many-locals
class SimplePasswordGet(unittest.TestCase):

    @patch("src.simple_password.get.simple_password_get.Faker.unique")
    @patch("src.simple_password.get.simple_password_get.secrets")
    def test_generate_simple_password(self, mock_secrets, mock_faker):
        mock_faker.color_name.side_effect = ["blue", "green", "yellow"]
        mock_faker.element.side_effect = ["tin", "cobalt", "helium"]
        mock_faker.animal.side_effect = ["fox", "badger", "starfish"]
        mock_secrets.randbelow.side_effect = [0, 18, 2, 0, 1, 55]
        mock_secrets.SystemRandom.sample.side_effect = ["_", "*", "!"]
        # generate three random simple passwords
        simple_password1 = generate_simple_password()
        simple_password2 = generate_simple_password()
        simple_password3 = generate_simple_password()
        # check the passwords are as expected, given mocked values
        self.assertEqual("BLUE_tin_fox18", simple_password1)
        self.assertEqual("green*cobalt*BADGER0", simple_password2)
        self.assertEqual("yellow!HELIUM!starfish55", simple_password3)
        # check that the passwords are different to each other
        self.assertNotEqual(simple_password1, simple_password2)
        self.assertNotEqual(simple_password2, simple_password3)
        self.assertNotEqual(simple_password3, simple_password1)
        simple_passwords = [simple_password1, simple_password2, simple_password3]
        for simple_pw in simple_passwords:
            # check the password is a string
            self.assertTrue(type(simple_pw), str)
            # check that the length of the string is >= 8
            self.assertTrue(len(simple_pw) >= 8)
            # check that the password contains only symbols from the approved PW_SYMBOLS_LIST
            symbols = [c for c in simple_pw if c in PW_SYMBOLS_LIST]
            self.assertEqual(len(symbols), 2)
            # check that the password contains lowercase letters
            contains_uppercase = any(c.islower() and c.isalpha() for c in simple_pw)
            self.assertTrue(contains_uppercase)
            # check that the password contains uppercase letters
            contains_uppercase = any(c.isupper() and c.isalpha() for c in simple_pw)
            self.assertTrue(contains_uppercase)
            # check that the password contains numbers
            self.assertTrue(any(c.isdigit() for c in simple_pw))

    @patch("src.simple_password.get.simple_password_get.Faker.unique")
    @patch("src.simple_password.get.simple_password_get.secrets")
    def test_success__admin_generate_password(self, mock_secrets, mock_faker):
        mock_faker.color_name.return_value = "darkred"
        mock_faker.element.return_value = "oxygen"
        mock_faker.animal.return_value = "lion"
        mock_secrets.randbelow.side_effect = [1, 99]
        mock_secrets.SystemRandom.sample.return_value = "-"

        expected_simple_pw = "darkred-OXYGEN-lion99"

        response = handler({}, {})

        self.assertEqual(response["statusCode"], 200)
        simple_password = json.loads(response["body"])["simple_password"]
        self.assertEqual(expected_simple_pw, simple_password)
