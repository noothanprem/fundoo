from django.test import TestCase

class TestCalls(TestCase):
    def test_call_view_denies_anonymous(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/login/google/?next=%2F')
[...]