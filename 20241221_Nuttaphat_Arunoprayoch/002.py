# 002
# Part 2:  Two Sum Less Than K
# ---
# Given an array A of integers and integer K. Any integer pair in A could be combined as a set. Find and return all combinations of sets where the sum S of elements is the maximum but less than K ( a, b are in A and a + b = S < K and S is maximum, return [a, b] ). The answer must exclude duplicates, but it's fine in any order. e.g. [1, 2] or [2, 1] may be treated as the same, no need to return twice in one output. Please answer the time complexity of your program, too.
# Free to use any programing language
# ---
# Example 1:
# ```
# Input: A = [1, 2, 3, 4]. K = 4
# Output: [[1, 2]], because 1+2 = 3 < 4
# ```
# Example 2:
# ```
# Input: A = [1, 2, 3]. K = 3
# Output: []
# ```
# Example 3:
# ```
# Input: A = [1, 2, 2, 3, 4]. K = 5
# Output: [[1, 3], [2, 2]], because both `1+3` and `2+2` are 4 < 5
# ```


# # Time complexity: O(n^2).
# def two_sum_less_than_k(arr: list[int], k: int) -> list[list[int]]:
#     """Find all combinations of sets where the sum S of elements is the maximum but less than K.

#     Args:
#         arr (list[int]): A list of integers.
#         k (int): An integer K.

#     Returns:
#         list[list[int]]: All combinations of sets where the sum S of elements is the maximum but less than K.
#     """
#     result = []
#     max_sum = float('-inf')  # Initialize the maximum sum as negative infinity
#     seen = set()

#     for num in arr:
#         for seen_num in seen:
#             total = num + seen_num
#             if total < k:
#                 if total > max_sum:
#                     result = [[seen_num, num]]  # Start a new result list with the current pair
#                     max_sum = total
#                 elif total == max_sum:
#                     result.append([seen_num, num])  # Add to the current result list
#         seen.add(num)  # Add the current number to the seen set

#     return result


# Time complexity: O(n log n)
# NOTE: Since the array is not sorted, we need to sort it first. Then, we can use two pointers to find the maximum sum that is less than K.
def two_sum_less_than_k(arr: list[int], k: int) -> list[list[int]]:
    """Find all combinations of sets where the sum S of elements is the maximum but less than K.

    Args:
        arr (list[int]): A list of integers.
        k (int): An integer K.

    Returns:
        list[list[int]]: All combinations of sets where the sum S of elements is the maximum but less than K.
    """
    # Sort the array
    arr.sort()

    # Initialize two pointers
    left, right = 0, len(arr) - 1
    result = []
    max_sum = float('-inf')  # Init the maximum sum as negative infinity

    # Use two pointers to find the maximum sum that is less than K
    while left < right:

        # Calculate the sum of two elements
        total = arr[left] + arr[right]

        # If the sum is less than K, update the result
        if total < k:

            # If the sum is greater than the current maximum sum, update the result
            if total > max_sum:
                result = [[arr[left], arr[right]]]
                max_sum = total

            # If the sum is equal to the current maximum sum, append the result
            elif total == max_sum:
                result.append([arr[left], arr[right]])

            # Move the left pointer to the right
            left += 1

        else:
            # Move the right pointer to the left
            right -= 1

    return result


# Test cases
print(two_sum_less_than_k([1, 2, 3, 4], 4))  # [[1, 2]]
print(two_sum_less_than_k([1, 2, 3], 3))  # []
print(two_sum_less_than_k([1, 2, 2, 3, 4], 5))  # [[1, 3], [2, 2]]
