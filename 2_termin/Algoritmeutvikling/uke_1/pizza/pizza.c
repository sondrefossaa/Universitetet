// Small pizza has 6, medium has 8 and large has 12
// Cant pu a slice in a box it didnt come from

#include <stdio.h>
#define BUFFER_SIZE 256
long long ceil_division(long long a, long long b) { return (a + b - 1) / b; }
int main(void) {
  long boxes;
  char buffer[BUFFER_SIZE];
  fgets(buffer, BUFFER_SIZE, stdin);
  sscanf(buffer, "%ld", &boxes);
  long long temp_piz_count;
  char boxtype;
  long long Lpiz = 0.0L, Mpiz = 0.0L, Spiz = 0.0L;
  for (int i = 0; i < boxes; i++) {
    fgets(buffer, BUFFER_SIZE, stdin);
    sscanf(buffer, "%c %lld", &boxtype, &temp_piz_count);
    // printf("%Lf\n", temp_piz_count);
    switch (boxtype) {
    case 'L': {
      Lpiz += temp_piz_count;
      break;
    }
    case 'M': {
      Mpiz += temp_piz_count;
      break;
    }
    case 'S': {
      Spiz += temp_piz_count;
      break;
    }
    }
  }

  long long sum = 0;

  if (Spiz != 0) {
    sum += ceil_division(Spiz, 6);
  }
  if (Mpiz != 0) {
    sum += ceil_division(Mpiz, 8);
  }
  if (Lpiz != 0) {
    sum += ceil_division(Lpiz, 12);
  }
  printf("%lld\n", sum);

  return 0;
}
