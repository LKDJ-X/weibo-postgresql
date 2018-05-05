from flask import redirect, request, session, url_for, json
from helpers import sql

INVALID_CONTENT_SIZE = 'Invalid content size (140 characters maximum)'
INVALID_NO_CONTENT = 'At least write something before posting'
INTERNAL_ERROR = 'Internal error occurred, please try again later'
POST_NOT_FOUND = 'The post was not found'
EMPTY_POST = 'Your post is empty'


def post():
    error = None
    post_data = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        content = request.form.get('content', None)

        if content is None:
            error = INVALID_NO_CONTENT
        elif len(content) <= 140:
            results = sql.execute_query('INSERT INTO posts (user_id, content, creation_date) VALUES (%s, %s, NOW()) RETURNING post_id, content, TO_CHAR(creation_date,\'dd-Mon-YYYY HH:mi:ss\')', (user_id, content), commit=True)

            if results is None or len(results) != 1:
                error = INTERNAL_ERROR
            else:
                results = results[0]
                post_data = dict()
                post_data['post_id'] = results[0]
                post_data['content'] = results[1]
                post_data['creation_date'] = results[2]
        else:
            error = INVALID_CONTENT_SIZE

        return json.dumps({'success': error is None, 'error': error, 'post_data': post_data})


def delete_post(post_id):
    error = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        results = sql.execute_update('DELETE FROM posts WHERE user_id = %s AND post_id = %s',
                                     (user_id, post_id))

        if results != 1:
            error = POST_NOT_FOUND

    return json.dumps({'success': error is None, 'error': error})


def edit_post(post_id):
    error = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        content = request.form.get('content', None)

        if content is None or len(content) == 0:
            error = EMPTY_POST
        else:
            results = sql.execute_update('UPDATE posts SET content = %s WHERE post_id = %s AND user_id = %s',
                                         (content, post_id, user_id))

            if results != 1:
                error = POST_NOT_FOUND

    return json.dumps({'success': error is None, 'error': error})
