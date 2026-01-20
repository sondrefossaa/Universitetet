#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BUFFER_SIZE 512
int max_chambers = 0;
int buisiest_layer = 0;
int chambers;

typedef struct arrayList {
  int *connects_to;
  int size;
} arrayList;

void insert_into_map(arrayList *map, int to, int from) {
  map[from].connects_to[map[from].size] = to;
  map[from].size++;
}
int main(void) {
  // Populate start nodes
  scanf("%d", &chambers);
  // printf("Chambers is %d\n", chambers);
  int *queue = calloc(chambers, sizeof(int));
  int *seen = calloc(chambers, sizeof(int));
  arrayList connections[chambers];
  int edge_counts[chambers];
  for (int i = 0; i < chambers; i++) {
    edge_counts[i] = 0;
  }
  int to, from;
  for (int i = 0; i < chambers - 1; i++) {
    scanf("%d %d", &to, &from);
    edge_counts[to]++;
    edge_counts[from]++;
  }

  for (int i = 0; i < chambers; i++) {
    connections[i].connects_to = malloc(sizeof(int) * edge_counts[i]);
    connections[i].size = 0;
  }

  rewind(stdin);
  scanf("%d", &chambers);
  for (int i = 0; i < chambers - 1; i++) {
    scanf("%d %d", &to, &from);
    insert_into_map(connections, to, from);
    insert_into_map(connections, from, to);
  }
  // print_hashmap(hashmap);
  int level = 0;
  queue[0] = 0;
  int added = 1;
  int *temp_queue = calloc(chambers, sizeof(int));
  // seen[0] = 1;
  // Change bfs abit
  for (int i = 0; i < chambers; i++) {
    if (added > max_chambers) {
      max_chambers = added;
      buisiest_layer = i;
    }
    int prev_size = added;
    added = 0;
    // For each entry in queue, check the hashmap for champers connecting to it
    for (int j = 0; j < prev_size; j++) {
      if (seen[queue[j]] == 1)
        continue;
      arrayList *current = &connections[queue[j]];
      int size = current->size;
      int *connects = current->connects_to;
      seen[queue[j]] = 1;

      for (int a = 0; a < size; a++) {
        int connection = connects[a];
        if (seen[connection] == 0) {
          temp_queue[added] = connection;
          added++;
        }
      }
    }
    memcpy(queue, temp_queue, added * sizeof(int));
    memset(temp_queue, 0, added * sizeof(int));

    if (added == 0) {
      break;
    }
  }

  printf("%d\n", buisiest_layer);
  free(queue);
  free(temp_queue);
  free(seen);
}
