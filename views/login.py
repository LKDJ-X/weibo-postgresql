import uuid

from flask import render_template, redirect, request, session, url_for

from helpers import crypto, sql

from validate_email import validate_email


INVALID_EMAIL_OR_PASSWORD = 'Invalid email or password provided'


def login():
    error = None
    email = None

    if session.get('user', None):
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if email is None or password is None or not validate_email(email) or len(email) > 256:
            error = INVALID_EMAIL_OR_PASSWORD
        else:
            results = sql.execute_query('SELECT user_id, password, salt, user_tag, user_name FROM users WHERE email = %s', (email,))
            if results is None:
                error = sql.INTERNAL_ERROR

            elif len(results) != 1:
                error = INVALID_EMAIL_OR_PASSWORD

            else:
                res = results[0]

                salt = uuid.UUID(res[2])
                saved_password = res[1]

                hashed_password = crypto.hash_password(password, salt)

                if hashed_password != saved_password:
                    error = INVALID_EMAIL_OR_PASSWORD
                else:
                    session['user'] = res[0]
                    session['user_tag'] = res[3]
                    session['user_name'] = res[4]

                    return redirect(url_for('home'))

    return render_template('login.html',
                           error=error,
                           email=email)
