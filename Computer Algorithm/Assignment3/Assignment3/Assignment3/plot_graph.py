import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = {1: 8.88447, 2: 5.57978, 3: 4.05222, 4: 3.38965,
        5: 3.23881, 6: 2.90673, 7: 2.81921, 8: 3.28393}

# Extracting the threads and average time
threads = np.array(list(data.keys()))
avg_time = np.array(list(data.values()))

plt.figure(figsize=(12, 8))

# Create a different style for the plot
plt.plot(threads, avg_time, marker='s', linestyle='--', color='darkorange', linewidth=2, markersize=10, label='Average Time')

# Highlight the minimum time
min_time_idx = np.argmin(avg_time)
plt.scatter(threads[min_time_idx], avg_time[min_time_idx], color='red', zorder=5)
plt.annotate(f'Min Time: {avg_time[min_time_idx]:.4f}s',
             xy=(threads[min_time_idx], avg_time[min_time_idx]),
             xytext=(threads[min_time_idx] + 2, avg_time[min_time_idx] + 0.05),
             arrowprops=dict(facecolor='red', arrowstyle='->'))

plt.title('Matrix-Matrix Multiplication Time vs Number of Threads', fontsize=18, fontweight='bold')
plt.xlabel('Number of Threads', fontsize=14)
plt.ylabel('Average Time (seconds)', fontsize=14)

plt.grid(True, linestyle=':', alpha=0.5)
plt.gca().set_facecolor('lightgray')

plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)

plt.legend(fontsize=12)
plt.tight_layout()

plt.savefig('time_vs_threads_updated.png')
plt.show()