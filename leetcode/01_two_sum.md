### Problem:

Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

```
Given nums = [2, 7, 11, 15], target =9,


Because nums[0] + nums[1] = 2 + 7 = 9,

return [0, 1]
```

### Solution:

```go
func twoSum(nums []int, target int) []int {
    lookup := make(map[int]int)
	for i, num := range nums {
		if j, ok := lookup[target - num]; ok {
			return []int{j, i}
		}
		lookup[nums[i]] = i
	}
	return nil
}
```
