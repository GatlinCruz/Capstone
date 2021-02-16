q = [1,2,3,5,4,6,7,10,9,8,11,12,13,14,15,16,17,20,19,18]
count = 0
for i in range(len(q) - 2):
    if(q[i] > (i + 3)):
        print("error")
    elif(q[i] > (i + 2)):
        count += 2
    elif(q[i] > (i + 1)):
        count += 1
print(count)