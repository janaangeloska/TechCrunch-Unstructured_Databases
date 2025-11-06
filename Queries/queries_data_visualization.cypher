// Limitations of records for a clearer preview (LIMIT 500)

// 1. Shows Jason Kincaid and all posts he created

MATCH (a:Author {name: "Jason Kincaid"})-[r:CREATED]->(p:Post)
RETURN a, r, p


// 2. Displays posts with more than 50 comments and their comment nodes

MATCH (p:Post)<-[:HAS_COMMENT]-(c:Comment)
WITH p, collect(c) AS comments, count(c) AS total_comments
WHERE total_comments > 50
UNWIND comments AS c
MATCH (p)<-[r:HAS_COMMENT]-(c)
RETURN p, r, c


// 3. Shows authors and their posts published after 2010-01-01

MATCH (a:Author)-[r:CREATED]->(p:Post)
WHERE date(p.date) > date("2010-01-01")
RETURN a, r, p


// 4. Displays bloggers, their posts, and both comments and inlinks connected to those posts

MATCH (a:Author)-[cr:CREATED]->(p:Post)
OPTIONAL MATCH (p)<-[rc:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[ri:HAS_INLINK]-(i:Inlink)
RETURN a, cr, p, c, i, rc, ri
LIMIT 500


// 5. Shows authors and posts that have inlinks, highlighting influence connections

MATCH (a:Author)-[cr:CREATED]->(p:Post)<-[r:HAS_INLINK]-(i:Inlink)
RETURN a, cr, p, i, r
LIMIT 500


// 6. Displays posts with many comments and the authors who created them

MATCH (a:Author)-[:CREATED]->(p:Post)<-[r:HAS_COMMENT]-(c:Comment)
RETURN a, p, c, r


// 7. Shows the full interaction graph: author -> post <- comments/inlinks 

MATCH (a:Author)-[cr:CREATED]->(p:Post)
OPTIONAL MATCH (p)<-[rc:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[ri:HAS_INLINK]-(i:Inlink)
RETURN a, cr, p, c, i, rc, ri
LIMIT 500


// 8. Shows top influential bloggers (based on MEIBI + MEIBIX) 

MATCH (a:Author)-[cr:CREATED]->(p:Post)
WHERE (p.MEIBI_score + p.MEIBIX_score) > 50
OPTIONAL MATCH (p)<-[rc:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[ri:HAS_INLINK]-(i:Inlink)
RETURN a, cr, p, c, i, rc, ri
LIMIT 500


// 9. Displays posts with their comments and inlinks to visualize engagement

MATCH (p:Post)
OPTIONAL MATCH (p)<-[rc:HAS_COMMENT]-(c:Comment)
OPTIONAL MATCH (p)<-[ri:HAS_INLINK]-(i:Inlink)
RETURN p, c, i, rc, ri
LIMIT 500



