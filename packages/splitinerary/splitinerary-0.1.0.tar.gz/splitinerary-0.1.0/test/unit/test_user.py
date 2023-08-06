from splitinerary import User

import unittest


class TestUser(unittest.TestCase):
    def test_create_object_success(self):
        # arrange
        first_name = "Tim"
        last_name = "Paine"
        email = "tkp2108@columbia.edu"
        # act
        user = User(first_name, last_name, email)
        # assert
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)

    def test_get_email_success(self):
        # arrange
        first_name = "Tim"
        last_name = "Paine"
        expected_email = "tkp2108@columbia.edu"
        user = User(first_name, last_name, expected_email)
        # act
        email = user.get_email()
        # assert
        self.assertEqual(email, expected_email)

    def test_str_success(self):
        # arrange
        first_name = "Tim"
        last_name = "Paine"
        email = "tkp2108@columbia.edu"
        user = User(first_name, last_name, email)
        expected_str = f'{first_name} {last_name}({email})'
        # act

        # assert
        self.assertEqual(str(user), expected_str)

    def test_eq_success(self):
        # arrange
        first_name = "Tim"
        last_name = "Paine"
        email = "tkp2108@columbia.edu"
        user1 = User(first_name, last_name, email)

        first_name = "Thomas"
        last_name = "P"
        email = "tkp2108@columbia.edu"
        user2 = User(first_name, last_name, email)
        # act

        # assert
        self.assertTrue((user1 == user2))

    def test_hash_success(self):
        # arrange
        first_name = "Tim"
        last_name = "Paine"
        email = "tkp2108@columbia.edu"
        user = User(first_name, last_name, email)

        # act
        hashed_user = hash(str(user))
        # assert
        self.assertEqual(hashed_user, hash(user))
