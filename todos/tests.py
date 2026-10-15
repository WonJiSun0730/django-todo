from django.contrib import admin
from django.test import Client, TestCase
from django.urls import reverse
from .models import Todo


class TodoTests(TestCase):
    def test_create_defaults_and_list(self):
        response = self.client.post(reverse('todos:create'), {'title': '과제 제출'})
        self.assertRedirects(response, reverse('todos:list'))
        todo = Todo.objects.get()
        self.assertFalse(todo.is_completed)
        self.assertEqual(todo.content, '')
        self.assertIsNotNone(todo.created_at)
        self.assertContains(self.client.get('/'), '과제 제출')

    def test_invalid_create_and_update(self):
        for title in ('', '   ', 'a' * 201):
            response = self.client.post(reverse('todos:create'), {'title': title})
            self.assertTrue(response.context['form'].errors)
        self.assertEqual(Todo.objects.count(), 0)
        todo = Todo.objects.create(title='유지')
        response = self.client.post(reverse('todos:update', args=[todo.pk]), {'title': ''})
        self.assertTrue(response.context['form'].errors)
        todo.refresh_from_db()
        self.assertEqual(todo.title, '유지')

    def test_update(self):
        todo = Todo.objects.create(title='이전')
        self.client.post(reverse('todos:update', args=[todo.pk]),
                         {'title': '변경', 'content': '상세 내용', 'is_completed': 'on'})
        todo.refresh_from_db()
        self.assertEqual((todo.title, todo.content, todo.is_completed), ('변경', '상세 내용', True))

    def test_completion_and_filters(self):
        todo = Todo.objects.create(title='테스트')
        url = reverse('todos:complete', args=[todo.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        for _ in range(2):
            self.client.post(url, {'is_completed': 'on'})
        todo.refresh_from_db()
        self.assertTrue(todo.is_completed)
        self.assertContains(self.client.get('/?status=completed'), 'todo completed')
        self.assertNotContains(self.client.get('/?status=active'), '<h2>테스트</h2>', html=True)
        self.client.post(url, {})
        todo.refresh_from_db()
        self.assertFalse(todo.is_completed)

    def test_delete_requires_post(self):
        todo = Todo.objects.create(title='삭제 대상')
        url = reverse('todos:delete', args=[todo.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Todo.objects.filter(pk=todo.pk).exists())
        self.client.post(url)
        self.assertFalse(Todo.objects.exists())

    def test_csrf_and_escaping(self):
        todo = Todo.objects.create(title='<script>alert(1)</script>')
        self.assertContains(self.client.get('/'), '&lt;script&gt;')
        client = Client(enforce_csrf_checks=True)
        for url in (reverse('todos:create'), reverse('todos:update', args=[todo.pk]),
                    reverse('todos:delete', args=[todo.pk]), reverse('todos:complete', args=[todo.pk])):
            self.assertEqual(client.post(url, {'title': '임의 변경'}).status_code, 403)

    def test_missing_and_admin(self):
        for name in ('update', 'delete'):
            self.assertEqual(self.client.get(reverse('todos:' + name, args=[999])).status_code, 404)
        self.assertEqual(self.client.post(reverse('todos:complete', args=[999])).status_code, 404)
        self.assertTrue(admin.site.is_registered(Todo))
