// 1. Find all posts authored by "Jason Kincaid"

MATCH (b:Author {name: "Jason Kincaid"})-[:CREATED]->(p:Post)
RETURN p.post_id, p.title, p.date
ORDER BY p.date DESC


// 2. Find bloggers who have published posts after "2010-01-01"

MATCH (a:Author)-[:CREATED]->(p:Post)
WHERE date(p.date) > date("2010-01-01")
RETURN a.name AS author, count(p) AS posts_after_2010
ORDER BY posts_after_2010 DESC


// 3. Find posts that have more than 50 comments

MATCH (p:Post)<-[:HAS_COMMENT]-(c:Comment)
WITH p, count(c) AS total_comments
WHERE total_comments > 50
RETURN p.title, total_comments
ORDER BY total_comments DESC
