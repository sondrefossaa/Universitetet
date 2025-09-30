#C
#Romerske tall

symbol_values = {
    "I" : 1,
    "V" : 5,
    "X" : 10,
    "L" : 50,
    "C" : 100,
    "D" : 500,
    "M" : 1000
}

romersk_tall = "XII"
symbol_list = list(symbol_values.keys())
sum = 0
for i in range(0, len(romersk_tall), 2):
    if i + 1 < len(romersk_tall):
        if symbol_list.index(romersk_tall[i]) >= symbol_list.index(romersk_tall[i+1]):
            sum += symbol_values[romersk_tall[i]] + symbol_values[romersk_tall[i+1]]
        else:
            sum += symbol_values[romersk_tall[i+1]] - symbol_values[romersk_tall[i]]

print(sum)
       
            
            
