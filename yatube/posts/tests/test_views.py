from django.test import TestCase, Client
from ..models import Post, Group, User, Follow, Comment
from django.urls import reverse
from django import forms
from ..forms import PostForm
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
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
            image=SimpleUploadedFile(
                name='small.gif',
                content=(
                    b'\x47\x49\x46\x38\x39\x61\x02\x00'
                    b'\x01\x00\x80\x00\x00\x00\x00\x00'
                    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                    b'\x0A\x00\x3B'
                ),
                content_type='image/gif'
            )
        )

        cls.group2 = Group.objects.create(
            title='Тестовая группа2',
            slug='test-slug2',
            description='Тестовое описание2',
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cache.clear()

    def test_urls_uses_correct_template(self):
        """Проверка namespace:name.
        View функции используют соответствующие шаблоны."""
        templates_url_names_not_auth = {
            reverse(settings.NAME_INDEX): settings.HTML_INDEX,
            reverse(settings.NAME_PROFILE,
                    kwargs={'username': 'auth'}): settings.HTML_PROFILE,
            reverse(settings.NAME_POST_DETAIL,
                    kwargs={'post_id': '1'}): settings.HTML_POST_DELAIL,
            reverse(settings.NAME_GROUP_LIST,
                    kwargs={'slug': 'test-slug'}): settings.HTML_GROUP_LIST,
        }
        templates_url_names_auth = {
            reverse(settings.NAME_POST_CREATE): settings.HTML_POST_CREATE,
        }
        templates_url_names_author = {
            reverse(settings.NAME_POST_EDIT,
                    kwargs={'post_id': '1'}): settings.HTML_POST_EDIT,
        }
        for reverse_name, template in templates_url_names_not_auth.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
        for reverse_name, template in templates_url_names_auth.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        for reverse_name, template in templates_url_names_author.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""

        response = self.guest_client.get(reverse(settings.NAME_INDEX))
        post = response.context['page_obj'][0]
        test_post_tuple = (
            (post.author.username, 'auth'),
            (post.text, 'Тестовый пост'),
            (post.image.name, self.post.image.name),
        )
        for field, expectation in test_post_tuple:
            with self.subTest(field=field):
                self.assertEqual(field, expectation)

    def test_group_list_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse(settings.NAME_GROUP_LIST,
                                         kwargs={'slug': 'test-slug'}))
        group = response.context['group']
        post = response.context["page_obj"][0]
        test_group_and_post_tuple = (
            (group.title, 'Тестовая группа'),
            (group.slug, 'test-slug'),
            (group.description, 'Тестовое описание'),
            (post.author.username, 'auth'),
            (post.text, 'Тестовый пост'),
            (post.image.name, self.post.image.name),
        )
        for field, expectation in test_group_and_post_tuple:
            with self.subTest(field=field):
                self.assertEqual(field, expectation)

    def test_group_list_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse(settings.NAME_PROFILE,
                                         kwargs={'username': self.user}))
        author = response.context['author']
        count = response.context['count']
        post = response.context["page_obj"][0]
        test_author_tuple = (
            (author.username, 'auth'),
            (count, author.posts.count),
            (post.image.name, self.post.image.name),
        )
        for field, expectstion in test_author_tuple:
            with self.subTest(field=field):
                self.assertEqual(field, expectstion)

    def test_post_detail_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(settings.NAME_POST_DETAIL,
                    kwargs={'post_id': self.post.id}))
        post = response.context['post']
        count = response.context['count']
        title = response.context['title']
        test_author_tuple = (
            (post.author.username, 'auth'),
            (post.text, 'Тестовый пост'),
            (count, post.author.posts.count),
            (title, post.text[0:30]),
            (post.image.name, self.post.image.name),
        )
        for field, expectstion in test_author_tuple:
            with self.subTest(field=field):
                self.assertEqual(field, expectstion)

    def test_post_create_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        reverse_url = reverse(settings.NAME_POST_CREATE)
        response = self.authorized_client.get(reverse_url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        reverse_url = reverse(settings.NAME_POST_EDIT,
                              kwargs={'post_id': self.post.pk})
        response = self.authorized_client.get(reverse_url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

        post_id = response.context['post_id']
        self.assertEqual(post_id, str(self.post.id))

    def test_create_new_post_index(self):
        """Проверка, что созданный пост на странице index"""
        # Заполняем форму
        form_data = {
            'text': 'Текст',
            'group': self.group.id,
        }
        self.authorized_client.post(
            reverse('posts:post_create'), form_data, follow=True)
        response = self.guest_client.get(reverse(settings.NAME_INDEX))
        r = response.context['page_obj'][0]
        self.assertEqual(r.text, form_data['text'])

        #  Заходим на главную страницу, проверяем есть ли пост
        response = self.guest_client.get(reverse(settings.NAME_INDEX))
        post = response.context["page_obj"][0]
        self.assertEqual(post.text, form_data['text'])

        #  Заходим на страницу выбранной группы, проверяем есть ли пост
        response = self.guest_client.get(reverse(settings.NAME_GROUP_LIST,
                                         kwargs={'slug': 'test-slug'}))
        post = response.context["page_obj"][0]
        self.assertEqual(post.text, form_data['text'])

        #  Заходим в профайл пользователя, проверяем есть ли пост
        response = self.guest_client.get(
            reverse(settings.NAME_PROFILE,
                    kwargs={'username': 'auth'}))
        post = response.context["page_obj"][0]
        self.assertEqual(post.text, form_data['text'])

        # Проверяем, что пост не попал в другую группу
        response = self.guest_client.get(
            reverse(settings.NAME_GROUP_LIST,
                    kwargs={'slug': 'test-slug2'}))
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_create_new_comment(self):
        """Проверка, что создается комментарий на странице деталей поста"""
        form_data = {
            'text': 'Текст комментария',
        }
        self.authorized_client.post(
            reverse(settings.NAME_ADD_COMMENT,
                    kwargs={'post_id': self.post.id}),
            form_data, follow=True)
        self.authorized_client.get(reverse(settings.NAME_POST_DETAIL,
                                   kwargs={'post_id': self.post.id}))
        self.assertTrue(
            Comment.objects.filter(text=form_data['text']).exists())


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост_кэш',
        )

    def setUp(self):
        self.guest_client = Client()
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cache.clear()

    def test_cache(self):
        """Тестирования кэш страницы index"""
        response = self.guest_client.get(reverse(settings.NAME_INDEX))
        post = response.context.get('page_obj')
        self.assertIn(self.post, post)
        temp = response.content
        self.post.delete()
        self.assertEqual(temp, response.content)
        cache.clear()
        temp = response.content
        self.assertEqual(temp, response.content)


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='follower')
        cls.author = User.objects.create_user(username='following')
        cls.post = Post.objects.create(
            text='Тест для подписчика',
            author=cls.author,
        )

    def setUp(self):
        self.follower_client = Client()
        self.follower_client.force_login(self.user)
        self.following_client = Client()
        self.following_client.force_login(self.author)

    def test_authorized_user_can_subscribe(self):
        """Авторизованный пользователь может
        подписываться на других пользователей"""
        self.follower_client.get(reverse(settings.NAME_FOLLOWER,
                                         kwargs={'username': self.author}))
        response = self.follower_client.get(
            reverse(settings.NAME_FOLLOWER_INDEX))
        author = response.context['page_obj'][0].author
        self.assertEqual(author, self.author)

    def test_authorized_user_can_delete(self):
        """Авторизованный пользователь может
        удалять пользователей из подписок"""
        self.follower_client.get(reverse(settings.NAME_UNFOLLOWER,
                                         kwargs={'username': self.author}))
        response = self.follower_client.get(
            reverse(settings.NAME_FOLLOWER_INDEX))
        self.assertNotContains(response, self.author)

    def test_follow_new_post(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан и не появляется в ленте тех,
        кто не подписан"""
        Follow.objects.create(
            author=(User.objects.get(username='following')),
            user=(User.objects.get(username='follower')),
        )
        response = self.follower_client.get(
            reverse(settings.NAME_FOLLOWER_INDEX))
        post = response.context['page_obj'][0]
        self.assertEqual(post.text, self.post.text)
