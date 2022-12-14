'''
Calculate variance of LA Galaxy top 2 finishes
'''
list = [0.4, 0.4, 0.6, 0.5, 0.7, 0.8, 0.2, 0.3, 0.2, 0.6]
mean = 0.5251

list2 = [(n - mean)**2 for n in list]
print(sum(list2) / (len(list2) - 1))
