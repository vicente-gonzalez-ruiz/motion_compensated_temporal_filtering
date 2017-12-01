#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include "args.h"

/*
#define CHUNK_SIZE 3
#define OFFSET 0
#define N_BYTES 1
*/
#define BUF_SIZE 4096

int main(int argc, char *argv[]) {
  if(argc<=1) {
    print_parameters();
  } else {
    work(argc,argv);
  }
  return EXIT_SUCCESS;
}

print_parameters() {
  fprintf(stderr,"demux chunk_size offset number_of_bytes < input > output\n");
  /*fprintf(stderr,"Demultiplex a data sequence\n");
  fprintf(stderr," < multi-component input data seq. > single-component output data seq.\n");
  fprintf(stderr," [-chunk_size <multi-component chunk size in bytes>] (default %d)\n",CHUNK_SIZE);
  fprintf(stderr," [-offset <offset of the data in the chunk> (default %d)\n",OFFSET);
  fprintf(stderr," [-n_bytes <number of bytes to extract per chunk>] (default %d)\n",N_BYTES);*/
}

work(int argc, char *argv[]) {
  int chunk_size = atoi(argv[1]);
  int offset = atoi(argv[2]);
  int n_bytes = atoi(argv[3]);
  FILE *fd_i = stdin;
  FILE *fd_o = stdout;
  char *buffer;
  
  /*if(ARGS__EXIST("-chunk_size")) {
    chunk_size = atoi(ARGS__GET("-chunk_size"));
    }*/
#if defined DEBUG
  fprintf(stderr,"demux: chunk size = %d\n", chunk_size);
#endif

  /*if(ARGS__EXIST("-offset")) {
    offset = atoi(ARGS__GET("-offset"));
    }*/
#if defined DEBUG
  fprintf(stderr,"demux: internal chunk offset = %d\n", offset);
#endif

  /*if(ARGS__EXIST("-n_bytes")) {
    n_bytes = atoi(ARGS__GET("-n_bytes"));
    }*/
# if defined DEBUG
  fprintf(stderr,"demux: number of extracted bytes/chunk = %d\n", n_bytes);
#endif  

  buffer = (char *)malloc(chunk_size);
  if(!buffer) {
    perror("malloc");
    fprintf(stderr,"demux: unable to allocate %d bytes of memory\n",chunk_size);
    exit(EXIT_FAILURE);
  }

  for(;;) {
    int r = fread(buffer, sizeof(char), chunk_size, fd_i);
    if(r==0) break;
    fwrite(buffer+offset, sizeof(char), n_bytes, fd_o);
  }
  return 0;
}
