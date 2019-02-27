#!/usr/bin/env python

import matplotlib.pyplot as plt

# performance
data = {"AB_Improved": [], "AB_Custom": [], "AB_Custom_2": [], "AB_Custom_3": []}
with open('performance_data.txt', 'r') as file:
	for line in file:
		words = line.split()
		if not words: continue
		if words[0] != "Win": continue
		performance = [word for word in words if word not in ['Win', 'Rate:']]
		index = 0
		for key in data:
			data[key].append(float(performance[index][:-1]))
			index += 1

# plot the stuff
plt.title('Isolation Heuristics Performance')
plt.xlabel('Iterations')
plt.ylabel('% performance')

style = {"AB_Improved": '--', "AB_Custom": '--', "AB_Custom_2": '-r', "AB_Custom_3": '--'}
for key in data:
	pdata = data[key]
	avg = sum(pdata)/len(pdata)
	plt.plot(pdata, style[key], label="%s (avg %.1f)" % (key, avg))

plt.legend()
plt.show()