def calculate_distances(n, m):
    distances = [1 + (i ** 2 % m) for i in range(n)]
    return distances


def is_possible(max_jump, distances, j):
    n = len(distances)
    jumps = 0
    current_distance = 0

    for i in range(n):
        if distances[i] > max_jump:
            return False
        current_distance += distances[i]
        if current_distance > max_jump:
            jumps += 1
            current_distance = distances[i]
        if jumps > j:
            return False

    return jumps + 1 <= j


def find_minimum_max_jump(n, m, j):
    distances = calculate_distances(n, m)
    low, high = 1, sum(distances)

    while low < high:
        mid = (low + high) // 2
        if is_possible(mid, distances, j):
            high = mid
        else:
            low = mid + 1

    return low


def main():
    n, m, j = map(int, input().split())

    min_max_jump = find_minimum_max_jump(n, m, j)

    print(min_max_jump)

if __name__ == "__main__":
    main()