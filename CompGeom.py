def mk_OP(a):      # построение ограничительного прямоугольника
    x1 = min(a[0][0],a[2][0])
    x2 = max(a[0][0],a[2][0])
    y1 = min(a[0][1],a[2][1])
    y2 = max(a[0][1],a[2][1])
    t1 = [x1,y1]
    t2 = [x2,y2]
    p = [t1,t2]
    return p

def find_OP_cross(p1,p2): # нахождение пересечеений между ограничительными прямоугольниками
    if((p1[1][0] >= p2[0][0]) and (p2[1][0] >= p1[0][0]) and (p1[1][1] >= p2[0][1]) and (p2[1][1] >= p1[0][1])):
        return True
    else:
        return False
    
def area(a,b,c):  # ориентированная площадь треугольника
    S = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    return S

def exact_method(a,b):  # точный метод определения пересечения 2-х отрезков
    S1 = area(a[0],a[2],b[0])
    S2 = area(a[0],a[2],b[2])
    S3 = area(b[0],b[2],a[0])
    S4 = area(b[0],b[2],a[2])
    if (S1 * S2 > 0) or (S3 * S4 > 0):
        return 0 # не пересекаются
    elif (S1 == 0) and (S2 == 0) and (S3 == 0) and (S4 == 0):
        return -1 # накладываются друг на друга (пресекаются и лежат на одной прямой)
    else: 
        return 1 # все остальные случаи, когда отрезки не пересекаются, были отброшены на первом этапе
    

def PPPO(a,b): # эффективный метод проверки пересечения 2-х отрезков
    if not(find_OP_cross(mk_OP(a),mk_OP(b))):
        return 0
    else:
        return exact_method(a,b)

def cross(a,b): # координаты точки пересечения 2-х отрезков  (если они на одной прямой, то за точку пересечения берётся точка конца отрезка, которая пересекается с другим отрезком)
    p = PPPO(a,b)
    if (p == 1):
        A1 = a[0][1] - a[2][1]
        B1 = a[2][0] - a[0][0]
        C1 = a[0][0]*a[2][1] - a[2][0]*a[0][1]
        
        A2 = b[0][1] - b[2][1]
        B2 = b[2][0] - b[0][0]
        C2 = b[0][0]*b[2][1] - b[2][0]*b[0][1]
       
        x = (B2*C1 - B1*C2) / (A2*B1 - A1*B2)
        if (B1 != 0):
            y = (-A1*x - C1) / B1
        else:
            y = (-A2*x - C2) / B2
        c = [x,y]
    elif (p == -1):
        if (a[2][0] < b[2][0]):
            c = a[2]
        elif (a[2][0] > b[2][0]):
            c = b[2]
        elif (a[2][1] < b[2][1]):
            c = a[2]
        else:
            c = b[2]
    return c
        
def sorter(mas): # сортировка координат точек начала и конца отрезков списка mas по возрастанию х, если же х1 == х2, то по у
    for i in range (0,len(mas)):
        if (mas[i][0][0] > mas[i][1][0]) or ((mas[i][0][0] == mas[i][1][0]) and (mas[i][0][1] > mas[i][1][1])):
            mas[i][0],mas[i][1] = mas[i][1],mas[i][0]
    return mas

def Q_push(Q,seg): # добавление координат точек в траекторию заметающей прямой (по возрастанию х с приоритетом координат точек начала)
    i = 0
    for i in range(0,3,2):
        j = 0
        min_x_index = 0
        while (j < len(Q)) and (seg[i][0] > Q[j][0]):
            j += 1
            min_x_index = j
        if (min_x_index != len(Q)) and (seg[i][0] == Q[min_x_index][0]) and (i == 2): ## только 2 точка, чтобы подвинуть концы отрезков дальше 
            while (j < len(Q)) and (seg[i][0] == Q[j][0]):                            ## (первыми рассматриваются их начала, чтобы не потерять точки пересечения)
                j += 1
                min_x_index = j
                
        Q.insert(min_x_index,seg[i])

def Q_pop(Q): # удаление координат первой точки из траектории заметающей прямой
    return Q.pop(0)

def A_belong(A,el): # проверка на принадлежность элемента к списку пересекающихся прямых
    len_A = len(A)
    i = 0
    while (i < len_A) and (A[i] != [el[0],el[1]]) and (A[i] != [el[1],el[0]]):
        i += 1
    if (i == len_A):
        return 0
    else:
        return 1

def L_refresh(L, y_max, y_min, x, A): # обновление статуса заметающей прямой
    line = [[x,y_min],[x,y_min],[x,y_max]]
    len_L = len(L)
    for i in range(0,len_L):
        L[i][1] = cross(line, L[i])
    for i in range (len_L,1,-1):
        if ( i == len_L):
            for j in range (0,len_L-1):
                for k in range (j+1,len_L):
                    x1 = L[j][0]
                    y1 = L[j][2]
                    x2 = L[k][0]
                    y2 = L[k][2]
                    if ( (x1[0] == y1[0] == x2[0] == y2[0]) and
                         (y1[1] >= x2[1]) and
                         (y2[1] >= x1[1]) ) and not A_belong(A,[[x1,y1],[x2,y2]]):
                        A.append([[x1,y1],[x2,y2]])
        max_y = max(L[j][1][1] for j in range (i-1,-1,-1))
        j = 0
        while (j < i) and (L[j][1][1] != max_y):
            j += 1
        for k in range (j+1,i):
            x1 = L[j][0]
            y1 = L[j][2]
            x2 = L[k][0]
            y2 = L[k][2]
            if not A_belong(A,[[x1,y1],[x2,y2]]):
                A.append([[x1,y1],[x2,y2]])
                L[j],L[k] = L[k],L[j]
            j = k
    

def L_push(seg, L): # вставка нового отрезка в список текущих проверяемых отрезков
    len_L = len(L)
    min_y_index = 0
    i = 0
    while (i < len_L) and (seg[0][1] > L[i][1][1]):
        i += 1
        min_y_index = i
    L.insert(min_y_index,seg)

def L_pop(seg, L): # удаление отрезка из списока текущих проверяемых отрезков
    len_L = len(L)
    seg_index = -1
    i = 0
    while (i < len_L) and (seg_index == -1):
        if (seg[0] == L[i][0]) and (seg[2] == L[i][2]):
            seg_index = i
        i += 1
    L.pop(seg_index)

def belong(L,seg): # проверка принадлежности отрезка seg списку отрезков L
    len_L = len(L)
    i = 0
    while (i < len_L) and (L[i] != seg):
        i += 1
    if (i == len_L):
        return 0
    else:
        return 1

def find(P, L, p): # поиск такого отрезка seg из Р, у которого одна из координат == p, в приоритете начала отрезков, которх нет в списке заметающей прямой L
    i = 0
    seg = None
    while (i < len(P)):
        if (P[i][0] == p)  and not belong(L,P[i]):
            if (seg == None):
                seg = P[i]
            elif (seg[2][1] > P[i][2][1]) or (seg[2][1] == P[i][2][1] and seg[2][0] < P[i][2][0]):
                seg = P[i]
        i += 1
    if (seg == None):
        i = 0
        while (i < len(P)) and (P[i][2] != p):
            i += 1
        seg = P[i]
        P.pop(i)
    return seg

def VPO(P): # поиск всех пересекающихся отрезков на плоскости
    a = list(P)
    a = sorter(a)
    for i in range (0,len(a)):
        a[i].insert(1,a[i][0])
    y_max = max(max(a[i][0][1],a[i][2][1]) for i in range (0,len(a)))
    y_min = min(min(a[i][0][1],a[i][2][1]) for i in range (0,len(a)))
    LP = []
    SL = []
    C = []
    push_prev = None
    pop_prev = None
    for i in range (0,len(a)):
        Q_push(LP,a[i])
    print ("СПИСОК ТОЧЕК СОБЫТИЙ (точек перемещения прямой SL):")
    for i in range (0,len(LP)):
        print ("Q = ",LP[i])
    while len(LP) != 0:
        p = Q_pop(LP)
        seg = find(a,SL,p)
        if (p == seg[0]):
            if (push_prev != None) and (p != push_prev) and (p[1] == push_prev[1]):## обновляем статус, только когда y-координата предыдущей
                L_refresh(SL, y_max, y_min, p[0], C)                               ## точки == у-координате текущей (чтобы избежать ложных пересечений)
            L_push(seg,SL)
            push_prev = p
        elif (p == seg[2]):
            if (pop_prev == None) or (p[0] != pop_prev): ## нет смысла обновлять статус, если мы уже были в этой точке
                L_refresh(SL, y_max, y_min, p[0], C)            
            L_pop(seg,SL)
            pop_prev = p[0]
    print ("СПИСОК ПАР ПЕРЕСЕККАЮЩИХСЯ ОТРЕЗОВ:")
    for i in range (len(C)):
        print ("Cross[",i,"] = ",C[i])
    for i in range (0,len(P)):
        P[i].pop(1)
    return C

def TPM (A): # проверка простоты многоугольника
    C = VPO(A)
    if (len(C) > len(A)):
        return 0 ## непростой
    elif (len(C) == len(A)):
        return 1 ## простой
    

def exist_versa(A,M): # проверка существования противоположно лежащих отрезков, относительно горизонтального отрезка P, 
    line_y = A[0][0][0][1]                                                                                       #\ _P_
    P = M[1]                                                                                                     #      \      
    up_left = -1           
    down_left = -1
    up_right = -1
    down_right = -1
    for i in range (0,len(A)):
        J = A[i][1]
        if   J[0] == P[0]:
            if J[1][1] > line_y:
                up_left = i
            elif J[1][1] < line_y:
                down_left = i
        elif J[1] == P[0]:
            if J[0][1] > line_y:
                up_left = i
            elif J[0][1] < line_y:
                down_left = i
        elif J[0] == P[1]:
            if J[1][1] > line_y:
                up_right = i
            elif J[1][1] < line_y:
                down_right = i
        elif J[1] == P[1]:
            if J[0][1] > line_y:
                up_right = i
            elif J[0][1] < line_y:
                down_right = i
    if (down_left != -1 and up_right != -1):
        A.pop(down_left)
        if (down_left > up_right):
            A.pop(up_right)
        else:
            A.pop(up_right-1)
        return True
    elif (up_left != -1 and down_right != -1):
        A.pop(up_left)
        if (up_left > down_right):
            A.pop(down_right)
        else:
            A.pop(down_right-1)
        return True
    elif down_left != -1:
        A.pop(down_left)
        if (down_left > down_right):
            A.pop(down_right)
        else:
            A.pop(down_right-1)
        return False
    else:
        A.pop(up_left)
        if (up_left > up_right):
            A.pop(up_right)
        else:
            A.pop(up_right-1)
        return False

def one_side(A,M): # проверка вершины многоугольника - True, если оба других рёбер, формирующих вершину, находятся по одну сторону
    line_y = A[0][0][0][1]#                                                                             \/  или  /\
    P = M[1]
    up = 0
    down = 0
    if (P[0][1] == line_y):
        k = P[0]
        if (P[1][1] > line_y):
            up = 1
        elif (P[1][1] < line_y):
            down = 1
    elif P[1][1] == line_y:
        k = P[1]
        if (P[0][1] > line_y):
            up = 1
        elif (P[0][1] < line_y):
            down = 1

    i = 0
    while (i < len(A)) and (up == 1 and down == 0 or down == 1 and up == 0):
        J = A[i][1]
        if (((J[0] == k) and (J[1][1] > line_y)) or ((J[1] == k) and (J[0][1] > line_y)) ):
            up = i
        elif (((J[0] == k) and (J[1][1] < line_y)) or ((J[1][1] == k) and (J[0][1] < line_y)) ):
            down = i
    if (up == 0):
        A.pop(down)
        return True
    elif down == 0:
        A.pop(down)
        return True
    elif (up == 1):
        A.pop(down)
        return False
    else:
        A.pop(up)
        return False
    
def PPM(P1,P2): # проверка пересечения 2-х любых многоугольников
    P1 = sorter(P1)
    P2 = sorter(P2)
    len_P1 = len(P1)
    len_P2 = len(P2)
    max_p1_x = max(P1[i][1][0] for i in range (0,len_P1))
    min_p1_x = min(P1[i][0][0] for i in range (0,len_P1))
    max_p1_y = max(max(P1[i][0][1],P1[i][1][1]) for i in range (0,len_P1))
    min_p1_y = min(min(P1[i][0][1],P1[i][1][1]) for i in range (0,len_P1))
    square_P1 = [[min_p1_x, min_p1_y], [max_p1_x,max_p1_y]]
        
    max_p2_x = max(P2[i][1][0] for i in range (0,len_P2))
    min_p2_x = min(P2[i][0][0] for i in range (0,len_P2))
    max_p2_y = max(max(P2[i][0][1],P2[i][1][1]) for i in range (0,len_P2))
    min_p2_y = min(min(P2[i][0][1],P2[i][1][1]) for i in range (0,len_P2))
    square_P2 = [[min_p2_x, min_p2_y], [max_p2_x,max_p2_y]]
    if find_OP_cross(square_P1,square_P2):
        S = []
        for i in range (0, len_P1):
            S.append(P1[i])
        for i in range (0, len_P2):
            S.append(P2[i])
        C = VPO(S)
        len_C = len(C)
        
        i = 0
        while (i < len_C) and ((belong(P1,C[i][0]) and (belong(P1,C[i][1]))) or (belong(P2,C[i][0]) and (belong(P2,C[i][1])))):
            i += 1
        if (i == len_C):
            s = 0
            F = []
            if (square_P1[0][0] < square_P2[0][0]):
                point = P2[0][0]
                t = [max_p1_x+1,point[1]]
                Q = P1
            else:
                point = P1[0][0]
                t = [max_p2_x+1,point[1]]
                Q = P2

            min_y = point[1]
            line = [point,t]
            F.append(line)
            for i in range (0,len(Q)):
                if (((Q[i][0][0] > point[0]) or (Q[i][1][0] > point[0])) and
                    ((Q[i][0][1] <= point[1] and Q[i][1][1] >= point[1]) or (Q[i][0][1] >= point[1] and Q[i][1][1] <= point[1]))):
                    F.append(Q[i])
            
            K = VPO(F)
            
            i = 0
            while (i < len(K)):
                if (K[i][1] == line):
                    K[i][0],K[i][1] = K[i][1],K[i][0]
                    i += 1
                elif (K[i][0] != line):
                    K.pop(i)
                else:
                    i += 1
            for i in range (0,len(K)):
                if (K[i][1][0][1] == K[i][1][1][1]):
                    K.insert(0,K.pop(i))
            print ("ПЕРЕСЕЧЕНИЯ ГОРИЗОНАЛЬНОЙ ОТРЕЗКА ",line, "С РЁБРАМИ ВНЕШНЕГО МНОГОУГОЛЬНИКА:")
            for i in range(0,len(K)):
                print("CROSS[",i,"] = ",K[i])
            i = 0
            while (i < len(K)):
                J = K[i][1]
                if (J[0][1] == J[1][1]):
                    if exist_versa(K,K.pop(i)):
                        s += 1
                    else:
                        s += 2
                elif (J[0][1] == min_y) or (J[1][1] == min_y):
                    if one_side(K,K.pop(i)):
                        s += 2
                    else:
                        s += 1
                else:
                    s += 1
                    i += 1
            if s % 2 == 0:
                print("ВИД ПЕРЕСЕЧЕНИЯ: ",end = "")
                return 0
            else:
                print("ВИД ПЕРЕСЕЧЕНИЯ: ",end = "")
                return -1 # один внутри другого
        else:
            print("ВИД ПЕРЕСЕЧЕНИЯ: ",end = "")
            return 1 # пересекаются 
                            
                        
    else:
        print("ВИД ПЕРЕСЕЧЕНИЯ: ",end = "")
        return 0 #не пересекаются

        
## ВСЕ ЧЕРТЕЖИ ЕСТЬ/БУДУТ В ПРЕЗЕНТАЦИИ!!!
## для VPO()    
            
P = [[[2,1],[10,3]], ## хаотично расположенные отрезки с различными случаями пересечений и наклона (тривиальные и нет)
     [[1,7],[11,2]],
     [[4,2],[5,3]],
     [[1,4],[2,5]],
     [[4,4],[5,3]],
     [[2,3],[3,2]],
     [[2,3],[2,4]], [[2,4],[2,5]], [[2,1],[2,3]],
     [[6,3],[7,3]]]

U = [[[4,1],[2,1]], ## 6-угольник
     [[4,1],[5,2]],
     [[2,3],[4,3]],
     [[2,3],[1,2]],
     [[5,2],[4,3]],
     [[2,1],[1,2]]]

S = [[[2,0],[4,7]], ## звезда из примера для ВПО в презентации
     [[4,7],[6,0]],
     [[6,0],[0,6]],
     [[0,6],[8,6]],
     [[8,6],[2,0]]]

T = [[[3,0],[3,4]], ## треугольник с тремя медианами
     [[5,3],[1,1]],
     [[1,3],[5,1]],
     [[1,1],[5,1]],
     [[5,1],[3,4]],
     [[3,4],[1,1]]]

V = [[[1,0],[0,6]], ## пример, когда есть 15 точек пересечения от 6 отрезков
     [[2,0],[0,5]],
     [[3,0],[0,4]],
     [[4,0],[0,3]],
     [[5,0],[0,2]],
     [[6,0],[0,1]]]

## для PPM() и TPM()

G1 = [[[3,1],[1,3]], ## фигура, напоминающая букву G 
      [[1,3],[1,5]],
      [[1,5],[3,7]],
      [[3,7],[5,7]],
      [[5,7],[7,5]],
      [[7,5],[5,5]],
      [[5,5],[5,3]],
      [[5,3],[7,3]],
      [[7,3],[7,4]],
      [[7,4],[8,4]],
      [[8,4],[8,2]],
      [[8,2],[5,1]],
      [[5,1],[3,1]]]

G2 = [[[3,1],[1,3]], ## фигура, напоминающая букву G, со скошенным заворотом 
      [[1,3],[1,5]],
      [[1,5],[3,7]],
      [[3,7],[5,7]],
      [[5,7],[7,5]],
      [[7,5],[5,5]],
      [[5,5],[5,3]],
      [[5,3],[8,4]],
      [[8,4],[8,2]],
      [[8,2],[5,1]],
      [[5,1],[3,1]]]

N1 = [[[1,1],[1,7]], ## непростой многоугольник (2 треугольника)
      [[1,7],[10,2]],
      [[10,2],[10,6]],
      [[10,6],[1,1]]]

N2 = [[[1,1],[1,7]], ## непростой многоугольник, с нетривиальным случаем расположения одного рёбер
      [[1,7],[8,3]],
      [[8,3],[9,5]],
      [[9,5],[10,1]],
      [[10,1],[12,5]],
      [[12,5],[12,3]],
      [[12,3],[5,3]],
      [[5,3],[5,2]],
      [[5,2],[1,1]]]

S1 = [[[8,5],[10,5]], ## квадрат 2х2 с левой нижней вершиной в точке [8,5] (для пересечения с G1 или G2 -- для случая, когда ограничивающие прямоугольники не пересекаются)
      [[10,5],[10,7]],
      [[10,7],[8,7]],
      [[8,7],[8,5]]]

S2 = [[[6,6],[8,6]], ## квадрат 2х2 с левой нижней вершиной в точке [6,6] (для пересечения с G1 или G2 -- касание в точке [6,6])
      [[8,6],[8,8]],
      [[8,8],[6,8]],
      [[6,8],[6,6]]]

S3 = [[[2,3],[4,3]], ## квадрат 2х2 с левой нижней вершиной в точке [2,3] (для пересечения с G1, G2, N1 или N2 --для случая "внутри")
      [[4,3],[4,5]],
      [[4,5],[2,5]],
      [[2,5],[2,3]]]

S4 = [[[5.5,3.5],[6.5,3.5]], ## квадрат 1х1 с левой нижней вершиной в точке [5.5,3.5] (для пересечения с G1 -- случай, когда ограничивающий прямоугольник одного многоугольника 
      [[6.5,3.5],[6.5,4.5]], ## оказался внутри другого, но при этом нет случая "один внутри другого") 
      [[6.5,4.5],[5.5,4.5]],
      [[5.5,4.5],[5.5,3.5]]]

K = PPM (G1,S4)
print (K)

