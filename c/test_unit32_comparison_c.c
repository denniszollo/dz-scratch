#include <stdio.h>

int main() {

unsigned int test;

test = 0;

unsigned short test_bool;

test_bool = test > 0;

if (test_bool) {
printf("with test as %u test_bool is true", test);
}

test = 1;
test_bool = test > 0;

if (test_bool) {
printf("with test as %u test_bool is true", test);
}

test = 0x0010 << 16 | 0x1;
printf("%u\n", test);
test_bool = test > 0;

if (test_bool) {
printf("with test as %u test_bool is true", test);
}
return 0;
}

