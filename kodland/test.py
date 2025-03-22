
class Solution:
    def isPalindrome(self, x):
        x = str(x)  # Convert number to string
        rev = ''.join(reversed(x))  # Reverse the string
        return rev == x  # Check if reversed string matches original

# Create an instance of the class and test
solution = Solution()
x = '121'
result = solution.isPalindrome(x)
print(result)  # Output: True
