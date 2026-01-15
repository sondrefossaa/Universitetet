#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BUFFER_SIZE 512
int main(void) {
  char buffer[BUFFER_SIZE];
  fgets(buffer, BUFFER_SIZE, stdin);
  int i, j, lucky;
  // Read row and col size
  sscanf(buffer, "%d %d", &i, &j);
  fgets(buffer, BUFFER_SIZE, stdin);
  // Read lucky number
  sscanf(buffer, "%d", &lucky);
  // printf("%d, %d, %d\n", i, j, lucky);

  int **array = (int **)malloc(sizeof(int *) * i);
  for (int a = 0; a < i; a++) {
    char line[BUFFER_SIZE];
    fgets(line, BUFFER_SIZE, stdin);
    array[a] = (int *)malloc(sizeof(int) * j);
    char *token = strtok(line, " \n");
    int b = 0;
    while (token != NULL) {
      array[a][b] = atoi(token);
      token = strtok(NULL, " \n");
      b++;
    }
  }

  int ans = 0;
  for (int a = 1; a < i - 1; a++) {
    for (int b = 1; b < j - 1; b++) {
      if (array[a][b] == lucky) {
        if ((array[a - 1][b - 1] + array[a - 1][b + 1] + array[a + 1][b + 1] +
             array[a + 1][b - 1]) %
                lucky ==
            0) {
          ans++;
        }
      }
    }
  }
  printf("%d\n", ans);
  // Free memory
  for (int a = 0; a < i; a++) {
    free(array[a]);
  }
  return 0;
}
