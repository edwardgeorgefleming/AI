import numpy as np
import time

n = 1000
TT = 1
iin = 2
    
A = np.zeros(n, dtype=int)
L = True
X = False
TX = 0
TnX = 0
TA = np.zeros(n, dtype=int)
TnA = np.zeros(n, dtype=int)
TAX = np.zeros(n, dtype=int)
TAnX = np.zeros(n, dtype=int)
TnAX = np.zeros(n, dtype=int)
TnAnX = np.zeros(n, dtype=int)
op = np.zeros(n, dtype=int)
label_not = np.zeros(n, dtype=int)
save_op = np.zeros(n, dtype=int)
save_label_not = np.zeros(n, dtype=int)
j1 = np.arange(n, dtype=int)
nj1 = n
check_okay = False
            
print('Start')

for k in range(20):
    start_time = time.time()
    e = 0
    Te = 0
    for ii in range(1 << iin):
        
        A = np.random.randint(2, size=n)
        
        X = A[1] and not A[10] and A[100]
        
        if L:
            TX = TX + X
            TnX = TnX + 1 - X
            for j in range(nj1):
                j2 = j1[j]
                TA[j2] = TA[j2] + A[j2]
                TnA[j2] = TnA[j2] + 1 - A[j2]
                TAX[j2] = TAX[j2] + A[j2] * X
                TAnX[j2] = TAnX[j2] + A[j2] * (1 - X)
                TnAX[j2] = TnAX[j2] + (1 - A[j2]) * X
                TnAnX[j2] = TnAnX[j2] + (1 - A[j2]) * (1 - X)
                
            overfit = False
            for j in range(nj1):
                op[j] = 0
                j2 = j1[j]
                if TA[j2] >= TT and TnA[j2] >= TT and TX >= TT and TnX >= TT:
                    if TnAnX[j2] == TnA[j2]:
                        op[j] = 1
                        label_not[j] = 0
                    if TAnX[j2] == TA[j2]:
                        op[j] = 1
                        label_not[j] = 1
                     
                    if TAX[j2] == TA[j2]:
                        op[j] = 2
                        label_not[j] = 0
                    if TnAX[j2] == TnA[j2]:
                        op[j] = 2
                        label_not[j] = 1
                else:
                    overfit = True
                    if not (save_op[j] == 1 or save_op[j] == 2):
                        op[j] = 3     
        
        Z = A[j1[0]] != save_label_not[0]
        for j in range(1,nj1):
            if save_op[j] == 1:
                Z = Z and (A[j1[j]] != save_label_not[j])
            if save_op[j] == 2:
                Z = Z or (A[j1[j]] != save_label_not[j])
                           
        Te += 1
        if Z == X:
            e += 1

        if L:    
            j_index = 0
            for j in range(nj1):
                if op[j] != 0:
                    j1[j_index] = j1[j]
                    save_op[j_index] = op[j]
                    save_label_not[j_index] = label_not[j]
                    j_index += 1
            nj1 = j_index

    total_time = time.time() - start_time
    if Te != 0:
        print()
        print('Total Elased Time = ', total_time)
        print('The Average Elapsed Time for one cycle = ', total_time / Te, end = '')
        print(' Seconds.')
        print()
        if overfit:
            print('Data is Overfitted.')
        else:
            print('Accuracy = ', e , end = '')
            print(' / ', Te, end = '')
            print(' = ',e/Te)
            print()
            
    if not overfit:
        print('Boolean Equation = ', end = '')
            
        count = 0
        for j in range(nj1):
            count = count + 1 if save_op[j] == 2 else count
        if count <= 50:
            for j in range(nj1):
                if save_op[j] == 2:
                    count -= 1
                    if save_label_not[j]:
                        print('NOT ', end = '')
                    print('A[',j1[j], end = '')
                    if count <= 0:
                        print(']')
                    else:
                        print('] OR ', end = '')
        else:
            print(' > 50 Variables')
                    
        count = 0
        for j in range(nj1):
            count = count + 1 if save_op[j] == 1 else count
        if count <= 50:
            for j in range(nj1):
                if save_op[j] == 1:
                    count -= 1
                    if save_label_not[j]:
                        print('NOT ', end = '')
                    print('A[',j1[j], end = '')
                    if count <= 0:
                        print(']')
                    else:
                        print('] AND ', end = '')
        else:
            print(' > 50 Variables')
            
    print()
    print('Completed checked with 2 to the', iin, end = '')
    print(' power of random states.')
    print()
        
    answer = input('Do you want to EXIT the program? (y or n)? ')
    if answer == 'y':
        break
    
    answer = input('Do you want to go to the "AS TAUGHT MODE"  (y or n)? ')
    if answer == 'y':
        L = False
    else:
        L = True
    iin = int(input('Enter in the power of 2 you would like to check next = '))
                      
print('Done')
                                        
                    
