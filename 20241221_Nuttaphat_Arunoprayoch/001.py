# 001
# Fixed Point
# ---
# Given an array of distinct integers `arr`, where `arr` is sorted in **ascending order**, return the smallest index `i` that satisfies `arr[i] == i`. If there is no such index, return `-1`.
# ---
# Example 1:
# ```
# Input: arr = [-10,-5,0,3,7]
# Output: 3
# Explanation: For the given array, arr[0] = -10, arr[1] = -5, arr[2] = 0, arr[3] = 3, thus the output is 3.
# ```
# Example 2:
# ```
# Input: arr = [0,2,5,8,17]
# Output: 0
# Explanation: arr[0] = 0, thus the output is 0.
# ```

# Time complexity: O(n)
# def fixed_point(arr):
#     for i in range(len(arr)):
#         if arr[i] == i:
#             return i
#     return -1

# Time complexity: O(log n)
# NOTE: Since the array is sorted, we can use binary search to find the fixed point.
def fixed_point(arr: list[int]) -> int:
    """Find the smallest index i that satisfies arr[i] == i.

    Args:
        arr (list[int]): A list of distinct integers sorted in ascending order.

    Returns:
        int: The smallest index i that satisfies arr[i] == i. If there is no such index, return -1.
    """
    left, right = 0, len(arr) - 1
    result = -1  # Initialize result to -1 to indicate no fixed point found
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == mid:
            result = mid  # Update the result to the current fixed point
            right = mid - 1  # Continue searching in the left half for a smaller index
        elif arr[mid] < mid:
            left = mid + 1
        else:
            right = mid - 1
    return result


# Test cases
print(fixed_point([-10, -5, 0, 3, 7]))  # 3
print(fixed_point([0, 2, 5, 8, 17]))  # 0
print(fixed_point([-10, 1, 2, 3, 7]))  # 1
