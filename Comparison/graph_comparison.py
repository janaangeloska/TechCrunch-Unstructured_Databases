import matplotlib.pyplot as plt
import csv
import numpy as np

with open('PostgreSQL.csv', 'r') as f:
    postgre_data = [[float(x) for x in row] for row in csv.reader(f)]

with open('Neo4j.csv', 'r') as f:
    neo4j_data = [[float(x) for x in row] for row in csv.reader(f)]

queries = [f'Q{i+1}' for i in range(len(postgre_data))]
x = np.arange(len(queries))
width = 0.35

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].bar(x - width/2, [row[0] for row in postgre_data], width, label='PostgreSQL')
axes[0].bar(x + width/2, [row[0] for row in neo4j_data], width, label='Neo4j')
axes[0].set_title('Minimum Time', fontsize=14)
axes[0].set_ylabel('Time (ms)', fontsize=12)
axes[0].set_xticks(x)
axes[0].set_xticklabels(queries)
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

axes[1].bar(x - width/2, [row[1] for row in postgre_data], width, label='PostgreSQL')
axes[1].bar(x + width/2, [row[1] for row in neo4j_data], width, label='Neo4j')
axes[1].set_title('Maximum Time', fontsize=14)
axes[1].set_ylabel('Time (ms)', fontsize=12)
axes[1].set_xticks(x)
axes[1].set_xticklabels(queries)
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

axes[2].bar(x - width/2, [row[2] for row in postgre_data], width, label='PostgreSQL')
axes[2].bar(x + width/2, [row[2] for row in neo4j_data], width, label='Neo4j')
axes[2].set_title('Average Time', fontsize=14)
axes[2].set_ylabel('Time (ms)', fontsize=12)
axes[2].set_xticks(x)
axes[2].set_xticklabels(queries)
axes[2].legend()
axes[2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('benchmark_comparison.png', dpi=300, bbox_inches='tight')