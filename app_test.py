import unittest
import psycopg2

class FlaskrTestCase(unittest.TestCase):

    conn = None

    def setUp(self):
        global conn
        conn = psycopg2.connect(database="weibo", user="postgres", password="123456", host="localhost", port="5432")
        print("Opened database successfully")

    def tearDown(self):
        global conn
        conn.close()


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()

