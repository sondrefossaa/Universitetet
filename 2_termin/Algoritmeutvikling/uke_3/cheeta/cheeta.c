#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>

typedef struct {
    int start_time;
    int vel;
    double distance;
    double time;
} Cheetah;

double cheetah_pos_at_time(Cheetah *cheetah, double time) {
    double elapsed = time - cheetah->start_time;
    if (elapsed < 0) elapsed = 0;
    cheetah->distance = cheetah->vel * elapsed;
    return cheetah->distance;
}

double max_double(double a, double b) {
    return (a > b) ? a : b;
}

double min_double(double a, double b) {
    return (a < b) ? a : b;
}

int main() {
    int n;
    scanf("%d", &n);

    Cheetah *cheetahs = (Cheetah *)malloc(n * sizeof(Cheetah));

    int max_start_time = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d %d", &cheetahs[i].start_time, &cheetahs[i].vel);
        cheetahs[i].distance = 0;
        cheetahs[i].time = 0;
        if (cheetahs[i].start_time > max_start_time) {
            max_start_time = cheetahs[i].start_time;
        }
    }

    double time = (double)max_start_time;
    double epsilon = pow(10, -2);
    double min_distance = DBL_MAX;
    double prevmax = 0;

    while (1) {
        double max_pos = -DBL_MAX;
        double min_pos = DBL_MAX;

        for (int i = 0; i < n; i++) {
            double pos = cheetah_pos_at_time(&cheetahs[i], time);
            max_pos = max_double(max_pos, pos);
            min_pos = min_double(min_pos, pos);
        }

        time += epsilon;
        double cur_max_distance = fabs(max_pos - min_pos);
        min_distance = min_double(min_distance, cur_max_distance);

        if (min_distance <= epsilon || min_distance == prevmax) {
            break;
        }
        prevmax = min_distance;
    }

    printf("%.3f\n", min_distance);

    free(cheetahs);
    return 0;
}
