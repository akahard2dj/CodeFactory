class Solution:
    # @param {string} s
    # @return {boolean}
    def isValid(self, s):
        stack = []
        for i in range(0, len(s)):
            if s[i] == '(' or s[i] == '[' or s[i] == '{':
                stack.append(s[i])
            else:
                if len(stack)==0:
                    return False
                lastOpenParenthesis = stack.pop()
                if (s[i]==')' and lastOpenParenthesis !='(') or (s[i]==']' and lastOpenParenthesis !='[') or (s[i]=='}' and lastOpenParenthesis !='{'):
                    return False
        return len(stack)==0
