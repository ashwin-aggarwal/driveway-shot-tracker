import matplotlib.pyplot as plt

def plot_make_miss_stats(makes, misses):
    labels = ['Makes', 'Misses']
    counts = [len(makes), len(misses)]
    colors = ['#4CAF50', '#F44336']  # Green for makes, red for misses

    fig, ax = plt.subplots()
    bars = ax.bar(labels, counts, color=colors, width=0.5)

    fgpercent = len(makes) / (len(makes) + len(misses)) * 100 if (len(makes) + len(misses)) > 0 else 0
    # Annotate bar values
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, f'{yval}', ha='center', va='bottom', fontsize=12)

    # Style tweaks
    ax.set_title(f"Shot Outcome Summary -- You Shot {fgpercent}% Today!", fontsize=16, weight='bold')
    ax.set_ylabel("Number of Shots", fontsize=12)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_ylim(0, max(counts) + 5)

    plt.tight_layout()
    plt.show()
