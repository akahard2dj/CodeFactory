class Solution:
    # @param {string} s
    # @return {integer}
    def lengthOfLastWord(self, s):
        splitStr = s.split()
        if not splitStr:
            return 0
        else:
            return len(splitStr[-1])
