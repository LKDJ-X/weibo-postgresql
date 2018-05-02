import re

from flask import render_template, redirect, request, session, url_for

from helpers import crypto, sql

from validate_email import validate_email

INVALID_FORM = 'Please fill in all required fields'
INVALID_EMAIL = 'Invalid email'
INVALID_PASSWORD = 'Password should be at least 8 characters long'
PASSWORD_NOT_MATCHING = 'Passwords are not the same ones'
EMAIL_ALREADY_IN_USE = 'This email address is already used'
TAG_ALREADY_IN_USE = 'This username is already in use'


def validate_tag(tag):
    return re.match('^[a-zA-Z0-9_]+$', tag)


def register():
    error = None

    tag = None
    email = None

    if session.get('user', None):
        return redirect(url_for('home'))

    if request.method == 'POST':
        tag = request.form.get('tag', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password_confirm = request.form.get('password_confirm')

        if email is None or password is None or tag is None:
            error = INVALID_FORM
        elif not validate_email(email) or len(email) > 256:
            error = INVALID_EMAIL
        elif len(password) < 8:
            error = INVALID_PASSWORD
        elif password != password_confirm:
            error = PASSWORD_NOT_MATCHING
        else:
            # TODO Lock
            results = sql.execute_query(
                'SELECT email, user_tag FROM users WHERE email = %s OR user_tag = %s',
                (email, tag)
            )

            if results is None:
                error = sql.INTERNAL_ERROR
            elif len(results) != 0:
                result1 = results[0]
                result2 = results[1] if len(results) == 2 else result1

                if email == result1[0] or email == result2[0]:
                    error = EMAIL_ALREADY_IN_USE
                else:
                    error = TAG_ALREADY_IN_USE
            else:
                salt = crypto.generate_salt()

                hashed_password = crypto.hash_password(password, salt)

                print(salt, hashed_password)

                results = sql.execute_query(
                    'INSERT INTO users (user_tag, user_name, user_description, email, password, salt, creation_date)' +
                    'VALUES (%s, %s, %s, %s, %s, %s, NOW()) RETURNING user_id',
                    (tag, tag, '', email, hashed_password, str(salt)), commit=True
                )

                print(results)

                if results is None or len(results) != 1:
                    error = sql.INTERNAL_ERROR
                else:
                    session['user'] = results[0][0]
                    session['user_tag'] = tag
                    session['user_name'] = tag
                    return redirect(url_for('home'))

    return render_template('register.html',
                           error=error,
                           email=email,
                           tag=tag)
