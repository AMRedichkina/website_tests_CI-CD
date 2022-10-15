from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Group, Post, User
from django.core.cache import cache

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cache.clear()

    def test_models_have_correct_object_names_group(self):
        """Проверяем, что у моделей корректно работает __str__"""
        group = PostModelTest.group
        expected_object_name = group.title
        with self.subTest(group=group):
            self.assertEqual(expected_object_name, self.group.title)
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        with self.subTest(post=post):
            self.assertEqual(expected_object_name, self.post.text[:15])

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = PostModelTest.group
        verbose = group._meta.get_field('title').verbose_name
        self.assertEqual(verbose, 'Группа')

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = PostModelTest.group
        help_text = group._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Группа, к которой будет относиться пост')
