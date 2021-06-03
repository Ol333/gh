import matplotlib.pyplot as plt

engine_list = ["gikou","Kristallweizen","YaneuraOu","nozomi"]
win_mas_1 = [10,10,15,0]
win_mas_2 = [12,7,14,1]
win_mas_3 = [10,5,16,4]

fig, axes = plt.subplots(nrows = 1, ncols = 3)

axes[0].set_title("25 мин. (0 с)", fontsize=16)
axes[0].set_xlabel("Движок", fontsize=14)
axes[0].set_ylabel("Количество побед, шт.", fontsize=14)
rect = axes[0].bar(engine_list,win_mas_1,0.9,label='Количество побед',color=["#FFF9CD"])
axes[0].legend()

axes[1].set_title("15 мин. (5 с)", fontsize=16)
axes[1].set_xlabel("Движок", fontsize=14)
axes[1].set_ylabel("Количество побед, шт.", fontsize=14)
rect = axes[1].bar(engine_list,win_mas_2,0.9,label='Количество побед',color=["#FFF9CD"])
axes[1].legend()

axes[2].set_title("5 мин. (10 с)", fontsize=16)
axes[2].set_xlabel("Движок", fontsize=14)
axes[2].set_ylabel("Количество побед, шт.", fontsize=14)
rect = axes[2].bar(engine_list,win_mas_3,0.9,label='Количество побед',color=["#FFF9CD"])
axes[2].legend()

plt.show()