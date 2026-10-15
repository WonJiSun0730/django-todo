-- MySQL 8.0+, UTF-8. Submission DDL for the Todo model.
CREATE DATABASE IF NOT EXISTS todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE todo_db;
CREATE TABLE todos_todo (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content LONGTEXT NOT NULL,
    is_completed BOOL NOT NULL DEFAULT 0,
    created_at DATETIME(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- content is optional in forms and stored as an empty string when omitted.
-- created_at is populated by Django auto_now_add. Boolean defaults exist in ORM and DB.
-- Normal install: create the database only, then run manage.py migrate.
-- Do not create this table manually before migrate (duplicate table).
