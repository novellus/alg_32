# import bisect
# import labmath
# import math
# import re
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import sys
import tabulate


max_num = 1000000
max_iterations = 100 * max_num  # prevent very long computation cycles, will raise error
if len(sys.argv) > 1:
    max_num = int(sys.argv[1])


def alg_32(initial_num):
    num = initial_num
    iterations = 1
    iterates = [num]

    while num != 1:
        if iterations >= max_iterations:
            raise RuntimeError(f'Max Iterations Exceeded, for initial integer {initial_num}, current iterate {num} at iteration {iterations}\n{iterates[:10]}...{iterates[-10:]}')

        if num%2:
            num = num * 3 + 1
        else:
            num = num // 2

        iterations += 1
        iterates.append(num)

    return iterations, iterates


def pretty_print(index):
    # prints persistent data bin entries at specified index
    # prints binary and trinary data representations for iterates

    iterates = alg_32_iterates[index]
    iterations = list(range(1, len(iterates) + 1))
    binary_repr = [np.base_repr(num, base=2) for num in iterates]
    ternary_repr = [np.base_repr(num, base=3) for num in iterates]
    table_headers = ['iteration', 'iterate', 'parity', 'binary', 'ternary']
    table_data = list(zip(iterations, iterates, alg_32_iterate_parities[index], binary_repr, ternary_repr))

    print(f'''
initial integer: {nums[index]}
iteration length: {alg_32_iterations[index]}
max iterate: {alg_32_max_iterates[index]}, at iteration {alg_32_max_iterate_indeces[index]}
first power of 2: {alg_32_first_power_of_2s[index]} (2^{alg_32_first_power_of_2_exponents[index]})
Iterates:
''')

    print(tabulate.tabulate(table_data, table_headers, tablefmt='pipe'))



# prepare persistent data bins
nums = []
alg_32_iterations = []
alg_32_iterates = []
alg_32_iterate_parities = []
alg_32_max_iterates = []
alg_32_max_iterate_indeces = []
alg_32_first_power_of_2s = []
alg_32_first_power_of_2_exponents = []


def main():
    # populate basic data bins
    for num in range(1, max_num + 1):
        iterations, iterates = alg_32(num)
        nums.append(num)
        alg_32_iterations.append(iterations)
        alg_32_iterates.append(iterates)

        # populate simple comnputed data bins
        m = max(iterates)
        alg_32_max_iterates.append(m)
        alg_32_max_iterate_indeces.append(1 + iterates.index(m))

        iterate_parities = ['odd' if num%2 else 'even' for num in iterates]
        alg_32_iterate_parities.append(iterate_parities)

        # compute first power of 2 selected
        # first even number in the last set of even numbers before hitting 1
        index = len(iterate_parities) - 2
        while index > 0 and iterate_parities[index] == 'even':
            index -= 1

        if index == 0:
            if iterate_parities[0] == 'even':
                first_power_of_2 = iterates[0]
            else:
                first_power_of_2 = iterates[1]
        else:
            first_power_of_2 = iterates[index + 1]

        alg_32_first_power_of_2s.append(first_power_of_2)
        alg_32_first_power_of_2_exponents.append(first_power_of_2.bit_length() - 1)


def plot():
    # separated for profiling

    plt.figure()
    plt.title('Alg 32 Itertation Length\nFirst ' + str(max_num) + ' Positive Integers')
    plt.xlabel('initial integer')
    plt.ylabel('alg 32 iteration length')
    plt.scatter(nums, alg_32_iterations, s=2, marker='x')

    plt.figure()
    plt.title('Alg 32 Max Itertate\nFirst ' + str(max_num) + ' Positive Integers')
    plt.xlabel('initial integer')
    plt.ylabel('max iterate')
    plt.scatter(nums, alg_32_max_iterates, s=2, marker='x')
    plt.yscale('log')

    # plt.figure()
    # plt.title('Alg 32 First Power of 2 Selected as Iterate\nFirst ' + str(max_num) + ' Positive Integers')
    # plt.xlabel('initial integer')
    # plt.ylabel('first power of 2 selected as iterate')
    # plt.scatter(nums, alg_32_first_power_of_2s, s=2, marker='x')

    plt.figure()
    plt.title('Alg 32 First Power of 2 Exponent Selected as Iterate\nFirst ' + str(max_num) + ' Positive Integers')
    plt.xlabel('initial integer')
    plt.ylabel('first power of 2 exponent selected as iterate')
    plt.scatter(nums, alg_32_first_power_of_2_exponents, s=2, marker='x')

    plt.show()


# kernprof -l 99999_profile.py
# python -m line_profiler 99999_profile.py.lprof
main()
# pretty_print(len(nums) - 1)
pretty_print(alg_32_iterations.index(max(alg_32_iterations)))
plot()
