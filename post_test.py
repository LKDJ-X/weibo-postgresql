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






if __name__ == '__main__':
    #unittest.main(verbosity=2)
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(PostTestCase("test_login_success"))
    
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

