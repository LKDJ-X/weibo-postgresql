from flask import redirect, request, session, url_for, json, render_template
from helpers import sql

ALREADY_FOLLOW = "You have followed the user"
UNFOLLOW_FAIL = "Unfollow failed"
CANNOT_FOLLOW_YOURSELF = "Sorry, you couldn't follow yourself:)"

def friend():
    user_id = session.get('user', None)
    user_tag = session.get('user_tag', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template("friend.html",
                               user_tag=user_tag)

def follow(following_id):
    error = None

    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    following_id = int(following_id)

    if user_id == following_id:
        error = CANNOT_FOLLOW_YOURSELF
        return json.dumps({
            "success": error is None,
            "error": error,
        })

    if request.method == "POST":
        friendship = sql.execute_query("""
                            SELECT * FROM friendship f
                            WHERE f.user_id = %s and f.friend_id = %s
                            """,
                            (following_id, user_id))
        if friendship:
            error = ALREADY_FOLLOW
        else:
            results = sql.execute_update("""
                          INSERT INTO friendship VALUES (%s, %s)
                          """,
                          (following_id, user_id))



        return json.dumps({
            "success": error is None,
            "error": error,
        })

def unfollow(following_id):
    error = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == "POST":
        results = sql.execute_update("""
                      DELETE FROM friendship WHERE user_id = %s AND friend_id = %s
                      """,
                      (following_id, user_id))
        if (results != 1):
            error = UNFOLLOW_FAIL

        return json.dumps({
            "success": error is None,
            "error": error,
        })

def following_list():
    error = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == "GET":
        results = sql.execute_query("""
                    SELECT u.user_id, u.user_tag, u.email
                    FROM users as u, friendship as f 
                    WHERE u.user_id = f.user_id AND f.friend_id = %s
                    """,
                    (user_id,))

        if results is None:
            results = []
        results = transTuple2Dict(results)

        return json.dumps({
            "success": error is None,
            "error": error,
            "results": results
        })

def follower_list():
    error = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == "GET":
        results = sql.execute_query("""
                    SELECT u.user_id, u.user_tag, u.email
                    FROM users as u, friendship as f 
                    WHERE u.user_id = f.friend_id AND f.user_id = %s
                    """,
                    (user_id,))

        if results is None:
            results = []
        results = transTuple2Dict(results)

        return json.dumps({
            "success": error is None,
            "error": error,
            "results": results
        })

def search_user(keyword):
    error = None
    user_id = session.get('user', None)

    if user_id is None:
        return redirect(url_for('home'))

    if request.method == "GET":
        keyword = '%' + keyword + '%'
        results = sql.execute_query("""
                      SELECT user_id, user_tag, email FROM users
                      WHERE email LIKE %s OR user_tag LIKE %s
                      """,
                      (keyword, keyword))
        if results is None:
            results = []
        results = transTuple2Dict(results)

        return json.dumps({
            "success": error is None,
            "error": error,
            "results": results
        })

def transTuple2Dict(tupleList):
    newList = []
    for tuple in tupleList:
        item = {
            "user_id": tuple[0],
            "user_tag": tuple[1],
            "email": tuple[2]
        }
        newList.append(item)
    return newList