import heapq

nums = int(input())
num_count = input().split()
minimum = []
maximum = []
count = 0
first_heap = heapq
second_heap = heapq

for i in num_count:
    j = int(i)
    if minimum == []:
        first_heap.heappush(minimum, j)
    elif maximum == []:
        if j < minimum[0]:
            second_heap.heappush(maximum, j * -1)
        else:
            abc = first_heap.heappop(minimum)
            second_heap.heappush(maximum, abc * -1)
            first_heap.heappush(minimum, j)

    elif len(minimum) < len(maximum):
        if j < maximum[0] * -1:
            abc = second_heap.heappop(maximum)
            first_heap.heappush(minimum, abc * -1)
            second_heap.heappush(maximum, j *-1)
        else:
            first_heap.heappush(minimum, j)

    elif len(maximum) < len(minimum):
        if j < minimum[0]:
            second_heap.heappush(maximum, j * -1)
        else:
            abc = first_heap.heappop(minimum)
            second_heap.heappush(maximum, abc * -1)
            first_heap.heappush(minimum, j)
    else:
        if j < maximum[0] * -1:
            second_heap.heappush(maximum, j * -1)
        else:
            first_heap.heappush(minimum, j)
    if count == nums -1:
        a = "\n"
    else:
        a= " "
    if len(minimum) > len(maximum):
        print(f"{minimum[0]}", end=a)
    elif len(minimum) < len(maximum):
        print(f"{maximum[0] * -1}", end=a)
    else:
        print(f"{maximum[0] * -1}", end=a)
    count +=1

