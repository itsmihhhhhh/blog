from datetime import datetime
import unittest
from flask import request
from app import app, db, bcrypt
from app.models import User, Blog
from flask_login import current_user


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password(self):
        user = User(name='test', email='test@gmail.com', password='test123')
        self.assertTrue(bcrypt.check_password_hash(user.password, 'test123'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'wrongpw'))

    def test_follow(self):
        u1 = User(name='yiyi', email='yiyi@example.com', password='yiyi123')
        u2 = User(name='yoyo', email='yoyo@example.com', password='yoyo123')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().name, 'yoyo')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().name, 'yiyi')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)


    def test_create_post(self):
        u = User(name='yaya', email='yaya@gmail.com', password='yaya123')
        db.session.add(u)
        db.session.commit()

        b = Blog(title='test',body="a blog from yaya",author=u.id)
        db.session.add(b)
        db.session.commit()

        self.assertEqual(u.blog.first(), b)

    def test_delete_post(self):
        u = User(name='yaya', email='yaya@gmail.com', password='yaya123')
        db.session.add(u)
        db.session.commit()

        b = Blog(title='test',body="a blog from yaya",author=u.id)
        db.session.add(b)
        db.session.commit()

        db.session.delete(b)
        db.session.commit()

        self.assertEqual(u.blog.first(), None)

    def test_change_password(self):
        user = User(name='test', email='test@gmail.com', password='test123')
        db.session.add(user)
        db.session.commit()
        user = User(name='test', email='test@gmail.com', password='changing')
        db.session.commit()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'changing'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'test123'))



if __name__ == '__main__':
    unittest.main(verbosity=2)
