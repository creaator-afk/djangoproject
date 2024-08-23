from django.test import TestCase
from user.models import User


# Unit test
class UserModelTestCase(TestCase):
    def test_user_model_case(self):
        user = User.objects.create(name='Test User',password="pass")
        self.assertEqual(user.name,"Test User")
        self.assertEqual(user.password,"pass")

