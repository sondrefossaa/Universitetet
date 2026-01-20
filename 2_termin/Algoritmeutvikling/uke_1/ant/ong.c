#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct {
  int *connects_to;
  int count;
} chamber;

int main(void) {
  int chambers;
  scanf("%d", &chambers);
  int *degree = calloc(chambers, sizeof(int));
  int (*edges)[2] = malloc(sizeof(int[2]) * (chambers - 1));

  for (int i = 0; i < chambers - 1; i++) {
    // Scan all edges
    scanf("%d %d", &edges[i][0], &edges[i][1]);
    // Count adjacency for all chambers
    degree[edges[i][0]]++;
    degree[edges[i][1]]++;
  }
  int **graph = malloc(chambers * sizeof(int *));
  int *count = malloc(sizeof(int) * chambers);
  for (int i = 0; i < chambers; i++) {
    graph[i] = malloc(degree[i] * sizeof(int));
    count[i] = 0;
  }

  for (int i = 0; i < chambers - 1; i++) {
    int from = edges[i][0];
    int to = edges[i][1];
    graph[to][count[to]++] = from;
    graph[from][count[from]++] = to;
  }

  int *queue = malloc(chambers * sizeof(int));
  char *visited = calloc(chambers, sizeof(char));
  int head = 0, tail = 0;

  queue[tail++] = 0;
  visited[0] = 1;

  int lvl_end = 1;
  int curr_lvl = 0;
  int max_lvl = 0;
  int max_count = 1;

  while (head < tail) {
    int node = queue[head++];

    for (int i = 0; i < count[node]; i++) {
      int neighbour = graph[node][i];
      if (!visited[neighbour]) {
        visited[neighbour] = 1;
        queue[tail++] = neighbour;
      }
    }
    if (head == lvl_end) {
      int next_lvl_size = tail - lvl_end;
      if (next_lvl_size > max_count) {
        max_count = next_lvl_size;
        max_lvl = curr_lvl + 1;
      }
      lvl_end = tail;
      curr_lvl++;
    }
  }
  printf("%d\n", max_lvl);
  for (int i = 0; i < chambers; i++)
    free(graph[i]);
  free(graph);
  free(count);
  free(degree);
  free(edges);
  free(queue);
  free(visited);
}
