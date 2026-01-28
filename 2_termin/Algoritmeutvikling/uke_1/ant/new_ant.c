/*
 * currently failing on test 10 on kattis
 */
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct tunnel {
  int connect_to;
  struct tunnel *next;
} tunnel;

int max_chambers = 0;
int buisiest_level = 0;
int chambers;
int head = 0;
int tail = 0;
void print_layers(int *layers) {
  for (int i = 0; i < chambers; i++) {
    printf("%d, ", layers[i]);
  }
  printf("\n");
}
int find_biggest_layer(int *layer_count) {
  int biggest = layer_count[0];
  int biggest_layer = 0;

  for (int i = 1; i < chambers; i++) {
    if (layer_count[i] > biggest) {
      biggest = layer_count[i];
      biggest_layer = i;
    }
  }
  return biggest_layer;
}
void shift_queue(int *queue) {
  for (int i = head; i < tail; i++) {
    queue[i - head] = queue[i];
  }
  tail -= head;
  head = 0;
}

void insert_into_map(tunnel **hashmap, int index, int value) {
  tunnel *new_node = malloc(sizeof(tunnel));
  if (new_node == NULL) {
    printf("Failed\n");
    return;
  }
  new_node->connect_to = value;
  new_node->next = hashmap[index];
  hashmap[index] = new_node;
}
void print_hashmap(tunnel **hashmap) {
  for (int i = 0; i < chambers; i++) {
    tunnel *head = hashmap[i];
    while (head != NULL) {
      printf("%d is connected to %d\n", i, head->connect_to);
      head = head->next;
    }
  }
}
void free_hashmap(tunnel **hashmap) {
  for (int i = 0; i < chambers; i++) {
    tunnel *head = hashmap[i];
    while (head != NULL) {
      tunnel *temp = head;
      head = head->next;
      free(temp);
    }
  }
}
int main(void) {
  scanf("%d", &chambers);
  int queue_size = chambers;

  int *queue = malloc(queue_size * sizeof(int));
  int seen[chambers];
  int temp_queue[chambers];
  int layers[chambers];
  // memset(queue, 0, chambers * sizeof(int));
  memset(layers, 0, sizeof(int) * chambers);
  memset(seen, 0, chambers * sizeof(int));
  tunnel *hashmap[chambers + 1];
  for (int i = 0; i < chambers; i++) {
    hashmap[i] = NULL;
  }
  int to = 0;
  int from = 0;
  for (int i = 0; i < chambers - 1; i++) {
    scanf("%d %d", &to, &from);
    insert_into_map(hashmap, to, from);
    insert_into_map(hashmap, from, to);
    // printf("%d\n", i);
  }
  // print_hashmap(hashmap);
  int layer_count[chambers];
  memset(layer_count, 0, sizeof(int) * chambers);

  // Start from queen room
  queue[tail++] = 0;
  // Change bfs
  layer_count[0] = 1;
  seen[0] = true;
  while (head < tail) {
    int added = 0;
    // Expand first node
    int current = queue[head];
    // printf("Current is %d\n", current);
    head++;
    // Get nodes that connect to current node
    tunnel *curr = hashmap[current];
    while (curr != NULL) {
      int connection = curr->connect_to;
      if (seen[connection] == false) {
        // printf("Added %d\n", added);
        seen[connection] = true;
        queue[tail++] = connection;

        // New node is on next layer
        layers[curr->connect_to] = layers[current] + 1;
        layer_count[layers[current] + 1]++;
        // seen[curr->connect_to] = 1;
        if (tail >= queue_size) {
          shift_queue(queue);
        }
      }
      curr = curr->next;
    }
  }
  free_hashmap(hashmap);
  printf("%d\n", find_biggest_layer(layer_count));
}
