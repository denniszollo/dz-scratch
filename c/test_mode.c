#include<stdio.h>
void main() {

  unsigned char mode = 0;
  unsigned char ins = 0;

  mode = 1;
  ins = 1;

  unsigned int out = 0;
  out |= mode;
  out |= (ins << 1);
  printf("mode is %u, ins is %u, out is %u", mode, ins, out);

}

