from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteEditDelete(TestCase):
    NOTE_TITLE = 'Заголовок'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'note_slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            author=cls.author,
        )
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.list_url = reverse('notes:list')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_note_in_list_for_author(self):
        """Тест отображения заметки для автора"""
        response = self.author_client.get(self.list_url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_in_list_for_another_user(self):
        """Тест отображения заметки для читателя"""
        response = self.reader_client.get(self.list_url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_create_note_page_contains_form(self):
        """Тест отображения формы на странице создания"""
        response = self.author_client.get(self.add_url)
        self.assertIn('form', response.context)

    def test_edit_note_page_contains_form(self):
        """Тест отображения формы на странице редактирования"""
        response = self.author_client.get(self.edit_url)
        self.assertIn('form', response.context)
