import matplotlib.pyplot as plt

max_depth = 15
eng_time_param = []
f = open('new_output_1ris_check.txt','r')
counter = 0
time_mas = []
time_mas_labels = []
for line in f:
    line = line.replace('\n','')
    if "среднее" in line:
        temp = float(line.split(' ')[-1])
        time_mas_labels.append(round(temp))
        # temp = math.log(temp,30)
        time_mas.append(temp)
    else:
        if line == str(counter):
            eng_time_param.append([])
            counter += 1
        else:
            eng_time_param[counter-1].append(float(line))
print(eng_time_param)
print(time_mas)

fig, ax = plt.subplots()

ax.set_title("Важный график зависимости времени размышлений от глубины поиска хода", fontsize=16)
ax.set_xlabel("глубина поиска лучшего хода", fontsize=14)
ax.set_ylabel("время, потраченное движком на ходы в течение игры, с", fontsize=14)
ax.grid(which="major",linewidth=1.2)
ax.plot(range(1,max_depth+1),eng_time_param[0],label="gikou")
ax.plot(range(1,max_depth+1),eng_time_param[1],label="Kristallweizen-wcsc29-avx2")
ax.plot(range(1,max_depth+1),eng_time_param[2],label="YaneuraOu_KPPT-tournament-clang++-avx2")
ax.plot(range(1,max_depth+1),eng_time_param[3],label="nozomi")

rect = ax.bar(range(1,max_depth+1),time_mas,0.9,label='Общее количество ходов',color=["#FFF9CD"])
ax.bar_label(rect,time_mas_labels,padding=3)

ax.legend()
ax.tick_params(which='major', length=10, width=1)
plt.show()