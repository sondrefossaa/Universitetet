input = "001"

def q1(step):
    if step >len(input):
        print(input)
        
    elif input[step] == "0":
        #Case
        input[step] = "1"
        q1(step+1)
    elif input[step] == "1":
        input[step] = "1"
        q1(step+1)

q1(0)