#!/usr/bin/env python3
"""
Mapper script for Word Count MapReduce job
Reads text from stdin, tokenizes and emits (word, 1) pairs
"""
import sys
import re

def main():
    # Read from standard input
    for line in sys.stdin:
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Convert to lowercase and split into words
        # Remove punctuation and keep only alphanumeric characters
        words = re.findall(r'\b[a-z]+\b', line.lower())
        
        # Emit each word with count 1
        for word in words:
            if word:  # Skip empty strings
                print(f"{word}\t1")

if __name__ == "__main__":
    main()