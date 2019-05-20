#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

static int
_random(int min, int max) {
  return min + rand() % (max - min + 1);
}

int
main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Expected 1 argument, received: %i\n", argc);
    return -1;
  }

  // Let's ignore argv[1] anyway.

  srand(time(NULL));
  
  int seconds = _random(1, 60);

  printf("The fortune-telling will take %i seconds\n", seconds);

  sleep(seconds);

  return seconds % 2;
}
