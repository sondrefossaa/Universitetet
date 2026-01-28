
#include <stdio.h>
#include <string.h>
int main(void) {
  // Title print
  printf("Gnomes:\n");
  char buffer[256];
  fgets(buffer, 256, stdin);
  while (fgets(buffer, 256, stdin) != NULL) {
    int a, b, c;
    sscanf(buffer, "%d %d %d", &a, &b, &c);
    if ((a <= b && b <= c) || (a >= b && b >= c)) {
      printf("Ordered\n");
    } else {
      printf("Unordered\n");
    }
  }
  return 0;
}
