import matplotlib.pyplot as plt

engine_list_for_graphic = ["gikou","Kristallweizen","nozomi"]
counter_of_moves = [ [81,47,61,81,87,105,87,95,139,115],
                    [67,99,93,91,103,119,89,117,93,73],
                    [23,83,75,57,139,87,101,101,101,103]]
max_depth = 10

fig,ax = plt.subplots()
ax.set_xlabel("Глубина поиска лучшего хода", fontsize=14)
ax.set_ylabel("Среденее количество ходов в партии", fontsize=14)
ax.grid(which="major",linewidth=1.2)
for k in range(3):
    ax.plot(range(1,max_depth+1),counter_of_moves[k],label=engine_list_for_graphic[k])
ax.tick_params(which='major', length=10, width=1)
ax.legend()
plt.show()