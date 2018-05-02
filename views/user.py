from flask import redirect, render_template, url_for, session

from helpers import sql


NOT_FOUND = 'No user found with that username'


def user(user_tag):
    user_id = session.get('user', None)
    if user_id is None:
        return redirect(url_for('home'))

    error = None
    user_name = None
    user_description = None
    user_mail = None
    creation_date = None
    own = False

    user_info = sql.execute_query(
        'SELECT user_name, user_description, TO_CHAR(creation_date,\'dd-Mon-YYYY HH:mi:ss\'), email, user_id FROM users WHERE user_tag = %s',
        (user_tag,)
    )

    if user_info is None:
        error = sql.INTERNAL_ERROR
    elif len(user_info) == 0:
        error = NOT_FOUND
    else:
        user_info = user_info[0]

        user_name = user_info[0]
        user_description = user_info[1]
        creation_date = user_info[2]
        user_mail = user_info[3]
        if user_id == user_info[4]:
            own = True

    return render_template('user.html',
                           own=own,
                           error=error,
                           user_tag=user_tag,
                           user_name=user_name,
                           user_mail=user_mail,
                           user_description=user_description,
                           creation_date=creation_date)
