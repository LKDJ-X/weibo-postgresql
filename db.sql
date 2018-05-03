DROP TABLE IF EXISTS likes_posts;
DROP TABLE IF EXISTS likes_comments;
DROP TABLE IF EXISTS friendship;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL NOT NULL PRIMARY KEY,
  user_tag TEXT NOT NULL UNIQUE,
  user_name TEXT NOT NULL,
  user_description TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  salt TEXT NOT NULL,
  creation_date TIMESTAMPTZ NOT NULL,

  posts BIGINT NOT NULL DEFAULT 0,
  comments BIGINT NOT NULL DEFAULT 0,
  following BIGINT NOT NULL DEFAULT 0,
  followed BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX users_tag ON users (user_tag);
CREATE INDEX users_email ON users (email);

CREATE TABLE IF NOT EXISTS posts (
  post_id SERIAL NOT NULL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  creation_date TIMESTAMPTZ NOT NULL,

  comments BIGINT NOT NULL DEFAULT 0,
  likes BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX posts_user_id_btree ON posts USING BTREE (user_id);

CREATE TABLE IF NOT EXISTS comments (
  comment_id SERIAL NOT NULL PRIMARY KEY,
  post_id BIGINT NOT NULL REFERENCES posts (post_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  creation_date TIMESTAMPTZ NOT NULL,

  likes BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX comments_post_id_btree ON comments USING BTREE (post_id);
CREATE INDEX comments_user_id_btree ON comments USING BTREE (user_id);

CREATE TABLE IF NOT EXISTS likes_posts (
  post_id BIGINT NOT NULL REFERENCES posts (post_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE INDEX likes_posts_post_id_btree ON likes_posts USING BTREE (post_id);
CREATE INDEX likes_posts_user_id_btree ON likes_posts USING BTREE (user_id);
CREATE UNIQUE INDEX likes_posts_unique ON likes_posts (post_id, user_id);

CREATE TABLE IF NOT EXISTS likes_comments (
  comment_id BIGINT NOT NULL REFERENCES comments (comment_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE INDEX likes_comments_post_id_btree ON likes_comments USING BTREE (comment_id);
CREATE INDEX likes_comments_user_id_btree ON likes_comments USING BTREE (user_id);
CREATE UNIQUE INDEX likes_comments_unique ON likes_comments (comment_id, user_id);

CREATE TABLE IF NOT EXISTS friendship (
  user_id BIGINT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  friend_id BIGINT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE
    CHECK (friendship.friend_id != friendship.user_id)
);

CREATE INDEX friendship_user_id_btree ON friendship USING BTREE (user_id);
CREATE INDEX friendship_friend_id_btree ON friendship USING BTREE (friend_id);
ALTER TABLE friendship ADD PRIMARY KEY ("user_id", "friend_id");

-------------------------

CREATE OR REPLACE FUNCTION users_posts_increment() RETURNS TRIGGER AS
  $BODY$
  BEGIN
    UPDATE users SET posts = posts + 1 WHERE users.user_id = NEW.user_id;

    RETURN NEW;
  END;
  $BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION users_posts_decrement() RETURNS TRIGGER AS
  $BODY$
  BEGIN
    UPDATE users SET posts = posts - 1 WHERE users.user_id = OLD.user_id;

    RETURN NEW;
  END;
  $BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION users_following_increment() RETURNS TRIGGER AS
  $BODY$
  BEGIN
    UPDATE users SET following = users.following + 1 WHERE users.user_id = NEW.friend_id;

    RETURN NEW;
  END;
  $BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION users_following_decrement() RETURNS TRIGGER AS
  $BODY$
  BEGIN
    UPDATE users SET following = users.following - 1 WHERE users.user_id = OLD.friend_id;

    RETURN NEW;
  END;
  $BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION users_followed_increment() RETURNS TRIGGER AS
  $BODY$
  BEGIN
    UPDATE users SET followed = users.followed + 1 WHERE users.user_id = NEW.user_id;

    RETURN NEW;
  END;
  $BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION users_followed_decrement() RETURNS TRIGGER AS
  $BODY$
  BEGIN
    UPDATE users SET followed = users.followed - 1 WHERE users.user_id = OLD.user_id;

    RETURN NEW;
  END;
  $BODY$ LANGUAGE plpgsql;

CREATE TRIGGER users_posts_trigger_insert AFTER INSERT ON posts FOR EACH ROW EXECUTE PROCEDURE users_posts_increment();
CREATE TRIGGER users_posts_trigger_delete AFTER DELETE ON posts FOR EACH ROW EXECUTE PROCEDURE users_posts_decrement();
CREATE TRIGGER users_following_trigger_insert AFTER INSERT ON friendship FOR EACH ROW EXECUTE PROCEDURE users_following_increment();
CREATE TRIGGER users_following_trigger_delete AFTER DELETE ON friendship FOR EACH ROW EXECUTE PROCEDURE users_following_decrement();
CREATE TRIGGER users_followed_trigger_insert AFTER INSERT ON friendship FOR EACH ROW EXECUTE PROCEDURE users_followed_increment();
CREATE TRIGGER users_followed_trigger_delete AFTER DELETE ON friendship FOR EACH ROW EXECUTE PROCEDURE users_followed_decrement();
