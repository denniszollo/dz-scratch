#include <stdio.h>


struct temp {
  int integers[10];
  char characters[10];
};

void main(void)
{
struct temp mine;

printf("sizeof integers is %d, sizeof characters is %d", sizeof(mine.integers), sizeof(mine.characters));
}
