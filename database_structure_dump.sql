CREATE TABLE "interactions" (
"interaction_id" TEXT,
  "post_id" TEXT,
  "user_id" TEXT,
  "interaction_type" TEXT,
  "timestamp" TEXT,
  "reaction_type" TEXT
);
CREATE TABLE "posts" (
"post_id" TEXT,
  "user_id" TEXT,
  "timestamp" TEXT,
  "content_type" TEXT,
  "content_preview" TEXT,
  "has_media" INTEGER,
  "topic_id" TEXT,
  "language" TEXT
);
CREATE TABLE "topics" (
"topic_id" TEXT,
  "topic_name" TEXT,
  "category" TEXT,
  "moderation_level" TEXT,
  "description" TEXT
);
CREATE TABLE "users" (
"user_id" TEXT,
  "username" TEXT,
  "join_date" TEXT,
  "location" TEXT,
  "account_type" TEXT,
  "verified" INTEGER,
  "followers_count" INTEGER
);
