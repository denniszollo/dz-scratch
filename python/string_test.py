def strdup_every_other_char(s):
    new_string = []
    for i,char in enumerate(s):
        if i %2 == 0:
            new_string.append(char)
    return ''.join(new_string)




print strdup_every_other_char("house")
print strdup_every_other_char("h ")
print strdup_every_other_char("D E N N I S")
