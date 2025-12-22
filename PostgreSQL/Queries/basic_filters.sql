-- 1. Find all posts authored by "Jason Kincaid"
SELECT
	-- *
	P.POST_ID,
	P.TITLE,
	P.DATE
FROM
	POSTS AS P
	INNER JOIN AUTHORS AS A ON P.BLOGGERS_ID = A.AUTH_ID
WHERE
	A."name" = 'Jason Kincaid'
ORDER BY
	P.DATE DESC;

-- 2. Find bloggers who have published posts after "2010-01-01"
SELECT
	A."name",
	COUNT(P.POST_ID) AS "posts_after_2010"
FROM
	POSTS AS P
	INNER JOIN AUTHORS AS A ON P.BLOGGERS_ID = A.AUTH_ID
WHERE
	P.DATE > '2010-01-01'
GROUP BY
	A."name"
ORDER BY
	POSTS_AFTER_2010 DESC;

-- 3. Find posts that have more than 50 comments
SELECT
	P.TITLE,
	COUNT(C.COM_ID) AS "total_comments"
FROM
	"comments" AS C
	INNER JOIN POSTS AS P ON C.POST_ID = P.POST_ID
GROUP BY
	P.TITLE
ORDER BY
	TOTAL_COMMENTS DESC