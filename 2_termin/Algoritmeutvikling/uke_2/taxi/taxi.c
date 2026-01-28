#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int row, col;
} Point;

int main(void) {
    int rows, cols;
    scanf("%d %d", &rows, &cols);

    char **grid = (char**)malloc(rows * sizeof(char*));
    for (int i = 0; i < rows; i++) {
        // + 1 for '\0'
        grid[i] = (char*)malloc((cols + 1) * sizeof(char));
        scanf("%s", grid[i]);
    }

    Point *queue = (Point*)malloc(rows * cols * sizeof(Point));
    int front = 0, rear = 0;

    char *visited = (char*)malloc(rows * cols * sizeof(char));
    memset(visited, 0, rows * cols * sizeof(char));

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (grid[i][j] == 'S') {
                queue[rear].row = i;
                queue[rear].col = j;
                rear++;
                visited[i * cols + j] = 1;
            }
        }
    }

    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    int pickup_count = 0;

    while (front < rear) {
        int r = queue[front].row;
        int c = queue[front].col;
        front++;

        if (grid[r][c] == 'P') {
            pickup_count++;
        }

        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                char cell = grid[nr][nc];
                if (cell == '.' || cell == 'S' || cell == 'C' || cell == 'P') {
                    int idx = nr * cols + nc;
                    if (!visited[idx]) {
                        visited[idx] = 1;
                        queue[rear].row = nr;
                        queue[rear].col = nc;
                        rear++;
                    }
                }
            }
        }
    }

    printf("%d\n", pickup_count);

    for (int i = 0; i < rows; i++) {
        free(grid[i]);
    }
    free(grid);
    free(queue);
    free(visited);

    return 0;
}
