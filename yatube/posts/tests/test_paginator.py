from django.test import TestCase, Client
from ..models import Post, Group, User
from django.urls import reverse
from django.conf import settings
import math
from django.core.cache import cache


class PaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание2',
        )
        cls.all_posts = 19
        cls.post = []
        for i in range(cls.all_posts):
            cls.post.append(
                Post(
                    author=cls.user,
                    group=cls.group,
                    text=f'Тестовый пост {i}',))
        Post.objects.bulk_create(cls.post)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cache.clear()

    def test_index_correct_context_paginator(self):
        """Проверка paginator index: количество
        постов на первой странице равно 10. """
        response = self.guest_client.get(reverse(settings.NAME_INDEX))
        self.assertEqual(len(response.context['page_obj']),
                         settings.POSTS_PER_PAGE)

    def test_index_correct_context_paginator(self):
        """Проверка paginator index: количество
        постов на последней странице """
        response = self.guest_client.get(reverse(settings.NAME_INDEX)
                                         + '?page=2')
        self.assertEqual(len(response.context['page_obj']),
                         self.all_posts % settings.POSTS_PER_PAGE)

    def test_paginator_correct(self):
        """Проверка paginator group_list и profile"""
        num_pages = math.ceil(self.all_posts
                              / settings.POSTS_PER_PAGE)
        urls = {
            settings.NAME_GROUP_LIST: self.group.slug,
            settings.NAME_PROFILE: self.user,
        }
        for url, args in urls.items():
            reverse_name = reverse(url, args={args})
            with self.subTest(reverse_name=reverse_name):
                if self.all_posts <= settings.POSTS_PER_PAGE:
                    response = self.guest_client.get(reverse_name)
                    self.assertEqual(len(response.context['page_obj']),
                                     settings.POSTS_PER_PAGE)
                reverse_name_page = (
                    f'{reverse_name}?page={num_pages}')
                response = self.guest_client.get(reverse_name_page)
                self.assertEqual(len(
                                 response.context['page_obj']),
                                 self.all_posts
                                 - settings.POSTS_PER_PAGE * (num_pages - 1)
                                 )
