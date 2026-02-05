#!/usr/bin/env python3
"""
Reducer script for Word Count MapReduce job
Reads (word, count) pairs from stdin and aggregates counts per word
"""
import sys
from collections import defaultdict

def main():
    current_word = None
    current_count = 0
    
    # Read from standard input
    for line in sys.stdin:
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Parse the input from mapper
        try:
            word, count = line.split('\t', 1)
            count = int(count)
        except ValueError:
            # Skip malformed lines
            continue
        
        # If we're still on the same word, accumulate count
        if current_word == word:
            current_count += count
        else:
            # New word encountered
            if current_word:
                # Output the previous word and its total count
                print(f"{current_word}\t{current_count}")
            
            current_word = word
            current_count = count
    
    # Output the last word
    if current_word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    main()