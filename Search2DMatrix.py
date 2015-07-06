class Solution:
    # @param {integer[][]} matrix
    # @param {integer} target
    # @return {boolean}
    def searchMatrix(self, matrix, target):
        if matrix==None or len(matrix)==0:
            return False
            
        start=0
        end=len(matrix)*len(matrix[0])-1
            
        while (start<=end):
            mid=start+(end-start)/2
                
            if matrix[mid/len(matrix[0])][mid%len(matrix[0])]==target:
                return True
                
            elif matrix[mid/len(matrix[0])][mid%len(matrix[0])]<target:
                start=mid+1
            else:
                end=mid-1
            
        return False
