import unittest
import app


class UserTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def register(self, tag, email, password, password_confirm):
        return self.app.post('/register',
                             data=dict(tag=tag, email=email, password=password, password_confirm=password_confirm),
                             follow_redirects=True)

    def login(self, email, password):
        rv = self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return rv

    def logout(self):
        return self.app.post('/logout', follow_redirects=True)

    def user(self, user_tag):
        return self.app.post('/user/' + user_tag, follow_redirects=True)

    def test_register_success(self):
        rv = self.register("aa", "aa1111@qq.com", "123456", "123456")
        assert 'aa' in rv.data.decode()

    def test_register_tag_invalid(self):
        rv = self.register("tag", "tag1111@qq.com", "123456", "123456")
        assert 'tag' in rv.data.decode()
        rv = self.register(None, "tag21111@qq.com", "123456", "123456")
        assert 'Please fill in all required fields' in rv.data.decode()
        rv = self.register("tag", "tag1111@qq.com", "123456", "123456")
        assert 'This username is already in use' in rv.data.decode()

    def test_register_email_invalid(self):
        rv = self.register("email", "email1111@qq.com", "123456", "123456")
        assert 'email' in rv.data.decode()
        rv = self.register("email2", "email1111@qq.com", "123456", "123456")
        assert 'This email address is already used' in rv.data.decode()
        rv = self.register("email3", "email1111qq.com", "123456", "123456")
        assert 'Invalid email' in rv.data.decode()
        rv = self.register("email4", None, "123456", "123456")
        assert 'Please fill in all required fields' in rv.data.decode()

    def test_register_password_invalid(self):
        rv = self.register("pw1", "pw1111@qq.com", "123", "123")
        assert 'Password should be at least 6 characters long' in rv.data.decode()
        rv = self.register("pw2", "cc1111@qq.com", "123456", "123555")
        assert 'Passwords are not the same ones' in rv.data.decode()
        rv = self.register("pw3", "pw31111@qq.com", None, None)
        assert 'Please fill in all required fields' in rv.data.decode()


if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(UserTestCase("test_register_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

