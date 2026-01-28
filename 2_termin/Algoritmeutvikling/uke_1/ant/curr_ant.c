#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BUFFER_SIZE 512
int max_chambers = 0;
int buisiest_layer = 0;
int chambers;

typedef struct tunnel {
  int connect_to;
  struct tunnel *next;
} tunnel;

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
  // Populate start nodes
  scanf("%d", &chambers);
  // printf("Chambers is %d\n", chambers);
  int queue[chambers];
  int seen[chambers];
  int temp_queue[chambers];
  // memset(queue, 0, chambers * sizeof(int));
  memset(seen, 0, chambers * sizeof(int));
  tunnel *hashmap[chambers];
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
  int level = 0;
  queue[0] = 0;
  int added = 1;
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
      tunnel *curr = hashmap[queue[j]];
      if (seen[queue[j]] == 1)
        continue;
      seen[queue[j]] = 1;
      while (curr != NULL) {
        if (seen[curr->connect_to] == 0) {
          // printf("Added %d\n", added);
          temp_queue[added] = curr->connect_to;
          added++;
          // printf("A %d\n", added);
        }
        curr = curr->next;
      }
    }
    // Change so dont have to do this
    memcpy(queue, temp_queue, added * sizeof(int));
    // memset(temp_queue, 0, added * sizeof(int));

    if (added == 0 || max_chambers == chambers) {
      break;
    }
  }

  printf("%d\n", buisiest_layer);
  free_hashmap(hashmap);
}
