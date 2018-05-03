from flask import render_template, session

from helpers import sql


def home():
    user_id = session.get('user', None)
    user_tag = session.get('user_tag', None)
    user_name = session.get('user_name', None)


    if user_id is None:
        return render_template('index.html')
    else:
        results = sql.execute_query('''SELECT users.user_name, users.user_tag, TO_CHAR(posts.creation_date, \'dd-Mon-YYYY HH:mi:ss\'), 
          posts.content, posts.post_id, posts.likes, posts.comments, users.posts ,
          users.following, users.followed FROM posts, users 
          WHERE  (posts.user_id IN (SELECT user_id FROM friendship WHERE friend_id = %s) OR posts.user_id = %s)
          AND users.user_id = posts.user_id  
          ORDER BY posts.creation_date DESC''', (user_id, user_id))
        if results is None:
            results = []
        return render_template('home.html',
                               user_tag=user_tag,
                               user_name=user_name,
                               tweets=results)
