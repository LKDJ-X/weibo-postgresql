import unittest
import app


class PostTestCase(unittest.TestCase):

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

    def post(self, content):
        return self.app.post('/post',
                             data=dict(content=content),
                             follow_redirects=True)

    def delete_post(self, post_id):
        return self.app.post('/delete_post/' + post_id , follow_redirects=True)

    def edit_post(self, post_id, content):
        return self.app.post('/edit_post/' + post_id, data=dict(content=content), follow_redirects=True)

    def like_post(self, post_id):
        return self.app.post('/like_post/' + post_id, follow_redirects=True)

    def dislike_post(self, post_id):
        return self.app.post('/dislike_post/' + post_id, follow_redirects=True)

    def test_post_success(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.post("Woooo")
        assert 'true' in rv.data.decode()

    def test_post_content_invalid(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.post("")
        assert 'At least write something before posting' in rv.data.decode()

    def test_delete_post_sucess(self):
        self.login("7777888@qq.com", "11111111")
        result = self.post("test1")
        post_id = result.data.decode()['post_data']['post_id']
        rv = self.delete_post(post_id)
        assert 'true' in rv.data.decode()

    def test_delete_post_fail(self):
        self.login("7777888@qq.com", "11111111")
        rv = self.delete_post("123")
        assert 'The post does not found' in rv.data.decode()

    def test_edit_post_sucess(self):
        self.login("7777888@qq.com", "11111111")
        result = self.post("test edit")
        post_id = result.data.decode()['post_data']['post_id']
        rv = self.edit_post(post_id, "edit success")
        assert 'true' in rv.data.decode()


if __name__ == '__main__':
    #unittest.main(verbosity=2)
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(PostTestCase("test_login_success"))
    
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

