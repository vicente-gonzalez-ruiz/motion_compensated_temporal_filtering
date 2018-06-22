/* Log-search bidirectional block-based motion estimation */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
//#include <netpbm/pgm.h>
#include <sys/stat.h>
#include <sys/types.h>

#define __INFO__
#define __DEBUG__
#define __WARNING__

#include "display.cpp"
#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include "common.h"

#define FAST_SEARCH
#define TEXTURE_INTERPOLATION_FILTER _5_3
#define MOTION_INTERPOLATION_FILTER Haar

#if defined FAST_SEARCH

void local_me_for_block
(
 MVC_TYPE ****mv,    /* [PREV|NEXT][Y|X][coor_y][coor_x] */
 TC_CPU_TYPE ***ref, /* [PREV|NEXT][coor_y][coor_x] */
 TC_CPU_TYPE **pred, /* [coor_y][coor_x] */
 int luby, int lubx, /* Coordinate upper-left block. */
 int rbby, int rbbx, /* Coordinate lower-right block. */
 int by, int bx      /* Vector coordinate in the field of movement. */
 ) {

  int min_error[2];
  int vy[2], vx[2];

  MVC_TYPE mv_prev_y_by_bx = mv[PREV][Y_FIELD][by][bx];
  MVC_TYPE mv_prev_x_by_bx = mv[PREV][X_FIELD][by][bx];
  MVC_TYPE mv_next_y_by_bx = mv[NEXT][Y_FIELD][by][bx];
  MVC_TYPE mv_next_x_by_bx = mv[NEXT][X_FIELD][by][bx];

#define COMPUTE_ERRORS(_y,_x)						\
  MVC_TYPE y[2] = {(MVC_TYPE)(mv_prev_y_by_bx + _y), (MVC_TYPE)(mv_next_y_by_bx - _y)}; \
  MVC_TYPE x[2] = {(MVC_TYPE)(mv_prev_x_by_bx + _x), (MVC_TYPE)(mv_next_x_by_bx - _x)}; \
  int error[2] = {0, 0};						\
  									\
  for(int py=luby; py<rbby; py++) {					\
    TC_CPU_TYPE *pred_py = pred[py];					\
    for(int px=lubx; px<rbbx; px++) {					\
      error[PREV] += abs						\
	(pred_py[px] - ref[PREV][py + y[PREV]][px + x[PREV]]);		\
      error[NEXT] += abs						\
	(pred_py[px] - ref[NEXT][py + y[NEXT]][px + x[NEXT]]);		\
    }									\
  }

#define UPDATE_VECTORS							\
  if(error[PREV] <= min_error[PREV]) {					\
    vy[PREV] = y[PREV];							\
    vx[PREV] = x[PREV];							\
    min_error[PREV] = error[PREV];					\
  }									\
									\
  if(error[NEXT] <= min_error[NEXT]) {					\
    vy[NEXT] = y[NEXT];							\
    vx[NEXT] = x[NEXT];							\
    min_error[NEXT] = error[NEXT];					\
  }

  /* 1. Position (-1,-1). Up - Left. */ {
    COMPUTE_ERRORS(-1,-1);
    
    min_error[PREV] = error[PREV];
    vy[PREV] = y[PREV];
    vx[PREV] = x[PREV];

    min_error[NEXT] = error[NEXT];
    vy[NEXT] = y[NEXT];
    vx[NEXT] = x[NEXT];
  }
  
  /* 2. Position (-1,1). Up - Right. */ {
    COMPUTE_ERRORS(-1,1);
    UPDATE_VECTORS;
  }
  
  /* 3. Position (1,-1). Down - left. */ {
    COMPUTE_ERRORS(1,-1);
    UPDATE_VECTORS;
  }
  
  /* 4. Position (1,1). Down - Right. */ {
    COMPUTE_ERRORS(1,1);
    UPDATE_VECTORS;
  }
  
  /* 5. Position (-1,0). Up. */ {
    COMPUTE_ERRORS(-1,0);
    UPDATE_VECTORS;
  }
  
  /* 6. Position (1,0). Down. */ {
    COMPUTE_ERRORS(1,0);
    UPDATE_VECTORS;
  }
  
  /* 7. Position (0,1). Right. */ {
    COMPUTE_ERRORS(0,1);
    UPDATE_VECTORS;
  }
  
  /* 8. Position (0,-1). Left. */ {
    COMPUTE_ERRORS(0,-1);
    UPDATE_VECTORS;
  }
  
  /* 9. Position (0,0). */ {
    COMPUTE_ERRORS(0,0);
    UPDATE_VECTORS;
  }
  
#undef COMPUTE_ERRORS
#undef UPDATE_VECTORS
  
  mv[PREV][Y_FIELD][by][bx] = vy[PREV];
  mv[PREV][X_FIELD][by][bx] = vx[PREV];
  mv[NEXT][Y_FIELD][by][bx] = vy[NEXT];
  mv[NEXT][X_FIELD][by][bx] = vx[NEXT];

} /* local_me_for_block() */

/* Estimates the motion of a block from the reference picture to the
 * predicted picture, use a search area of +-1. */
void local_me_for_picture
(
 MVC_TYPE ****mv,             /* [PREV|NEXT][Y|X][coor_y][coor_x] */
 TC_CPU_TYPE ***ref,          /* [PREV|NEXT][coor_y][coor_x] */
 TC_CPU_TYPE **pred,          /* [coor_y][coor_x] */
 int block_size,
 int border_size,
 int blocks_in_y,
 int blocks_in_x
) {
  for(int by=0; by<blocks_in_y; by++) {
    info("%d/%d ", by, blocks_in_y); info_flush();
    for(int bx=0; bx<blocks_in_x; bx++) {
      /* Region occupied by the block (including the border). */
      int luby = (by  ) * block_size - border_size;
      int lubx = (bx  ) * block_size - border_size;
      int rbby = (by+1) * block_size + border_size;
      int rbbx = (bx+1) * block_size + border_size;
      local_me_for_block(mv, ref, pred, luby, lubx, rbby, rbbx, by, bx);
    }
  }
  info("\n");
}

/* Number of blocks in each level DWT (Discrete Wavelet Transform).
 */
int desp(int x, int y) {
  int i;
  for(i=0; i<y; i++) x = (x+1)/2;
  return x;
}

# endif /* FAST_SEARCH */

void me_for_picture
(MVC_TYPE ****mv,               /* [PREV|NEXT][y_field|x_field][y_coor][x_coor] */
 TC_CPU_TYPE ***ref,            /* [PREV|NEXT][y_coor][x_coor] */
 TC_CPU_TYPE **pred,            /* [y_coor][x_coor] */
 int pixels_in_y,
 int pixels_in_x,
 int block_size,
 int border_size,
 int subpixel_accuracy,
 int search_range,
 int blocks_in_y,
 int blocks_in_x,
 class dwt2d < TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TC_CPU_TYPE > > *pic_dwt,
 class dwt2d < MVC_TYPE, MOTION_INTERPOLATION_FILTER < MVC_TYPE > > *mv_dwt) {

#if defined FAST_SEARCH
  
  int dwt_levels = (int)rint(log((double)search_range)/log(2.0)) - 1;
  info("motion_estimate: dwt_levels = %d\n", dwt_levels);

  /* DWT applied to pictures. */
  pic_dwt->analyze(ref[PREV], pixels_in_y, pixels_in_x, dwt_levels);
  pic_dwt->analyze(ref[NEXT], pixels_in_y, pixels_in_x, dwt_levels);
  pic_dwt->analyze(pred, pixels_in_y, pixels_in_x, dwt_levels);

  /* Over-pixel estimation. */
  info("motion_estimate: over-pixel motion estimation level=%d\n", dwt_levels);

  local_me_for_picture(mv,
		     ref,
		     pred,
		     block_size,
		     border_size,
		     desp(blocks_in_y, dwt_levels),
		     desp(blocks_in_x, dwt_levels));
    
  for(int l=dwt_levels-1; l>=0; --l) {
    int Y_l = desp(pixels_in_y, l);
    int X_l = desp(pixels_in_x, l);
    int blocks_in_y_l = desp(blocks_in_y, l);
    int blocks_in_x_l = desp(blocks_in_x, l);

    /* Expand pictures in a factor of 2. */
    pic_dwt->synthesize(ref[PREV], Y_l, X_l, 1);
    pic_dwt->synthesize(ref[NEXT], Y_l, X_l, 1);
    pic_dwt->synthesize(pred, Y_l, X_l, 1);

    /*  Motion fields expanded by a factor of 2. This is necessary
	because in the next iteration the reference and predicted
	pictures are twice as large. */
    mv_dwt->synthesize(mv[PREV][Y_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    mv_dwt->synthesize(mv[NEXT][Y_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    mv_dwt->synthesize(mv[PREV][X_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    mv_dwt->synthesize(mv[NEXT][X_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    
    /* Multiply by 2 the motion vectors, because the calculated values
       now referenced to an picture twice as large in each dimension. */
    for(int by=0; by<blocks_in_y_l; by++) {
      for(int bx=0; bx<blocks_in_x_l; bx++) {

	mv[PREV][Y_FIELD][by][bx] *= 2;
	if(mv[PREV][Y_FIELD][by][bx] > search_range)
	  mv[PREV][Y_FIELD][by][bx] = search_range;
	if(mv[PREV][Y_FIELD][by][bx] < -search_range)
	  mv[PREV][Y_FIELD][by][bx] = -search_range;

	mv[NEXT][Y_FIELD][by][bx] *= 2;
	if(mv[NEXT][Y_FIELD][by][bx] > search_range)
	  mv[NEXT][Y_FIELD][by][bx] =  search_range;
	if(mv[NEXT][Y_FIELD][by][bx] < -search_range)
	  mv[NEXT][Y_FIELD][by][bx] = -search_range;

	mv[PREV][X_FIELD][by][bx] *= 2;
	if(mv[PREV][X_FIELD][by][bx] > search_range)
	  mv[PREV][X_FIELD][by][bx] =  search_range;
	if(mv[PREV][X_FIELD][by][bx] < -search_range)
	  mv[PREV][X_FIELD][by][bx] = -search_range;

	mv[NEXT][X_FIELD][by][bx] *= 2;
	if(mv[NEXT][X_FIELD][by][bx] > search_range)
	  mv[NEXT][X_FIELD][by][bx] =  search_range;
	if(mv[NEXT][X_FIELD][by][bx] < -search_range)
	  mv[NEXT][X_FIELD][by][bx] = -search_range;
      }
    }
    info("motion_estimate: over-pixel motion estimation level=%d\n",l);
    local_me_for_picture(mv,
		       ref,
		       pred,
		       block_size,
		       border_size,
		       blocks_in_y_l, blocks_in_x_l);
  }
  
  /* Sub-pixel estimation. */
  for(int l=1; l<=subpixel_accuracy; l++) {
    info("motion_estimate: sub-pixel motion estimation level=%d\n",l);
    
    /* Expand pictures on a factor of 2. */
    pic_dwt->synthesize(ref[PREV], pixels_in_y<<l, pixels_in_x<<l, 1);
    pic_dwt->synthesize(ref[NEXT], pixels_in_y<<l, pixels_in_x<<l, 1);
    pic_dwt->synthesize(pred, pixels_in_y<<l, pixels_in_x<<l, 1);
    
    /* Motion fields expanded by a factor of 2. */
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {

	mv[PREV][Y_FIELD][by][bx] *= 2;
	if(mv[PREV][Y_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[PREV][Y_FIELD][by][bx] = search_range<<subpixel_accuracy;
	if(mv[PREV][Y_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[PREV][Y_FIELD][by][bx]= -(search_range<<subpixel_accuracy);

	mv[NEXT][Y_FIELD][by][bx] *= 2;
	if(mv[NEXT][Y_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[NEXT][Y_FIELD][by][bx] = search_range<<subpixel_accuracy;
	if(mv[NEXT][Y_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[NEXT][Y_FIELD][by][bx]= -(search_range<<subpixel_accuracy);

	mv[PREV][X_FIELD][by][bx] *= 2;
	if(mv[PREV][X_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[PREV][X_FIELD][by][bx] = (search_range<<subpixel_accuracy);
	if(mv[PREV][X_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[PREV][X_FIELD][by][bx]= -(search_range<<subpixel_accuracy);

	mv[NEXT][X_FIELD][by][bx] *= 2;
	if(mv[NEXT][X_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[NEXT][X_FIELD][by][bx] = (search_range<<subpixel_accuracy);
	if(mv[NEXT][X_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[NEXT][X_FIELD][by][bx]= -(search_range<<subpixel_accuracy);
      }
    }
    
    local_me_for_picture(mv,
		       ref,
		       pred,
		       block_size<<l,
		       border_size>>l,
		       blocks_in_y, blocks_in_x);
  }

  /* Interpolate. */
  pic_dwt->analyze(ref[PREV], pixels_in_y << subpixel_accuracy, pixels_in_x << subpixel_accuracy, subpixel_accuracy);
  pic_dwt->analyze(ref[NEXT], pixels_in_y << subpixel_accuracy, pixels_in_x << subpixel_accuracy, subpixel_accuracy);
  pic_dwt->analyze(pred, pixels_in_y << subpixel_accuracy, pixels_in_x << subpixel_accuracy, subpixel_accuracy);

  //pic_dwt->analyze(reference_pic, Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);
  //pic_dwt->analyze(predicted_pic, Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);

#else /* !defined FAST_SEARCH */

  pic_dwt->synthesize(ref[0], pixels_in_y<<subpixel_accuracy, pixels_in_x<<subpixel_accuracy, subpixel_accuracy);
  pic_dwt->synthesize(ref[1], pixels_in_y<<subpixel_accuracy, pixels_in_x<<subpixel_accuracy, subpixel_accuracy);
  pic_dwt->synthesize(pred, pixels_in_y<<subpixel_accuracy, pixels_in_x<<subpixel_accuracy, subpixel_accuracy);
  
  block_size <<= subpixel_accuracy;
  search_range <<= subpixel_accuracy;
  border_size <<= subpixel_accuracy;
  
  //int blocks_in_y = (Y<<subpixel_accuracy)/block_size;
  //int blocks_in_x = (X<<subpixel_accuracy)/block_size;
  
  for(int by=0; by<blocks_in_y; by++) {
    printf("%d/%d ",by, blocks_in_y); fflush(stderr);
    for(int bx=0; bx<blocks_in_x; bx++) {
      int min_error = 999999999;
      int vy, vx;
      
      /* For each point of the search area. */
      for(int ry=by*block_size-search_range; ry<=by*block_size+search_range; ry++) {
	for(int rx=bx*block_size-search_range; rx<=bx*block_size+search_range; rx++) {
	  /* For each point of the block to search. */
	  int error = 0;
	  for(int y=-border_size; y<block_size+border_size; y++) {
	    for(int x=-border_size; x<block_size+border_size; x++) {
	      error += abs(pred[by*block_size+y][bx*block_size+x] -
			   ref
			   [0]
			   [ry + mv[NEXT][Y_FIELD][by][bx] + y]
			   [rx + mv[NEXT][X_FIELD][by][bx] + x]);
	      error += abs(pred[by*block_size+y][bx*block_size+x] -
			   ref
			   [1]
			   [by*block_size*2 - ry + mv[PREV][Y_FIELD][by][bx] + y]
			   [bx*block_size*2 - rx + mv[PREV][X_FIELD][by][bx] + x]);
	    }
	  }
	  if(error < min_error) {
	    min_error = error;
	    vy = ry-by*block_size;
	    vx = rx-bx*block_size;
	  }
	  /*print("\n%d,%d  %d,%d %d %d",
	    ry + mv[NEXT][Y][by][bx],
	    rx + mv[NEXT][X][by][bx],
	    by*block_size*2 - ry + mv[PREV][Y][by][bx],
	    bx*block_size*2 - rx + mv[PREV][X][by][bx],
	    error, min_error
	    );*/
	}
      }
      
      mv[NEXT][Y_FIELD][by][bx] += vy;
      mv[NEXT][X_FIELD][by][bx] += vx;
      mv[PREV][Y_FIELD][by][bx] += -vy;
      mv[PREV][X_FIELD][by][bx] += -vx;
      
      //print("\nvector = %d,%d,%d,%d",mv[NEXT][Y][by][bx],mv[NEXT][X][by][bx],mv[PREV][Y][by][bx],mv[PREV][X][by][bx]);
    }
  }

#endif /* FAST_SEARCH */

} /* me_for_picture */

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
  int border_size = 0;
  char *even_fn = (char *)"E";
  char *imotion_fn = (char *)"imotion";
  char *motion_fn = (char *)"motion";
  char *odd_fn = (char *)"O";
  int pictures = 9;
  int pixels_in_x = 352;
  int pixels_in_y = 288;
  int search_range = 4;
  int subpixel_accuracy = 0;
  
  int c;
  while(1) {
    
    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"block_size", required_argument, 0, 'b'},
      {"border_size", required_argument, 0, 'd'},
      {"even_fn", required_argument, 0, 'e'},
      {"imotion_fn", required_argument, 0, 'i'},
      {"motion_fn", required_argument, 0, 'm'},
      {"odd_fn", required_argument, 0, 'o'},
      {"pictures", required_argument, 0, 'p'},
      {"pixels_in_x", required_argument, 0, 'x'},
      {"pixels_in_y", required_argument, 0, 'y'},
      {"search_range", required_argument, 0, 's'},
      {"subpixel_accuracy", required_argument, 0, 'a'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };

    int option_index = 0;
    
    c = getopt_long(argc, argv, "b:d:e:i:m:o:p:x:y:s:a:?", long_options, &option_index);

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
      
    case 'e':
      even_fn = optarg;
      info("%s: even_fn=\"%s\"\n", argv[0], even_fn);
      break;

    case 'i':
      imotion_fn = optarg;
      info("%s: imotion_fn=\"%s\"\n", argv[0], imotion_fn);
      break;

    case 'm':
      motion_fn = optarg;
      info("%s: motion_fn=\"%s\"\n", argv[0], motion_fn);
      break;

    case 'o':
      odd_fn = optarg;
      info("%s: odd_fn=\"%s\"\n", argv[0], odd_fn);
      break;

    case 'd':
      border_size = atoi(optarg);
      info("%s: border_size=%d\n", argv[0], border_size);
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
      
    case 's':
      search_range = atoi(optarg);
      info("%s: search_range=%d\n", argv[0], search_range);
      break;
      
    case 'a':
      subpixel_accuracy = atoi(optarg);
      info("%s: subpixel_accuracy=%d\n", argv[0], subpixel_accuracy);
      break;
      
    case '?':
      printf("+----------------------+\n");
      printf("| MCTF motion_estimate |\n");
      printf("+----------------------+\n");
      printf("\n");
      printf("   Block-based time-domain motion estimation.\n");
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-b]lock_size = size of the blocks in the motion estimation process (%d)\n", block_size);
      printf("   -[-]bor[d]der_size = size of the border of the blocks in the motion estimation process (%d)\n", border_size);
      printf("   -[-e]ven_fn = input file with the even pictures (\"%s\")\n", even_fn);
      printf("   -[-i]motion_fn = input file with the initial motion fields (\"%s\")\n", imotion_fn);
      printf("   -[-m]otion_fn = output file with the motion fields (\"%s\")\n", imotion_fn);
      printf("   -[-o]dd_fn = input file with odd pictures (\"%s\")\n", odd_fn);
      printf("   -[-p]ictures = number of pictures to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y);
      printf("   -[-s]earch_range = size of the searching area of the motion estimation (%d)\n", search_range);
      printf("   -[-]subpixel_[a]ccuracy = sub-pixel accuracy of the motion estimation (%d)\n", subpixel_accuracy);
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
 
  int picture_border_size = search_range + border_size;

  texture < TC_IO_TYPE, TC_CPU_TYPE > texture;

  TC_CPU_TYPE **reference[2];
  for(int i=0; i<2; i++) {
    reference[i] =
      texture.alloc(pixels_in_y << subpixel_accuracy,
		    pixels_in_x << subpixel_accuracy,
		    picture_border_size << subpixel_accuracy/*2*/);

    /* This initialization seems to be unnecessary. */
    for(int y=0; y<pixels_in_y << subpixel_accuracy; y++) {
      for(int x=0; x<pixels_in_x <<subpixel_accuracy; x++) {
	reference[i][y][x] = 0;
      }
    }
  }
  
  TC_CPU_TYPE **predicted =
    texture.alloc(pixels_in_y << subpixel_accuracy,
		  pixels_in_x << subpixel_accuracy,
		  picture_border_size << subpixel_accuracy/*2*/);

  /* This initialization seems to be unnecessary. */
  for(int y=0; y<pixels_in_y << subpixel_accuracy; y++) {
    for(int x=0; x<pixels_in_x <<subpixel_accuracy; x++) {
      predicted[y][x] = 0;
    }
  }

  int blocks_in_y = pixels_in_y/block_size;
  int blocks_in_x = pixels_in_x/block_size;
  info("%s: blocks_in_y=%d\n", argv[0], blocks_in_y);
  info("%s: blocks_in_x=%d\n", argv[0], blocks_in_x);

  motion < MVC_TYPE > motion;
  MVC_TYPE ****mv = motion.alloc(blocks_in_y, blocks_in_x);

  class dwt2d <
  TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER <
  TC_CPU_TYPE > > *texture_dwt
    = new class dwt2d <
  TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER <
  TC_CPU_TYPE > >;
  texture_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  class dwt2d < 
  MVC_TYPE, MOTION_INTERPOLATION_FILTER <
  MVC_TYPE > > *motion_dwt
    = new class dwt2d <
  MVC_TYPE, MOTION_INTERPOLATION_FILTER <
  MVC_TYPE > >;
  motion_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  /* Read the luma of reference[0]. */
  // {{{ reference[0] <- E
  texture.read_picture(reference[0],
		     pixels_in_y, pixels_in_x,
		     even_fn,
		     0,
		     LUMA
#if defined __INFO__
		     ,
		     argv[0]
#endif /* __INFO__ */
		     );
  // }}}

  /* Skip to the chroma. */
  /*fseek(E_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);
    fseek(E_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);*/

  /* Fill the edge of the read picture. */
  texture.fill_border(reference[0],
		      pixels_in_y,
		      pixels_in_x,
		      picture_border_size);

  for(int i=0; i<pictures/2; i++) {

    info("%s: reading picture %d of \"%s\"\n", argv[0], i, odd_fn);

    /* Luma. */
    //texture.read(O_fd, predicted, pixels_in_y, pixels_in_x);
    // {{{ predicted <- O
    texture.read_picture(predicted,
		       pixels_in_y, pixels_in_x,
		       odd_fn,
		       i,
		       LUMA
#if defined __INFO__
		       ,
		       argv[0]
#endif /* __INFO__ */
		       );
    // }}}

    /* Chroma. */
    /*fseek(O_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);
      fseek(O_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);*/

    info("%s: reading picture %d of \"%s\"\n", argv[0], i, even_fn);

    /* This initialization seems to do nothing. */
    for(int y=0; y<pixels_in_y << subpixel_accuracy; y++) {
      for(int x=0; x<pixels_in_x <<subpixel_accuracy; x++) {
	reference[1][y][x] = 0;
      }
    }

    /* Read the luma of reference[1]. */
    // {{{ reference[1] <- E
    texture.read_picture(reference[1],
		       pixels_in_y, pixels_in_x,
		       even_fn,
		       i,
		       LUMA
#if defined __INFO__
		       ,
		       argv[0]
#endif /* __INFO__ */
		       );
    // }}}
    //texture.read(E_fd, reference[1], pixels_in_y, pixels_in_x);

    /* Cromas. */
    /*fseek(E_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);
      fseek(E_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);*/

    /* Fill the edge of the read picture. */
    texture.fill_border(reference[1],
			pixels_in_y,
			pixels_in_x,
			picture_border_size);

    info("%s: reading initial motion vectors\n", argv[0]);
    //motion.read(imotion_fd, mv, blocks_in_y, blocks_in_x);
    //This does nothing (leave the above).
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	mv[PREV][Y_FIELD][by][bx] = mv[PREV][X_FIELD][by][bx] = mv[NEXT][Y_FIELD][by][bx] = mv[NEXT][X_FIELD][by][bx] = 0;
      }
    }

    me_for_picture(mv,
		 reference,
		 predicted,
		 pixels_in_y, pixels_in_x,
		 block_size,
		 border_size,
		 subpixel_accuracy,
		 search_range,
		 blocks_in_y,
		 blocks_in_x,
		 texture_dwt,
		 motion_dwt);
    
#ifdef CLEAR_MVS
    for(int y=0; y<blocks_in_y; y++) {
      for(int x=0; x<blocks_in_x; x++) {
	mv[PREV][Y_FIELD][y][x] = 0;
	mv[PREV][X_FIELD][y][x] = 0;
	mv[NEXT][Y_FIELD][y][x] = 0;
	mv[NEXT][X_FIELD][y][x] = 0;
      }
    }
#endif

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

#if defined __GNUPLOT__
    for(int y=0; y<blocks_in_y; y++) {
      for(int x=0; x<blocks_in_x; x++) {
	printf("GNUPLOT %d %d %f %f %f %f\n",
	       x*block_size, y*block_size,
	       (float)mv[PREV][X_FIELD][y][x], (float)mv[PREV][Y_FIELD][y][x],
	       (float)mv[NEXT][X_FIELD][y][x], (float)mv[NEXT][Y_FIELD][y][x]);
      }
    }
#endif /* __GNUPLOT__ */

    info("%s: writing motion vector field %d in \"%s\"\n", argv[0], i, motion_fn);

    //motion.write(motion_fd, mv, blocks_in_y, blocks_in_x);
    motion.write_field(mv, blocks_in_y, blocks_in_x, motion_fn, i
#if defined __INFO__
		       , argv[0]
#endif /* __INFO__ */
		       );
		       
#ifdef _1_
    // {{{ mv[0][0] -> motion
    motion.write_component(mv[0][0],
			   blocks_in_y, blocks_in_x,
			   motion_fn,
			   i,
			   0
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    // }}}
    // {{{ mv[0][1] -> motion
    motion.write_component(mv[0][1],
			   blocks_in_y, blocks_in_x,
			   motion_fn,
			   i,
			   1
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    // }}}
    // {{{ mv[1][0] -> motion
    motion.write_component(mv[1][0],
			   blocks_in_y, blocks_in_x,
			   motion_fn,
			   i,
			   2
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    // }}}
    // {{{ mv[1][1] -> motion
    motion.write_component(mv[1][1],
			   blocks_in_y, blocks_in_x,
			   motion_fn,
			   i,
			   3
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    // }}}
#endif /* _1_ */
    /* SWAP(&reference_pic[0], &reference_pic[1]). */ {
      TC_CPU_TYPE **tmp = reference[0];
      reference[0] = reference[1];
      reference[1] = tmp;
    }
  }

  delete motion_dwt;
  delete texture_dwt;

}
