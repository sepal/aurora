ALTER DATABASE django_website CHARACTER SET = utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE diskurs_post CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE diskurs_post CHANGE content content longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;