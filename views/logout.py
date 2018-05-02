from flask import redirect, session, url_for


def logout():
    session.pop('user', None)
    session.pop('user_tag', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))
