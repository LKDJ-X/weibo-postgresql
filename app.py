from flask import Flask

from views.register import register
from views.home import home
from views.login import login
from views.logout import logout
from views.user import user
from views.post import post, edit_post, delete_post


app = Flask(__name__)

app.add_url_rule('/', 'home', home)
app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/post', 'post', post, methods=["POST"])
app.add_url_rule('/register', 'register', register, methods=["GET", "POST"])
app.add_url_rule('/user/<user_tag>', 'user', user)


app.add_url_rule('/edit_post/<post_id>', 'edit_post', edit_post, methods=["POST"])
app.add_url_rule('/delete_post/<post_id>', 'delete_post', delete_post, methods=["POST"])



# TODO move to external thing
# Secret key, good luck to brute force that
app.secret_key = 'cayupruChukebucAkexEtHU2rey25tudyadasaphed6A85e6ucrufutehAquxusttacenaPhutreqevexutHaVuva2ebebasspatr'


if __name__ == '__main__':

    app.run(debug = True)

