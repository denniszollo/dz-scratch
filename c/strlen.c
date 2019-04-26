#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

// Assuming I can use strnlen or other functions from string.h
// Will fail truncate string if it is longer than INT_MAX

char* strdup_every_other_char(const char* s) {
  // every other character plus null terminator 
  int len = (strnlen(s, INT_MAX) + 1)/2 + 1;
  char *ret = (char*) malloc(len * sizeof(char));
  ret[len] = '\0';
  int ret_index = 0;
  for(int i = 0; i < strnlen(s, INT_MAX); i+=2)
  {
    memcpy(&ret[ret_index], &s[i], 1);
    ret_index++;
  }
  return ret;
}

void main()
{
 char* out = strdup_every_other_char("D T");
 printf("%s", out);
 free(out);
}
