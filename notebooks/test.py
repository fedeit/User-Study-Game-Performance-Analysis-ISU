import pandas as pd
import matplotlib.pyplot as plt
import glob

directory = '../../data/raw'

labels = []
level_means = []
load_means = []

for filename in glob.iglob(f'{directory}/*/'):
    for filename2 in glob.iglob(f'{filename}/*'):
        split = filename2.split("\\")
        new = split[-1]
        #print(split[-2])
        if new.startswith("metrics") and new.endswith("csv"):
            df = pd.read_csv(filename2)

            labels.append(split[-2])
            
            level_means.append(df['level'].mean())
            load_means.append(df['load'].mean())

            games = df.groupby(['game_name'], as_index = False)
            for game in games:
                data = game[1][['load', 'level', 'iteration']]

                plt.plot(data['iteration'], data['level'], label = game[0])
                plt.title(split[-2] + " LEVEL")

            plt.legend()
            plt.show()

            for game in games:
                data = game[1][['load', 'level', 'iteration']]

                plt.plot(data['iteration'], data['load'], label = game[0])
                plt.title(split[-2] + " LOAD")

            plt.legend()
            plt.show()
            #for game in games:
                #game_name = game[0]
                #print(game[0])
                #data = ['load', 'level', 'iteration']
                #plotGame(game_name, 'load', data)
                #plotGame(game_name, 'level', data)

        else:
            continue
        '''df = pd.read_csv('../../data/raw/G10-6700-SSD/metrics_03-20-22_04-19-50.csv')

        level_times = df['level'].mean()
        load_times = df['load'].mean()'''

width = 0.35

fig, ax = plt.subplots()

plt.xticks(rotation=45, ha="right")

ax.bar(labels, level_means, width, label='Level')
ax.bar(labels, load_means, width, bottom=level_means, label='Load')

ax.set_ylabel('Times')
ax.set_title('Times by Level and Load')
ax.legend()

plt.show()