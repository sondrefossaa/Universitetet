#include <stdio.h>
#include <stdlib.h>
#define BUFFER_SIZE 512

char ansString[BUFFER_SIZE];

int main(void) {
  int length;
  char buffer[BUFFER_SIZE];
  char *endpointer;
  fgets(buffer, BUFFER_SIZE, stdin);
  sscanf(buffer, "%d", &length);
  long long *array = malloc(sizeof(long long) * length);
  // printf("len: %d\n", length);
  for (int i = 0; i < length; i++) {
    fgets(buffer, BUFFER_SIZE, stdin);
    array[i] = strtoll(buffer, &endpointer, 2);
    // printf("Inserted %lld into array \n", array[i]);
  }
  for (int i = 0; i < length; i++) {
    long long temp = 1 << i;
    if ((array[i] && temp) == 0) {
      ansString[i] = '1';
    } else {
      ansString[i] = '0';
    }
  }
  // printf("ans: %lld\n", numAns);
  // printf("%s\n", convertNumToBinString(numAns));
  printf("%s\n", ansString);

  free(array);
  return 0;
}
