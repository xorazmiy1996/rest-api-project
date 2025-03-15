import unittest
from flask import json
from app import create_app
from db import db

class StoreListTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Ma'lumotlar bazasi jadvallarini yarating


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()   # Ma'lumotlar bazasi jadvallarini o'chiring

    # GET metodini test qilish
    def test_get_stores(self):
        response = self.client.get('/store')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)  # Javob ro'yxat ekanligini tekshiring

    # POST metodini test qilish
    def test_post_store(self):
        store_data = {
            'name': 'Test Store'  # StoreSchema ga asoslangan boshqa zarur maydonlarni qo'shing
        }
        response = self.client.post('/store', json=store_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', json.loads(response.data))  # Javobda 'name' maydoni borligini tekshiring

        # Takroriy do'kon nomi bilan POST metodini test qilish

    def test_post_duplicate_store(self):
        store_data = {
            'name': 'Duplicate Store'
        }
        self.client.post('/store', json=store_data)  # Birinchi post muvaffaqiyatli bo'lishi kerak
        response = self.client.post('/store', json=store_data)  # Ikkinchi post muvaffaqiyatsiz bo'lishi kerak
        self.assertEqual(response.status_code, 400)
        self.assertIn('A store with that name already exists.', str(response.data))
