import matplotlib.pyplot as plt
import csv
import numpy as np

with open('PostgreSQL.csv', 'r') as f:
    postgre_data = [[float(x) for x in row] for row in csv.reader(f)]

with open('Neo4j.csv', 'r') as f:
    neo4j_data = [[float(x) for x in row] for row in csv.reader(f)]

postgre_avg = [row[2] for row in postgre_data]
neo4j_avg = [row[2] for row in neo4j_data]

# Group by category
simple = [0, 1, 2]  # Q1, Q2, Q3
complex = [3, 4, 5]  # Q4, Q5, Q6
very_complex = [6, 7, 8]  # Q7, Q8, Q9

categories = ['Simple\n(Q1-Q3)', 'Complex\n(Q4-Q6)', 'Very Complex\n(Q7-Q9)']

postgre_by_category = [
    np.mean([postgre_avg[i] for i in simple]),
    np.mean([postgre_avg[i] for i in complex]),
    np.mean([postgre_avg[i] for i in very_complex])
]

neo4j_by_category = [
    np.mean([neo4j_avg[i] for i in simple]),
    np.mean([neo4j_avg[i] for i in complex]),
    np.mean([neo4j_avg[i] for i in very_complex])
]

x_cat = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(x_cat - width/2, postgre_by_category, width,
               label='PostgreSQL', color='#3498db')
bars2 = ax.bar(x_cat + width/2, neo4j_by_category, width,
               label='Neo4j', color='#e74c3c')

ax.set_title('Average Performance by Query Complexity', fontsize=16)
ax.set_xlabel('Query Category', fontsize=14)
ax.set_ylabel('Average Time (ms)', fontsize=14)
ax.set_xticks(x_cat)
ax.set_xticklabels(categories, fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')

for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}', ha='center', va='bottom', fontsize=11)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig('performance_by_category.png', dpi=300, bbox_inches='tight')
plt.show()