// Redo all with adjacency map
#include <stdlib.h>

#include <stdio.h>
// that layer. Start at level 0 and use bfs to get the layer, use buzzle input
// to get nodes in layer.
#define BUFFER_SIZE 512
int max_chambers = 0;
int buisiest_level = 0;
int chambers;
int head = 0;
int tail = 1;
void print_layers(int *layers) {
  for (int i = 0; i < chambers; i++) {
    printf("%d, ", layers[i]);
  }
  printf("\n");
}
int find_biggest_layer(int *layer_count) {
  int biggest = 0;
  int biggest_layer = 0;
  int curr = layer_count[0];
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
int main(void) {
  // Populate start nodes
  char buffer[BUFFER_SIZE];
  fgets(buffer, BUFFER_SIZE, stdin);

  sscanf(buffer, "%d", &chambers);
  // int queue_size = pow((double)chambers, 6);
  int queue_size = chambers;
  int *queue = calloc(queue_size, sizeof(int));
  int *layers = calloc(chambers, sizeof(int));
  int *layer_count = calloc(chambers + 1, sizeof(int));
  int *tunnels = malloc(sizeof(int) * chambers);
  int *visited = calloc(chambers, sizeof(int));
  // print_layers(layers);
  int index = 0;
  int value = 0;
  for (int i = 0; i < chambers - 1; i++) {
    fgets(buffer, BUFFER_SIZE, stdin);
    sscanf(buffer, "%d %d", &value, &index);
    tunnels[index] = value;
    // printf("%d %d\n", index, tunnels[index]);
  }
  int level = 0;

  // Start from queen room
  queue[0] = 0;
  // Mega scuffed
  while (head < tail) {
    int added = 0;
    // Expand first node
    int current = queue[head];
    head++;
    if (visited[current] != 0) {
      continue;
    }
    visited[current] = 1;
    // GOTO next node
    if (tail >= queue_size) {
      shift_queue(queue);
    }

    if (layers[current] == 0) {
      level++;
    }
    // Fix so doesnt add many 0
    // Chambers start at 0
    for (int i = 1; i < chambers; i++) {
      if (tunnels[i] == current) {
        queue[tail] = i;
        // Add the children of this node to the next layer
        layers[i] = layers[current] + 1;
        layer_count[layers[current] + 1]++;
        // printf("Added %d to queue \n", i);
        tail++;
      }
    }

    // printf("Level of current node is %d\n", layers[current]);
    //
    // printf("Level is %d\n", level);
    // printf("Current node is chamber: %d\n", current);
    // printf("Added %d nodes to tree\n", added);
    // printf("Head is %d and tail is %d\n", head, tail);
    // Need to change this logic somehow?

    // level++;
    // print_layers(layers);
    // print_layers(layer_count);
  }
  // printf("Buisiest level is %d with %d chambers\n", buisiest_level,
  //        max_chambers);
  printf("%d\n", find_biggest_layer(layer_count));
  free(layers);
  free(queue);
  free(layer_count);
  free(tunnels);
}
