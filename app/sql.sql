CREATE TABLE "users"
(
    "id"         text PRIMARY KEY,
    "email"      text    NOT NULL UNIQUE,
    "password"   text    NOT NULL,
    "nickname"   text,
    "scores"     integer NOT NULL,
    "firstname"  text,
    "lastname"   text,
    "patronymic" text,
    "avatar"     text,
    "birthday"   date,
    "phone"      text,
    "gender"     text,
    "profession" text,
    "company"    text
);
create TABLE "admins"
(
    "id" text PRIMARY KEY references users (id) on delete cascade
);
ALTER TABLE "admins"
    ADD CONSTRAINT "admins_fk0" FOREIGN KEY ("id") REFERENCES "users" ("id");

create TABLE "teachers"
(
    "id" text PRIMARY KEY references users (id) on delete cascade
);
create TABLE "videos"
(
    "id"           serial PRIMARY KEY,
    "link"         TEXT      NOT NULL,
    "title"        TEXT      NOT NULL,
    "description"  TEXT,
    "posting_time" TIMESTAMP NOT NULL,
    "creator_id"   TEXT      references teachers (id) on delete set null
);
CREATE TABLE "groups"
(
    "id"         serial PRIMARY KEY,
    "name"       TEXT NOT NULL,
    "teacher_id" TEXT references teachers (id) on delete set null,
    unique ("name", "teacher_id")
);
create TABLE "courses"
(
    "id"          serial PRIMARY KEY,
    "name"        TEXT NOT NULL,
    "description" TEXT,
    "teacher_id"  TEXT references teachers (id) on delete set null,
    unique ("name", "teacher_id")
);
CREATE TABLE "topics"
(
    "id"   serial PRIMARY KEY,
    "name" text NOT NULL UNIQUE
);
CREATE TABLE "advancements"
(
    "id"          serial PRIMARY KEY,
    "title"       text NOT NULL UNIQUE,
    "description" text,
    "level"       text
);

CREATE TABLE "users_advancements"
(
    "user_id"        text    NOT NULL references users (id) on delete cascade,
    "advancement_id" integer NOT NULL references advancements (id) on delete cascade,
    unique ("user_id", "advancement_id")
);
CREATE TABLE "users_groups"
(
    "user_id"  text    NOT NULL references users (id) on delete cascade,
    "group_id" integer NOT NULL references groups (id) on delete cascade,
    "status"   integer NOT NULL,
    unique ("user_id", "group_id")
);
CREATE TABLE "users_topics"
(
    "user_id"  text    NOT NULL references users (id) on delete cascade,
    "topic_id" integer NOT NULL references topics (id) on delete cascade,
    unique ("user_id", "topic_id")
);
CREATE TABLE "users_courses"
(
    "user_id"   text    NOT NULL references users (id) on delete cascade,
    "course_id" integer NOT NULL references topics (id) on delete cascade,
    "status"    integer NOT NULL,
    unique ("user_id", "course_id")
);
CREATE TABLE users_friends
(
    "user_id"   text    NOT NULL references users (id) on delete cascade,
    "friend_id" text    NOT NULL references users (id) on delete cascade,
    "status"    integer NOT NULL,
    unique ("user_id", "friend_id")
);

ALTER TABLE "groups"
    ADD CONSTRAINT "teams_fk0" FOREIGN KEY ("teacher_id") REFERENCES "teachers" ("id");
ALTER TABLE "teachers"
    ADD CONSTRAINT "teachers_fk0" FOREIGN KEY ("id") REFERENCES "users" ("id");
ALTER TABLE "videos"
    ADD CONSTRAINT "video_fk0" FOREIGN KEY ("creator_id") REFERENCES "teachers" ("id");

ALTER TABLE "users_advancements"
    ADD CONSTRAINT "users_achs_fk0" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "users_advancements"
    ADD CONSTRAINT "users_achs_fk1" FOREIGN KEY ("advancement_id") REFERENCES "advancements" ("id");

ALTER TABLE "users_groups"
    ADD CONSTRAINT "users_teams_fk0" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "users_groups"
    ADD CONSTRAINT "users_teams_fk1" FOREIGN KEY ("group_id") REFERENCES "groups" ("id");

ALTER TABLE "users_topics"
    ADD CONSTRAINT "users_topics_fk0" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "users_topics"
    ADD CONSTRAINT "users_topics_fk1" FOREIGN KEY ("topic_id") REFERENCES "topics" ("id");

ALTER TABLE "users_courses"
    ADD CONSTRAINT "users_courses_fk0" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "users_courses"
    ADD CONSTRAINT "users_courses_fk1" FOREIGN KEY ("course_id") REFERENCES "topics" ("id");
