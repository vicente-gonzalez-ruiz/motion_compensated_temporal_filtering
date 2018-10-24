/* Log-search bidirectional block-based motion estimation */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
//#include <netpbm/pgm.h>
#include <sys/stat.h>
#include <sys/types.h>

//#define __INFO__
//#define __DEBUG__
//#define __WARNING__

#include "display.cpp"
#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include "common.h"

#define MOTION_INTERPOLATION_FILTER Haar

#include <getopt.h>

int main(int argc, char *argv[]) {

#if defined __INFO__
  info("%s ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif

  int block_size = 32;
  char *imotion_fn = (char *)"/dev/zero";
  char *motion_fn = (char *)"motion";
  int pictures = 9;
  int pixels_in_x = 352;
  int pixels_in_y = 288;
  
  int c;
  while(1) {
    
    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"block_size", required_argument, 0, 'b'},
      {"imotion_fn", required_argument, 0, 'i'},
      {"motion_fn", required_argument, 0, 'm'},
      {"pictures", required_argument, 0, 'p'},
      {"pixels_in_x", required_argument, 0, 'x'},
      {"pixels_in_y", required_argument, 0, 'y'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };
    
    int option_index = 0;
    
    c = getopt_long(argc, argv, "b:i:m:p:x:y:?", long_options, &option_index);
    
    if(c==-1) {
      /* There are no more options. */
      break;
    }
    
    switch (c) {
    case 0:
      /* If this option set a flag, do nothing else now. */
      if (long_options[option_index].flag != 0)
	break;
      info("option %s", long_options[option_index].name);
      if (optarg)
	info(" with arg %s", optarg);
      info("\n");
      break;

    case 'b':
      block_size = atoi(optarg);
      info("%s: block_size=%d\n", argv[0], block_size);
      break;
      
    case 'i':
      imotion_fn = optarg;
      info("%s: imotion_fn=\"%s\"\n", argv[0], imotion_fn);
      break;

    case 'm':
      motion_fn = optarg;
      info("%s: motion_fn=\"%s\"\n", argv[0], motion_fn);
      break;

    case 'p':
      pictures = atoi(optarg);
      info("%s: pictures=%d\n", argv[0], pictures);
      break;
      
    case 'x':
      pixels_in_x = atoi(optarg);
     info("%s: pixels_in_x=%d\n", argv[0], pixels_in_x);
      break;
      
    case 'y':
      pixels_in_y = atoi(optarg);
      info("%s: pixels_in_y=%d\n", argv[0], pixels_in_y);
      break;
      
    case '?':
      printf("+---------------------+\n");
      printf("| MCTF zoomin_imotion |\n");
      printf("+---------------------+\n");
      printf("\n");
      printf("   Block-based time-domain motion estimation.\n");
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-i]motion_fn = input file with the initial motion fields (\"%s\")\n", imotion_fn);
      printf("   -[-m]otion_fn = output file with the motion fields (\"%s\")\n", imotion_fn);
      printf("   -[-p]ictures = number of pictures to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y);
      printf("\n");
      exit(1);
      break;
      
    default:
      error("%s: Unrecognized argument\n", argv[0]);
      abort();
    }
  }

  {
    int err = mkdir(motion_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], motion_fn);
      abort();
    }
#endif /* __DEBUG__ */
  }
  
  int blocks_in_y = pixels_in_y/block_size;
  int blocks_in_x = pixels_in_x/block_size;
  info("%s: blocks_in_y=%d\n", argv[0], blocks_in_y);
  info("%s: blocks_in_x=%d\n", argv[0], blocks_in_x);
  motion < MVC_TYPE > motion;
  MVC_TYPE ****mv = motion.alloc(blocks_in_y, blocks_in_x);

  class dwt2d < 
  MVC_TYPE, MOTION_INTERPOLATION_FILTER <
  MVC_TYPE > > *motion_dwt
    = new class dwt2d <
  MVC_TYPE, MOTION_INTERPOLATION_FILTER <
  MVC_TYPE > >;

  motion_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  for(int i=0; i<pictures/2; i++) {

    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	mv[PREV][Y_FIELD][by][bx] = 0;
	mv[PREV][X_FIELD][by][bx] = 0;
	mv[NEXT][Y_FIELD][by][bx] = 0;
	mv[NEXT][X_FIELD][by][bx] = 0;
      }
    }

    info("%s: reading initial motion vectors\n", argv[0]);

    motion.read_field(mv, blocks_in_y/2, blocks_in_x/2, imotion_fn, i
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
		      , argv[0]
#endif /* __INFO__ */
		      );

#if defined (__DEBUG__)
    printf("%s content:\n", imotion_fn);
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	printf("%d,%d %d,%d - ",
	       mv[PREV][Y_FIELD][by][bx],
	       mv[PREV][X_FIELD][by][bx],
	       mv[NEXT][Y_FIELD][by][bx],
	       mv[NEXT][X_FIELD][by][bx]);
      }
      printf("\n");
    }
#endif

    motion_dwt -> synthesize(mv[PREV][Y_FIELD], blocks_in_y, blocks_in_x, 1);
    motion_dwt -> synthesize(mv[NEXT][Y_FIELD], blocks_in_y, blocks_in_x, 1);
    motion_dwt -> synthesize(mv[PREV][X_FIELD], blocks_in_y, blocks_in_x, 1);
    motion_dwt -> synthesize(mv[NEXT][X_FIELD], blocks_in_y, blocks_in_x, 1);

#ifdef _1_
#if defined __INFO__
    info("Backward motion vector field:");
    for(int y=0; y<blocks_in_y; y++) {
      info("\n");
      for(int x=0; x<blocks_in_x; x++) {
	static char aux[80];
	sprintf(aux,"%3d,%3d",
	     mv[PREV][Y_FIELD][y][x],
	     mv[PREV][X_FIELD][y][x]);
	info("%8s",aux);
      }
    }
    info("\n");

    info("Forward motion vector field:");
    for(int y=0; y<blocks_in_y; y++) {
      info("\n");
      for(int x=0; x<blocks_in_x; x++) {
	static char aux[80];
	sprintf(aux,"%3d,%3d",
	     mv[NEXT][Y_FIELD][y][x],
	     mv[NEXT][X_FIELD][y][x]);
	info("%8s",aux);
      }
    }
    info("\n");
#endif /* __INFO__ */
#endif
    info("%s: writing motion vector field %d in \"%s\"\n", argv[0], i, motion_fn);
    
#if defined (__DEBUG__)
    printf("%s content:\n", motion_fn);
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	printf("%d,%d %d,%d - ",
	       mv[PREV][Y_FIELD][by][bx],
	       mv[PREV][X_FIELD][by][bx],
	       mv[NEXT][Y_FIELD][by][bx],
	       mv[NEXT][X_FIELD][by][bx]);
      }
      printf("\n");
    }
#endif
    motion.write_field(mv, blocks_in_y, blocks_in_x, motion_fn, i
#if defined (__INFO__)  || defined (__DEBUG__) || defined (__WARNING__)
		       , argv[0]
#endif /* __INFO__ */
		       );
  }
#ifdef _1_
  delete motion_dwt;
#endif
  motion.free(mv, blocks_in_y);
}
