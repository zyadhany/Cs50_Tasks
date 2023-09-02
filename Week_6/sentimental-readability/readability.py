# TODO
# take the text
S = input("Text: ")

w = 1.0
l = 0.0
s = 0.0

# count l and s and w
for c in S:
    if c == ' ':
        w += 1
    elif (c == '!' or c == '.' or c == '?'):
        s += 1
    elif c.islower() or c.isupper():
        l += 1

# calculate tthe grade
l = (l / w) * 100
s = (s / w) * 100
grade = round(0.0588 * l - 0.296 * s - 15.8)
if (grade > 16):
    print("Grade 16+\n")
elif (grade < 1):
    print("Before Grade 1\n")
else:
    print("Grade", grade)
