def Jarvis(p,n):
    a = p
    CH_p = []
    p_start = [0,0]
    p_current = [0,0]
    min_x = a[0][0]
    min_index = 0
    for i in range (0, n):
        if a[i][0] < min_x:
            min_x = a[i][0]
            p_start = a[i]
    for i in range (0, n):
        if (a[i][0] == min_x):
            if (a[i][1] < a[min_index][1]):
                min_index = i
    p_start = a[min_index]
    a.insert(0, a[min_index])
    CH_p.append(p_start)
    p_next = p_start
    p_current_index = 0
    p_next_index = 1
    while (p_next_index != min_index):
        p_current = p_next
        p_next_index = p_current_index + 1
        p_next = a[p_next_index]
        for i in range (p_next_index + 1, n+1):
            p_i = a[i]
            S = (p_next[0] - p_current[0])*(p_i[1] - p_current[1]) - (p_next[1] - p_current[1])*(p_i[0] - p_current[0])
            if ((S < 0) or (S == 0 and not ((p_current[0]+p_current[1] < p_i[0]+p_i[1] < p_next[0]+p_next[1]) or (p_current[0]+p_current[1] > p_i[0]+p_i[1] > p_next[0]+p_next[1])))):
                p_next = p_i
                p_next_index = i
            
        CH_p.append(p_next)
        a.insert(p_current_index+1, a.pop(p_next_index))
        if (p_next_index > min_index):
            min_index += 1
    return CH_p
        
a = [[1,5],[3,6],[5,6],[3,4],[2,4],[1,3],[5,4],[5,2],[3,2],[1,1],[3,1]]
p = Jarvis(a,11)
print(p)
