import unittest
import app


class FriendTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            self.login("7777888@qq.com", "11111111")

    def tearDown(self):
        self.logout()

    def login(self, email, password):
        rv = self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return rv

    def logout(self):
        return self.app.post('/logout', follow_redirects=True)

    def test_login_success(self):
        rv = self.login("7777888@qq.com", "11111111")
        assert 'duxue' in rv.data.decode()

    # search_user
    def test_search_user(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.get('/search_user/' + 'abc', follow_redirects=True)
        assert 'abc' in rv.data.decode()

    def test_search_user_fail(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.get('/search_user/' + 'dd', follow_redirects=True)
        print(rv)
        assert 'true' in rv.data.decode()

    # follow
    def test_follow_success(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.post('/follow/' + '3', follow_redirects=True)
        print(rv)
        assert 'true' in rv.data.decode()

    def test_follow_followed(self):
        self.login("7777888@qq.com", "11111111")
        self.app.post('/follow/' + '4', follow_redirects=True)
        rv = self.app.post('/follow/' + '4', follow_redirects=True)
        print(rv)
        assert 'You have followed the user' in rv.data.decode()

    def test_follow_myself(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.post('/follow/' + '2', follow_redirects=True)
        assert 'Sorry, you' in rv.data.decode()

    # unfollow
    def test_unfollow_success(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.post('/unfollow/' + '3', follow_redirects=True)
        assert 'true' in rv.data.decode()

    def test_unfollow_fail(self):
        self.login("7777888@qq.com", "11111111")
        self.app.post('/unfollow/' + '4', follow_redirects=True)
        rv = self.app.post('/unfollow/' + '4', follow_redirects=True)
        print(rv)
        assert 'Unfollow failed' in rv.data.decode()

    # following list
    def test_following_list_success(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.get('/following_list', follow_redirects=True)
        print(rv)
        assert 'true' in rv.data.decode()

    def test_following_list_fail(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.get('/following_list', follow_redirects=True)
        print(rv)
        assert 'true' in rv.data.decode()

    # follower list
    def test_follower_list_success(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.get('/follower_list', follow_redirects=True)
        print(rv)
        assert 'true' in rv.data.decode()

    def test_follower_list_fail(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.app.get('/follower_list', follow_redirects=True)
        print(rv)
        assert 'true' in rv.data.decode()



if __name__ == '__main__':
    #unittest.main(verbosity=2)

    suite = unittest.TestSuite()
    suite.addTest(FriendTestCase("test_login_success"))
    suite.addTest(FriendTestCase("test_follow_success"))
    suite.addTest(FriendTestCase("test_follow_followed"))
    suite.addTest(FriendTestCase("test_follow_myself"))
    suite.addTest(FriendTestCase("test_unfollow_success"))
    suite.addTest(FriendTestCase("test_unfollow_fail"))
    suite.addTest(FriendTestCase("test_following_list_success"))
    suite.addTest(FriendTestCase("test_following_list_fail"))
    suite.addTest(FriendTestCase("test_follower_list_success"))
    suite.addTest(FriendTestCase("test_follower_list_fail"))
    suite.addTest(FriendTestCase("test_search_user"))
    suite.addTest(FriendTestCase("test_search_user_fail"))

    runner = unittest.TextTestRunner()
    runner.run(suite)

