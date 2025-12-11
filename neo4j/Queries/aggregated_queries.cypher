// 7. Calculate the average number of comments and inlinks per post for each blogger

MATCH (a:Author)-[:CREATED]->(p:Post)
OPTIONAL MATCH (p)<-[:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[:HAS_INLINK]-(i:Inlink)
WITH a, count(DISTINCT p) AS total_posts,
	count(DISTINCT c) AS total_comments,
	count(DISTINCT i) AS total_inlinks
WITH a,
	round(total_comments * 1.0 / total_posts, 2) AS avg_comments_per_post,
	round(total_inlinks * 1.0 / total_posts, 2) AS avg_inlinks_per_post
RETURN a.name AS author, avg_comments_per_post, avg_inlinks_per_post
ORDER BY avg_inlinks_per_post DESC, avg_comments_per_post DESC


// 8. Identify the most influential bloggers by aggregating MEIBI and MEIBIX scores across their posts

MATCH (a:Author)-[:CREATED]->(p:Post)
OPTIONAL MATCH (p)<-[:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[:HAS_INLINK]-(i:Inlink)
WITH a, sum(p.MEIBI_score) AS total_meibi,
	sum(p.MEIBIX_score) AS total_meibix,
	count(DISTINCT c) AS total_comments,
	count(DISTINCT i) AS total_inlinks
WITH a, total_meibi, total_meibix, total_comments, total_inlinks,
     (total_meibi + total_meibix + total_comments + total_inlinks) AS influence_score
RETURN a.name AS author, total_meibi, total_meibix, total_comments, total_inlinks, 
	round(influence_score, 2) AS total_influence
ORDER BY total_influence DESC


// 9. Find the first 100 posts with the highest engagement score (sum of comments and inlinks)

MATCH (p:Post)
OPTIONAL MATCH (p)<-[:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[:HAS_INLINK]-(i:Inlink)
WITH p, count(DISTINCT c) AS total_comments, 
	count(DISTINCT i) AS total_inlinks
WITH p, total_comments, total_inlinks, (total_comments + total_inlinks) AS engagement_score
RETURN p.title AS post_title, engagement_score, total_comments, total_inlinks
ORDER BY engagement_score DESC
LIMIT 100

