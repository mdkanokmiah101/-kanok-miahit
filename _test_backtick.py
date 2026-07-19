#!/usr/bin/env python3
"""Test backtick handling."""
ch = '`'
print('backtick repr:', repr(ch))
print('backtick ord:', ord(ch))

text = 'content: `hello world`'
idx = text.find(':')
print('colon at:', idx)
print('after colon:', repr(text[idx+1:]))
i = idx + 1
while i < len(text) and text[i] == ' ':
    i += 1
print('char at i:', repr(text[i]), 'ord:', ord(text[i]))
print('ch == text[i]:', ch == text[i])
print('ch == text[i] using ord:', ord(ch) == ord(text[i]))
