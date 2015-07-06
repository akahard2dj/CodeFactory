class Solution:
    # @param {integer[]} nums
    # @param {integer} k
    # @return {integer}
    def qsort(self, arr):
        if len(arr) <= 1:
          return arr
        else:
          return self.qsort([x for x in arr[1:] if x>=arr[0]]) + [arr[0]] + self.qsort([x for x in arr[1:] if x<arr[0]])
    def findKthLargest(self, nums, k):
        sortedNums = self.qsort(nums)
        return sortedNums[k-1]
