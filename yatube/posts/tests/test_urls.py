from django.test import TestCase, Client
from ..models import Post, Group, User
from http import HTTPStatus
from django.conf import settings
from django.core.cache import cache


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            id='1'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cache.clear()

    def test_homepage(self):
        """Главная страница доступна"""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names_not_auth = {
            settings.URL_INDEX: settings.HTML_INDEX,
            settings.URL_PROFILE: settings.HTML_PROFILE,
            settings.URL_POST_DETAIL: settings.HTML_POST_DELAIL,
            settings.URL_GROUP_LIST: settings.HTML_GROUP_LIST,
        }
        templates_url_names_auth = {
            settings.URL_POST_CREATE: settings.HTML_POST_CREATE,
        }
        templates_url_names_author = {
            settings.URL_POST_EDIT: settings.HTML_POST_EDIT,
        }
        for address, template in templates_url_names_not_auth.items():
            with self.subTest(template=template):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

        for address, template in templates_url_names_auth.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

        for address, template in templates_url_names_author.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_author_edit_the_post(self):
        """Страница редактирования поста доступна автору"""
        response = self.authorized_client.get(settings.URL_POST_EDIT)
        self.assertEqual(response.status_code, 200)

    def test_just_author_edit_the_post(self):
        """Страница редактирования поста не доступна не авторам"""
        self.user2 = User.objects.create_user(username='HasNoName2')
        self.other_client = Client()
        self.other_client.force_login(self.user2)
        response = self.other_client.get(settings.URL_POST_EDIT)
        self.assertEqual(response.status_code, 302)

    def test_page_404(self):
        response = self.guest_client.get('/123/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
