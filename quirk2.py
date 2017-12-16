for n in range(2, 7):
    vec = list(map(str,range(n)))
    while True:
        temp = vec.pop()
        for i in range(n):
            vec.insert(0, str(i) + temp)
        if len(vec[-1]) == n:
            break
    vec.sort()
    quirk = 0
    for i in vec:
        for index_j, term_j in enumerate(i):
            for k in i[index_j + 1:]:
                if int(term_j) > int(k):
                    quirk += 1
    print("Number of quirks in vec of size %d is %d" % (n, quirk))
