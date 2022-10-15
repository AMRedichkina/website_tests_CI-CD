import shutil
import tempfile
from django.test import Client, TestCase, override_settings
from ..models import Post, Group, User, Comment
from ..forms import PostForm
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа2',
            slug='test-slug2',
            description='Тестовое описание2',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_authorized_client(self):
        """Проверка, что создаётся новая запись в базе данных"""
        count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': uploaded,
        }
        self.authorized_client.post(
            reverse(settings.NAME_POST_CREATE),
            form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                image='posts/small.gif',
            ).exists()
        )

    def test_new_post_anonim(self):
        """Проверка, что не создаётся новая запись,
        если ее создает анонимный пользователь"""
        count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        self.guest_client.post(
            reverse(settings.NAME_POST_CREATE),
            form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), count)

    def test_change_post(self):
        """Проверка, что происходит изменение текста поста в базе данных"""
        form_data = {
            'text': 'Текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse(settings.NAME_POST_EDIT,
                    kwargs={'post_id': self.post.id}),
            form_data,
            fallow=True)
        response = self.authorized_client.get(
            reverse(settings.NAME_POST_DETAIL,
                    kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context["post"].text,
                         form_data['text'])

    def test_change_post(self):
        """Проверка, что происходит изменение группы поста в базе данных"""
        form_data = {
            'text': self.post.text,
            'group': self.group2.id,
        }
        response = self.authorized_client.post(
            reverse(settings.NAME_POST_EDIT,
                    kwargs={'post_id': self.post.id}),
            form_data,
            fallow=True)
        response = self.authorized_client.get(
            reverse(settings.NAME_POST_DETAIL,
                    kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context["post"].text,
                         form_data['text'])

    def test_not_change_post_anonim(self):
        """Проверка, что пост не меняется,
        если редактирует аноним"""
        form_data = {
            'text': 'Текст',
            'group': self.group.id,
        }
        response = self.guest_client.post(
            reverse(settings.NAME_POST_EDIT,
                    kwargs={'post_id': self.post.id}),
            form_data,
            fallow=True)
        response = self.guest_client.get(
            reverse(settings.NAME_POST_DETAIL,
                    kwargs={'post_id': self.post.id}))
        self.assertNotEqual(response.context["post"].text, form_data['text'])

    def test_new_comment_not_authorized_client(self):
        """Проверка, что комментарий не создается неавт. пользователем"""
        count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый комментарий',
        }
        self.guest_client.post(
            reverse(settings.NAME_POST_DETAIL,
                    kwargs={'post_id': self.post.id}),
            form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), count + 1)
