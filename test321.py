def accSum(n):
    sum = 0
    for i in range(1, n+1): #[1,n+1)
        sum += i
    return sum

def jiazong(n):
    jiaz=accSum(n)*2
    return jiaz
