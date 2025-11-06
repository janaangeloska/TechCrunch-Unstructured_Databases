// 4. For each blogger, find the total number of comments and inlinks on their posts

MATCH (a:Author)-[:CREATED]->(p:Post)
OPTIONAL MATCH (p)<-[:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[:HAS_INLINK]-(i:Inlink)
WITH a, count(DISTINCT c) AS total_comments, 
        count(DISTINCT i) AS total_inlinks
RETURN a.name AS author, total_comments, total_inlinks
ORDER BY total_inlinks DESC, total_comments DESC


// 5. Identify the most influential bloggers based on the average number of inlinks per post

MATCH (a:Author)-[:CREATED]->(p:Post)<-[:HAS_INLINK]-(i:Inlink)
WITH a, count(i) AS total_inlinks, 
	count(DISTINCT p) AS total_posts
WITH a, total_inlinks * 1.0 / total_posts AS avg_inlinks_per_post
RETURN a.name AS author, round(avg_inlinks_per_post, 2) AS avg_inlinks
ORDER BY avg_inlinks DESC


// 6. Find the first 100 most commented posts along with their authors

MATCH (a:Author)-[:CREATED]->(p:Post)<-[:HAS_COMMENT]-(c:Comment)
WITH a, p, count(c) AS total_comments
RETURN a.name AS author, p.title AS post_title, total_comments
ORDER BY total_comments DESC
LIMIT 100

