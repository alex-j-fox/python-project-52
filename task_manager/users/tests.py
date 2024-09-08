from django.test import TestCase

from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='testuser',
                            password1='testpassword',
                            password2='testpassword',
                            first_name='testfirst',
                            last_name='testlast',
                            )

    def test_user_creation(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'testfirst')
        self.assertEqual(user.last_name, 'testlast')

    def test_user_get_updating(self):
        user = User.objects.get(username='testuser')
        user.first_name = 'newfirst'
        user.last_name = 'newlast'
        user.save()
        self.assertEqual(user.first_name, 'newfirst')
        self.assertEqual(user.last_name, 'newlast')

    def test_user_deletion(self):
        user = User.objects.get(username='testuser')
        user.delete()
        self.assertRaises(User.DoesNotExist, User.objects.get, username='testuser')

    def test_user_get(self):
        user = User.objects.get(username='testuser')
        found_user = User.objects.get(username='testuser')
        self.assertEqual(found_user, user)

    def test_user_password_comparison(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.password1, user.password2)

    # def test_user_creation_with_permissions(self):
    #     user = User.objects.get(username='testuser')
    #     self.assertTrue(user.has_perm('myapp.can_view_page'))
    #     self.assertFalse(user.has_perm('myapp.can_edit_page'))

    # def test_user_creation_with_groups(self):
    #     group = Group.objects.create(name='testgroup')
    #     user = User.objects.create_user(username='testuser')
    #     user.groups.add(group)
    #     self.assertIn(group, user.groups.all())
