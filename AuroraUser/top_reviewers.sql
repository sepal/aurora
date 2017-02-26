UPDATE "Course_courseuserrelation"
SET top_reviewer = TRUE
WHERE id IN (SELECT id
			 FROM "Course_courseuserrelation"
			 WHERE course_id = 1
			 ORDER BY review_karma DESC
			 LIMIT 50
     );

UPDATE "Course_courseuserrelation"
SET top_reviewer = TRUE
WHERE id IN (SELECT id
			 FROM "Course_courseuserrelation"
			 WHERE course_id = 2
			 ORDER BY review_karma DESC
			 LIMIT 50
     );
