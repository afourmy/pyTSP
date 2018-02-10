from random import randint

a = list(range(1, 10))
b = [9, 3, 7, 8, 2, 6, 5, 1, 4]

def order_crossover(i1, i2):
    n = len(i1)
    a = randint(1, n - 2)
    b = randint(a + 1, n)
    ni1, ni2, i1, i2 = i1[a:b], i2[a:b], i1[b:] + i1[:b], i2[b:] + i2[:b]
    for x in i1:
        if x in ni2: continue
        ni2.append(x)
    for x in i2:
        if x in ni1: continue
        ni1.append(x)
    return ni1, ni2
        
def maximal_preservative_crossover(i1, i2):
    n = len(i1)
    c = len(i1)//2
    r = randint(0, n)
    s1, s2 = (i1*2)[r:r+c], (i2*2)[r:r+c]
    for x in s1:
        i2.remove(x)
    for x in s2:
        i1.remove(x)
    ni1, ni2 = s2 + i1, s1 + i2
    return ni1, ni2

def partial_mapping(i1, i2, ni1, ni2, a, b):
    for x in i2[a:b]:
        if x in i1[a:b]:
            continue
        curr = x
        while True:
            index_curr = i2.index(curr)
            j = i1[index_curr]
            if not ni1[i2.index(j)]:
                ni1[i2.index(j)] = x
                break
            else:
                curr = ni2[i2.index(j)]
    
def partially_mapped_crossover(i1, i2):
    n = len(i1)
    a = randint(1, n - 2)
    b = randint(a + 1, n)
    ni1, ni2 = [0]*n, [0]*n
    ni1[a:b], ni2[a:b] = i1[a:b], i2[a:b]
    partial_mapping(i1, i2, ni1, ni2, a, b)
    partial_mapping(i2, i1, ni2, ni1, a, b)
    ni1 = [x if x else i2[i] for i, x in enumerate(ni1)]
    ni2 = [x if x else i1[i] for i, x in enumerate(ni2)]
    return ni1, ni2

def insertion_mutation(a):
    n = len(a)
    random_city, random_position = randint(0, n - 1), randint(0, n)
    city = a.pop(random_city)
    a.insert(random_position, city)

def displacement_mutation(i):
    n = len(i)
    a = randint(1, n - 2)
    b = randint(a + 1, n)
    random_position = randint(0, n)
    substring = i[a:b]
    i = i[:a] + i[b:]
    return i[:random_position] + substring + i[random_position:]
