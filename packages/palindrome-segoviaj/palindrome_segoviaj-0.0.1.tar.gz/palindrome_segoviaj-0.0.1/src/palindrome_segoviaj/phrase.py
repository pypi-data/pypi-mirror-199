import re

class Phrase:
    """A class to represent phrases."""

    def __init__(self, content):
        self.content = content

    def processed_content(self):
        """Process the content for palindrome testing."""
        return self.letters().lower()

    def ispalindrome(self):
        """Return True for a palindrome, False otherwise."""
        return self.processed_content() == reverse(self.processed_content())
    
    def letters(self):
        """Return the letters in the content"""
        return "".join(re.findall(r"[a-zA-Z]", self.content))
    
def reverse(string):
    """Reverse a string."""
    return "".join(reversed(string))