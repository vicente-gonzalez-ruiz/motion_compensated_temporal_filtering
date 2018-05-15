/* De/correlate a sequence of images using the input bidirectional
   motion vector fields. When it is used to analyze, uses information
   about the movement to generate a prediction of the odd images
   (predicted frames) from the pairs (reference images). Then the
   predictions are subtracted at odd images to generate high temporal
   frequency band (images of error). If the predicted image has a
   lower or equal to the image entropy residue, then the predicted
   image which becomes part of the high frequency subband. When used
   to synthesize, the motion information used to generate a prediction
   of the odd images from the even-numbered images. Then the
   predictions are combined with the high temporal frequency band
   (error images) to generate the odd images. The subtraction or the
   sum of images is performed in the image domain.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

#define __INFO__
#define __DEBUG__
#define __WARNING__

#include "display.cpp"
//#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include "entropy.h"
#include "common.h"

#define TEXTURE_INTERPOLATION_FILTER _5_3
#define __GET_PREDICTION__ /* If defined, shows information about predictions. */

void predict
(
 int block_overlaping,
 int block_size,
 int blocks_in_y,
 int blocks_in_x,
 int components,
 int pixels_in_y,
 int pixels_in_x,
 MVC_TYPE ****mv,
 class dwt2d < TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TC_CPU_TYPE > > *overlap_dwt,
 TC_CPU_TYPE **prediction_block,
 TC_CPU_TYPE ***prediction_picture,
 TC_CPU_TYPE ****reference_picture
) {
  int dwt_border = block_overlaping;
  int levels = 0;
  if(block_overlaping>0) {
    levels = (int)rint(log((double)block_overlaping)/log(2.0));
  }
  for(int c=0; c<components; c++) {
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	
	int mvy0 = mv[PREV][Y_FIELD][by][bx] + by * block_size;
	int mvy1 = mv[NEXT][Y_FIELD][by][bx] + by * block_size;
	int mvx0 = mv[PREV][X_FIELD][by][bx] + bx * block_size;
	int mvx1 = mv[NEXT][X_FIELD][by][bx] + bx * block_size;

	/* Each block is copied. */
	for(int y=-dwt_border; y<(block_size+dwt_border); y++) {
	  for(int x=-dwt_border; x<(block_size+dwt_border); x++) {
	    prediction_block[y+dwt_border][x+dwt_border]
	      =
	      (reference_picture[PREV][c][mvy0+y][mvx0+x]
	       +
	       reference_picture[NEXT][c][mvy1+y][mvx1+x])
	      /2;
	  }
	}
	
	/* Apply DWT to each block. */
	overlap_dwt->analyze(prediction_block,
			     block_size + dwt_border * 2,
			     block_size + dwt_border * 2,
			     levels);
	
	/* Copy to "prediction_picture" high frequency subbands. */ {
	  for(int l=1; l<=levels; l++) {
	    int bs = block_size>>l;
	    for(int y=0; y<bs; y++) {
	      for(int x=0; x<bs; x++) {
		/* Subband LH */
		prediction_picture
		  [c]
		  [by*bs+y]
		  [(pixels_in_x>>l)+bx*bs+x]
		  =
		  prediction_block
		  [(dwt_border>>l)+y]
		  [((block_size+dwt_border*3)>>l)+x];
		/* Subband HL */
		prediction_picture
		  [c]
		  [(pixels_in_y>>l)+by*bs+y]
		  [bx*bs+x]
		  =
		  prediction_block
		  [((block_size+dwt_border*3)>>l)+y]
		  [(dwt_border>>l)+x];
		/* Subband HH */
		prediction_picture
		  [c]
		  [(pixels_in_y>>l)+by*bs+y]
		  [(pixels_in_x>>l)+bx*bs+x]
		  =
		  prediction_block
		  [((block_size+dwt_border*3)>>l)+y]
		  [((block_size+dwt_border*3)>>l)+x];
	      } /* for(x) */
	    } /* for(y) */
	  } /* for(l) */
	} /* High frequency subbands. */
	
	/* Copy to "prediction_picture" low frequency subband (LL). */ { 
	  int bs = block_size>>levels;
	  for(int y=0; y<bs; y++) {
	    for(int x=0; x<bs; x++) {
	      prediction_picture
		[c]
		[by*bs+y]
		[bx*bs+x]
		=
		prediction_block
		[(dwt_border>>levels)+y]
		[(dwt_border>>levels)+x];
	    } /* for(x) */
	  } /* for(y) */
	} /* Band LL. */
      } /* for(blocks_in_y) */
    } /* for(blocks_in_x) */
    
    /* The prediction image is generated.*/
    overlap_dwt->synthesize(prediction_picture[c], pixels_in_y, pixels_in_x, levels);
   
#ifdef _1_ 
    if(levels) {
      /** And clipping of the prediction if _1_ is defined. */
      for(int y=0; y<pixels_in_y; y++) {
	for(int x=0; x<pixels_in_x; x++) {
	  TC_CPU_TYPE aux = prediction_picture[c][y][x];
	  if(aux<MIN_TC_VAL) aux=MIN_TC_VAL;
	  else if(aux>MAX_TC_VAL) aux=MAX_TC_VAL;
	  prediction_picture[c][y][x] = aux;
	}
      }
    }
#endif
  } /* for(components) */

} /* predict() */


#include <getopt.h>

int main(int argc, char *argv[]) {

#if defined __INFO__
  info("%s ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif /* __INFO__ */

  int block_overlaping = 0;
  int block_size = 16;
  int components = COMPONENTS;
  char *even_fn = (char *)"even";
  char *frame_types_fn = (char *)"frame_types";
  char *high_fn = (char *)"high";
  char *motion_in_fn = (char *)"motion_in";
#if defined __ANALYZE__
  char *motion_out_fn = (char *)"motion_out";
#endif /* __ANALYZE__ */
  char *odd_fn = (char *)"odd";
  int pictures = 33;
  int pixels_in_x[COMPONENTS] = {PIXELS_IN_X, PIXELS_IN_X/2, PIXELS_IN_X/2};
  int pixels_in_y[COMPONENTS] = {PIXELS_IN_Y, PIXELS_IN_Y/2, PIXELS_IN_Y/2};
  int search_range = 4;
  int subpixel_accuracy = 0;
  int always_B = 0; /* By default, not force to have only B frames */
  
  int c;
  while(1) {

    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */    
    static struct option long_options[] = {
      {"block_overlaping", required_argument, 0, 'v'},
      {"block_size", required_argument, 0, 'b'},
      {"even_fn", required_argument, 0, 'e'},
      {"frame_types_fn", required_argument, 0, 'f'},
      {"high_fn", required_argument, 0, 'h'},
      {"motion_in_fn", required_argument, 0, 'i'},
#if defined __ANALYZE__
      {"motion_out_fn", required_argument, 0, 't'},
#endif /* __ANALYZE__ */
      {"odd_fn", required_argument, 0, 'o'},
      {"pictures", required_argument, 0, 'p'},
      {"pixels_in_x", required_argument, 0, 'x'},
      {"pixels_in_y", required_argument, 0, 'y'},
      {"search_range", required_argument, 0, 's'},
      {"subpixel_accuracy", required_argument, 0, 'a'},
      {"always_B", required_argument, 0, 'B'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };
    
    int option_index = 0;

    c = getopt_long(argc, argv,
#if defined __ANALYZE__
		    "v:b:e:f:h:i:t:o:p:x:y:s:a:B:?",
#else /* __ANALYZE__ */
		    "v:b:e:f:h:i:o:p:x:y:s:a:B:?",
#endif /* __ANALYZE__ */
		    long_options, &option_index);
    
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
      
    case 'v':
      block_overlaping = atoi(optarg);
      info("%s: block_overlaping=%d\n", argv[0], block_overlaping);
      break;
      
    case 'b':
      block_size = atoi(optarg);
      info("%s: block_size=%d\n", argv[0], block_size);
      break;
      
    case 'e':
      even_fn = optarg;
      info("%s: even_fn=%s\n", argv[0], even_fn);
      break;

    case 'f':
      frame_types_fn = optarg;
      info("%s: frame_types_fn=%s\n", argv[0], frame_types_fn);
      break;

    case 'h':
      high_fn = optarg;
      info("%s: high_fn=%s\n", argv[0], high_fn);
      break;

    case 'i':
      motion_in_fn = optarg;
      info("%s: motion_in_fn=%s\n", argv[0], motion_in_fn);
      break;

#if defined __ANALYZE__
    case 't':
      motion_out_fn = optarg;
      info("%s: motion_out_fn=%s\n", argv[0], motion_out_fn);
      break;
#endif

    case 'o':
      odd_fn = optarg;
      info("%s: odd_fn=%s\n", argv[0], odd_fn);
      break;

    case 'p':
      pictures = atoi(optarg);
      info("%s: pictures=%d\n", argv[0], pictures);
      break;
      
    case 'x':
      pixels_in_x[0] = atoi(optarg);
      pixels_in_x[1] = pixels_in_x[2] = pixels_in_x[0]/2;
      info("%s: pixels_in_x=%d\n", argv[0], pixels_in_x[0]);
     break;
      
    case 'y':
      pixels_in_y[0] = atoi(optarg);
      pixels_in_y[1] = pixels_in_y[2] = pixels_in_y[0]/2;
      info("%s: pixels_in_y=%d\n", argv[0], pixels_in_y[0]);
      break;

    case 's':
      search_range = atoi(optarg);
      info("%s: search_range=%d\n", argv[0], search_range);
      break;
      
    case 'a':
      subpixel_accuracy = atoi(optarg);
      info("%s: subpixel_accuracy=%d\n", argv[0], subpixel_accuracy);
      break;
      
    case 'B':
      always_B = atoi(optarg);
      info("%s: always_B=%d\n", argv[0], always_B);
      break;
      
    case '?':
#if defined __ANALYZE__
      printf("+------------------+\n");
      printf("| MCTF decorrelate |\n");
      printf("+------------------+\n");
#else /* __ANALYZE__ */
      printf("+----------------+\n");
      printf("| MCTF correlate |\n");
      printf("+----------------+\n");
#endif /* __ANALYZE__ */
      printf("\n");
#if defined __ANALYZE__
      printf("  Block-based time-domain motion decorrelation.\n");
#else /* __ANALYZE__ */
      printf("  Block-based time-domain motion correlation.\n");
#endif /* __ANALYZE__ */
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-]block_o[v]erlaping = number of overlaped pixels between the blocks in the motion compensation (%d)\n", block_overlaping);
      printf("   -[-b]lock_size = size of the blocks in the motion estimation process (%d)\n", block_size);
      printf("   -[-e]ven_fn = input file with the even pictures (\"%s\")\n", even_fn);
      printf("   -[-f]rame_types_fn = output file with the frame types (\"%s\")\n", frame_types_fn);
      printf("   -[-h]igh_fn = input file with high-subband pictures (\"%s\")\n", high_fn);
      printf("   -[-]motion_[i]n_fn = input file with the motion fields (\"%s\")\n", motion_in_fn);
#if defined __ANALYZE__
      printf("   -[-]mo[t]ion_out_fn = output file with the motion fields (\"%s\")\n", motion_out_fn);
#endif /* __ANALYZE__ */
      printf("   -[-o]dd_fn = input file with odd pictures (\"%s\")\n", odd_fn);
      printf("   -[-p]ictures = number of images to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x[0]);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y[0]);
      printf("   -[-s]earch_range = size of the searching area of the motion estimation (%d)\n", search_range);
      printf("   -[-]subpixel_[a]ccuracy = sub-pixel accuracy of the motion estimation (%d)\n", subpixel_accuracy);
      printf("   -[-]always_[B] (%d)\n", always_B);
      printf("\n");
      exit(1);
      break;
      
    default:
      error("%s: Unrecognized argument.\n", argv[0]);
    }
  }

#ifdef _1_
  {
    int err = mkdir(even_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], even_fn);
      abort();
    }
#endif /* __DEBUG__ */
  }
#endif

  {
#if defined __ANALYZE__
    int err = mkdir(motion_out_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], motion_out_fn);
      abort();
    }
#endif /* __DEBUG__ */
#endif /* __ANALYZE__ */
  }

#ifdef _1_
  {
#if defined __ANALYZE__
    int err = mkdir(odd_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], odd_fn);
      abort();
    }
#endif /* __DEBUG__ */
#endif /* __ANALYZE__ */
  }
#endif
  
  {
#if defined __ANALYZE__
    int err = mkdir(high_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], high_fn);
      abort();
    }
#endif /* __DEBUG__ */
#endif /* __ANALYZE__ */
  }
  
#if defined __GET_PREDICTION__
  char prediction_fn[80];
  sprintf(prediction_fn, "prediction_%s", even_fn);
  {
    int err = mkdir(prediction_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], prediction_fn);
      abort();
    }
#endif /* __DEBUG__ */
  }
#endif /* __GET_PREDICTION__ */
  
  FILE *frame_types_fd; {
    frame_types_fd = fopen(frame_types_fn,
#if defined __ANALYZE__
			   "w"
#else /* __ANALYZE__ */
			   "r"
#endif /* __ANALYZE__ */
			   );
    if(!frame_types_fd) {
#if defined __ANALYZE__
      error("%s: unable to write \"%s\" ... aborting!\n", argv[0], frame_types_fn);
#else /* __ANALYZE__ */
      error("%s: unable to read \"%s\" ... aborting!\n", argv[0], frame_types_fn);    
#endif /* __ANALYZE__ */
      abort();
    }
  }

  class dwt2d <
    TC_CPU_TYPE,
    TEXTURE_INTERPOLATION_FILTER <
      TC_CPU_TYPE
      >
    >
    *image_dwt = new class dwt2d <
      TC_CPU_TYPE,
    TEXTURE_INTERPOLATION_FILTER <
      TC_CPU_TYPE
      >
    >;
  image_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  int blocks_in_y = pixels_in_y[0]/block_size;
  int blocks_in_x = pixels_in_x[0]/block_size;
  info("%s: blocks_in_y = %d\n", argv[0], blocks_in_y);
  info("%s: blocks_in_x = %d\n", argv[0], blocks_in_x);

  motion < MVC_TYPE > motion;
  texture < TC_IO_TYPE, TC_CPU_TYPE > texture;

  MVC_TYPE ****mv = motion.alloc(blocks_in_y, blocks_in_x);

  MVC_TYPE ****zeroes = motion.alloc(blocks_in_y, blocks_in_x);
  for(int by=0; by<blocks_in_y; by++) {
    for(int bx=0; bx<blocks_in_x; bx++) {
      zeroes[0][0][by][bx] = 0;
      zeroes[0][1][by][bx] = 0;
      zeroes[1][0][by][bx] = 0;
      zeroes[1][1][by][bx] = 0;
    }
  }
  
  TC_CPU_TYPE **prediction_block =
    texture.alloc((pixels_in_y[0]/blocks_in_y + block_overlaping*2)
		  << subpixel_accuracy,
		  (pixels_in_x[0]/blocks_in_x + block_overlaping*2)
		  << subpixel_accuracy,
		  0);

  int picture_border_size = 4*search_range + block_overlaping;
  info("%s: picture_border = %d\n", argv[0], picture_border_size);

  TC_CPU_TYPE ***reference[2];
  for(int i=0; i<2; i++) {
    reference[i] = new TC_CPU_TYPE ** [COMPONENTS];
    for(int c=0; c<COMPONENTS; c++) {
      reference[i][c] =
	texture.alloc(pixels_in_y[0] << subpixel_accuracy,
		      pixels_in_x[0] << subpixel_accuracy,
		      picture_border_size << subpixel_accuracy);
    }
  }
  
  TC_CPU_TYPE ***predicted = new TC_CPU_TYPE ** [COMPONENTS];
  for(int c=0; c<COMPONENTS; c++) {
    predicted[c] = texture.alloc(pixels_in_y[c], /* c */
				 pixels_in_x[c], /* c */
				 picture_border_size);
  }

  TC_CPU_TYPE ***prediction = new TC_CPU_TYPE ** [COMPONENTS];
  for(int c=0; c<COMPONENTS; c++) {
    prediction[c] = texture.alloc(pixels_in_y[0] << subpixel_accuracy,
				  pixels_in_x[0] << subpixel_accuracy,
				  0);
  }
  
  TC_CPU_TYPE ***residue = new TC_CPU_TYPE ** [COMPONENTS];
  for(int c=0; c<COMPONENTS; c++) {
    residue[c] = texture.alloc(pixels_in_y[c], /* c */
			       pixels_in_x[c], /* c */
			       0/*picture_border_size*/);
  }
  
#if defined __GET_PREDICTION__
  TC_CPU_TYPE *line = (TC_CPU_TYPE *)malloc(pixels_in_x[0]*sizeof(TC_CPU_TYPE));
#endif /* __GET_PREDICTION__ */
  
  /* Decorrelation begins. */
  
  /* Read reference [0] (the first image). */
  for(int c=0; c<COMPONENTS; c++) {
    // image.read(even_fd, reference[0][c], pixels_in_y[c], pixels_in_x[c]);
    // {{{ reference[0] <- even
    texture.read_image(reference[0][c],
		       pixels_in_y[c], pixels_in_x[c],
		       even_fn,
		       0,
		       c
#if defined __INFO__
		       ,
		       argv[0]
#endif /* __INFO__ */
		       );
    // }}}
  }

  /* Interpolate the chroma of reference [0], to have the same size as
      the luma.  This is necessary because the fields of motion apply
      to chroma with the same precision as the luma. */

  /* Chroma Cb. */

  /*
    +--------------+--------------+
    |              |00000000000000|
    |              |00000000000000|
    |              |00000000000000|
    |              |00000000000000|
    |              |00000000000000|
    |              |00000000000000|
    +--------------+--------------+
    |              |              |
    |              |              |
    |              |              |
    |              |              |
    |              |              |
    |              |              |
    +--------------+--------------+
   */
  for(int y=0; y<pixels_in_y[0]/2; y++) {
    memset(reference[0][1][y]+pixels_in_x[0]/2, 0,
	   (pixels_in_x[0]*sizeof(TC_CPU_TYPE))/2);
  }

  /*
    +--------------+--------------+
    |              |              |
    |              |              |
    |              |              |
    |              |              |
    |              |              |
    |              |              |
    +--------------+--------------+
    |00000000000000|00000000000000|
    |00000000000000|00000000000000|
    |00000000000000|00000000000000|
    |00000000000000|00000000000000|
    |00000000000000|00000000000000|
    |00000000000000|00000000000000|
    +--------------+--------------+
   */

  for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
    memset(reference[0][1][y], 0, pixels_in_x[0]*sizeof(TC_CPU_TYPE));
  }

  /* Interpolation. */
  image_dwt->synthesize(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);

  /* Chroma Cr. */
  for(int y=0; y<pixels_in_y[0]/2; y++) {
    memset(reference[0][2][y]+pixels_in_x[0]/2, 0,
	   (pixels_in_x[0]*sizeof(TC_CPU_TYPE))/2);
  }
  for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
    memset(reference[0][2][y], 0, pixels_in_x[0]*sizeof(TC_CPU_TYPE));
  }
  image_dwt->synthesize(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1); 

  /** At this point, referece [0] has its three components with the
      same size.  It's time to interpolate (interpolation leads to
      errors).\n And fill edges, if you are using sub-pixel estimation
      movement. */

  /* Interpolate and fill edges. */
  for(int c = 0; c < COMPONENTS; c++) {
    
    for(int s = 1; s <= subpixel_accuracy; s++) {
      
      /* Interpolate (the error is here!) */
      for(int y = 0; y < ( pixels_in_y[0] << s ) / 2; y++) {
	memset ( reference[0][c][y] + ( pixels_in_x[0] << s ) / 2,
		 0,
		 ( ( ( pixels_in_x[0] << s ) / 2 ) * sizeof(TC_CPU_TYPE) )
		 );
      }
      
      for(int y = ( pixels_in_y[0] << s) / 2; y < ( pixels_in_y[0] << s); y++) {
	memset(reference[0][c][y],
	       0,
	       ( pixels_in_x[0] << s ) *sizeof(TC_CPU_TYPE) );
      }
      image_dwt->synthesize(reference[0][c],
			    pixels_in_y[0] << s,
			    pixels_in_x[0] << s,
			    1);
      
    }
    
    /* Fill edges. */
    texture.fill_border(reference[0][c],
			pixels_in_y[0] << subpixel_accuracy,
			pixels_in_x[0] << subpixel_accuracy,
			picture_border_size << subpixel_accuracy);
    
  }
  
  /* The other images are processed. */
  
  for(int i=0; i<pictures/2; i++) {
    
#if defined __ANALYZE__
    info("%s: reading picture %d of \"%s\".\n", argv[0], i, odd_fn);

    /* The next image (to predict) */
    for(int c=0; c<COMPONENTS; c++) {
      //image.read(odd_fd, predicted[c], pixels_in_y[c], pixels_in_x[c]);
      // {{{ predicted <- odd
      texture.read_image(predicted[c],
			 pixels_in_y[c], pixels_in_x[c],
			 odd_fn,
			 i,
			 c
#if defined __INFO__
			 ,
			 argv[0]
#endif /* __INFO__ */
			 );
      // }}}
    }

#else /* __ANALYZE__ */

    info("%s: reading picture %d of \"%s\".\n", argv[0], i, high_fn);
    
    /* Read residue image */
    for(int c=0; c<COMPONENTS; c++) {
      //image.read(high_fd, residue[c], pixels_in_y[c], pixels_in_x[c]);
      // {{{ residue -> high
      texture.read_image(residue[c],
			 pixels_in_y[c], pixels_in_x[c],
			 high_fn,
			 i,
			 c
#if defined __INFO__
			 ,
			 argv[0]
#endif /* __INFO__ */
			 );
      // }}}
      for(int y=0; y<pixels_in_y[c]; y++) {
	for(int x=0; x<pixels_in_x[c]; x++) {
	  residue[c][y][x] -= 128;
	}
      }
    }

#endif /* __ANALYZE__ */
    
    info("%s: reading picture %d of \"%s\".\n", argv[0], i, even_fn);
    
    /* Read reference [1], interpolating the chroma. */
    for(int c=0; c<COMPONENTS; c++) {
      //image.read(even_fd, reference[1][c], pixels_in_y[c], pixels_in_x[c]);
      // {{{ reference[1] <- even
      texture.read_image(reference[1][c],
			 pixels_in_y[c], pixels_in_x[c],
			 even_fn,
			 i,
			 c
#if defined __INFO__
			 ,
			 argv[0]
#endif /* __INFO__ */
			 );
      // }}}
    }

    /* Croma Cb. */
    for(int y=0; y<pixels_in_y[0]/2; y++) {
      memset(reference[1][1][y]+pixels_in_x[0]/2, 0,
	     (pixels_in_x[0]*sizeof(TC_CPU_TYPE))/2);
    }
    for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
      memset(reference[1][1][y], 0, pixels_in_x[0]*sizeof(TC_CPU_TYPE));
    }
    image_dwt->synthesize(reference[1][1], pixels_in_y[0], pixels_in_x[0], 1);

    /* Croma Cr. */
    for(int y=0; y<pixels_in_y[0]/2; y++) {
      memset(reference[1][2][y]+pixels_in_x[0]/2, 0,
	     (pixels_in_x[0]*sizeof(TC_CPU_TYPE))/2);
    }
    for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
      memset(reference[1][2][y], 0, pixels_in_x[0]*sizeof(TC_CPU_TYPE));
    }
    image_dwt->synthesize(reference[1][2], pixels_in_y[0], pixels_in_x[0], 1);

    /* Interpolate and fill edges. */
    
    for(int c = 0; c < COMPONENTS; c++) {      
      for(int s = 1; s <= subpixel_accuracy; s++) {
	
	/* Interpolate. */
	for(int y = 0; y < ( pixels_in_y[0] << s ) / 2; y++) {
	  memset ( reference[1][c][y] + ( pixels_in_x[0] << s ) / 2,
		   0,
		   ( ( ( pixels_in_x[0] << s ) / 2 ) * sizeof(TC_CPU_TYPE) )
		   );
	}
	
	for(int y = ( pixels_in_y[0] << s) / 2; y < ( pixels_in_y[0] << s); y++) {
	  memset(reference[1][c][y],
		 0,
		 ( pixels_in_x[0] << s ) *sizeof(TC_CPU_TYPE) );
	}
	image_dwt->synthesize(reference[1][c],
			      pixels_in_y[0] << s,
			      pixels_in_x[0] << s,
			      1);

      }
      
      /* Fill edges. */
      texture.fill_border(reference[1][c],
			  pixels_in_y[0] << subpixel_accuracy,
			  pixels_in_x[0] << subpixel_accuracy,
			  picture_border_size << subpixel_accuracy);
      
    }

    /* Motion fields are read. */
    info("%s: reading motion vector field %d in \"%s\".\n", argv[0], i, motion_in_fn);
    //motion.read(motion_in_fd, mv, blocks_in_y, blocks_in_x);
    // {{{ mv[0][0] <- motion_in
    motion.read_component(mv[0][0],
			  blocks_in_y, blocks_in_x,
			  motion_in_fn,
			  i,
			  0
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ mv[0][1] <- motion_in
    motion.read_component(mv[0][1],
			  blocks_in_y, blocks_in_x,
			  motion_in_fn,
			  i,
			  1
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ mv[1][0] <- motion_in
    motion.read_component(mv[1][0],
			  blocks_in_y, blocks_in_x,
			  motion_in_fn,
			  i,
			  2
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ mv[1][1] <- motion_in
    motion.read_component(mv[1][1],
			  blocks_in_y, blocks_in_x,
			  motion_in_fn,
			  i,
			  3
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
#if defined __ANALYZE__
    float motion_entropy = 0.0; {
      static int count[256];
      
      if(!always_B) {
	
	for(int i=0; i<256; i++) {
	  count[i] = 0;
	}
	
	for(int y=0; y<blocks_in_y; y++) {
	  for(int x=0; x<blocks_in_x; x++) {
	    count[ mv[PREV][Y_FIELD][y][x] + 128 ]++;
	    count[ mv[PREV][X_FIELD][y][x] + 128 ]++;
	    count[ mv[NEXT][Y_FIELD][y][x] + 128 ]++;
	    count[ mv[NEXT][X_FIELD][y][x] + 128 ]++;
	  }
	}
	
	motion_entropy = entropy(count, 256);

      }
    }
#endif /* __ANALYZE__ */

    /** If the entropy of the predicted image is less than or equal to
	the entropy of the "wrong image" then the predicted image
	replaces the "wrong image". */

    /* Write the residue image, the chroma is subsampled. */
    predict(block_overlaping << subpixel_accuracy,
	    block_size << subpixel_accuracy,
	    blocks_in_y,
	    blocks_in_x,
	    COMPONENTS,
	    pixels_in_y[0] << subpixel_accuracy,
	    pixels_in_x[0] << subpixel_accuracy,
	    mv,
	    image_dwt,
	    prediction_block,
	    prediction,
	    reference);
    
    for(int c=0; c<COMPONENTS; c++) {
      for(int y=0; y<pixels_in_y[0] << subpixel_accuracy; y++) {
	for(int x=0; x<pixels_in_x[0] << subpixel_accuracy; x++) {
	  if (prediction[c][y][x] < 0) prediction[c][y][x] = 0;
	  else if (prediction[c][y][x] > 255) prediction[c][y][x] = 255;
	}
      }
    }
    
    /* Subsample the three components because the motion compensation
       is made to the original video resolution. */
    for(int c=0; c<COMPONENTS; c++) {
      image_dwt->analyze(prediction[c],
			 pixels_in_y[0] << subpixel_accuracy,
			 pixels_in_x[0] << subpixel_accuracy,
			 subpixel_accuracy);
    }
    
    /* The prediction is still on: YUV444; and we must pass it: YUV422. */
    image_dwt->analyze(prediction[1], pixels_in_y[0], pixels_in_x[0], 1);
    image_dwt->analyze(prediction[2], pixels_in_y[0], pixels_in_x[0], 1);
    
#if defined __GET_PREDICTION__
    info("%s: writing picture %d of \"%s\".\n", argv[0], i, prediction_fn);
    for(int c=0; c<COMPONENTS; c++) {
      // {{{ prediction -> prediction
      texture.write_image(prediction[c],
			  pixels_in_y[c], pixels_in_x[c],
			  prediction_fn,
			  i,
			  c
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
      // }}}
    }
#endif /* __GET_PREDICTION__ */
    
#if defined __ANALYZE__
    
    /* The residue image is generated. */
    
    info("%s: writing picture %d of \"%s\".\n", argv[0], i, high_fn);
    
    /*
      A subtraction at high resolution and a reduction,
      vs, 
      Two reductions and a subtraction at low resolution.
      
      Without truncating:
      
      1 2 3 4   1 1 2 2   0  1  1  2     0.5  1.5
      5 6 7 8 - 5 5 6 6 = 0  1  1  2 -> -0.5 -1.5
      8 7 6 5   8 8 7 7   0 -1 -1 -2
      4 3 2 1   4 4 3 3   0 -1 -1 -2
      
      |         |
      v         v
      
      3.5 5.5 - 3.0 4.0 =  0.5  1.5
      5.5 3.5   6.0 5.0   -0.5 -1.5
      
      Truncating:
      
      1 2 3 4   1 1 2 2   0  1  1  2     0  1
      5 6 7 8 - 5 5 6 6 = 0  1  1  2 -> -1 -2
      8 7 6 5   8 8 7 7   0 -1 -1 -2
      4 3 2 1   4 4 3 3   0 -1 -1 -2
      
      |         |
      v         v
      
      3 5     -   3 4 =  0  1
      5 3         6 5   -1 -2
      
      That is, the motion compensation at high resolution is the
      same as at low resolution (if the predictions are equal).
    */
    
    
    /* Compensation is applied (with clipping). The compensation is
       done over-pixel resolution. */
    for(int c=0; c<COMPONENTS; c++) {
      for(int y=0; y<pixels_in_y[c]; y++) {
	for(int x=0; x<pixels_in_x[c]; x++) {
	  int val = predicted[c][y][x] - prediction[c][y][x];
	  if(val < -128) val = -128;
	  else if(val > 127) val = 127;
	  residue[c][y][x] = val;
	}
      }
    }
    
    /* The entropy of the residual image and the predicted image is
       calculated. We only use the luma. */

    float residue_entropy = 0.0, predicted_entropy = 1.0; {
      static int predicted_count[256];
      static int residue_count[256];
      
      if (!always_B) {
	
	for(int i=0; i<256; i++) {
	  predicted_count[i] = 0;
	  residue_count[i] = 0;
	}
	
	for(int y=0; y<pixels_in_y[0]; y++) {
	  for(int x=0; x<pixels_in_x[0]; x++) {
	    predicted_count[ predicted[0][y][x]       ]++;
	    residue_count  [ residue  [0][y][x] + 128 ]++; // Usar puntero
	  }
	}
	
	predicted_entropy = entropy(predicted_count, 256);
	residue_entropy = entropy(residue_count, 256);
	
      }
    }

    /* If the entropy of the predicted image is less than or equal to
       the entropy of the "wrong image" then the predicted image
       replaces the "wrong image". */

      /* Write the residue image, the chroma subsampling. */

    int predicted_size
      = (int)(predicted_entropy * (float)pixels_in_y[0] * (float)pixels_in_x[0]);
    int residue_size
      = (int)(residue_entropy * (float)pixels_in_y[0] * (float)pixels_in_x[0]);
    int motion_size
      = (int)(motion_entropy * (float)blocks_in_y * (float)blocks_in_x);

    info("predicted_entropy=%f residue_entropy=%f motion_entropy=%f\n",
	 predicted_entropy, residue_entropy, motion_entropy);
    info("predicted_size=%d residue_size=%d motion_size=%d\n",
	 predicted_size, residue_size, motion_size);

    //if(predicted_entropy <= (residue_entropy + motion_entropy)) /* Image of type I. */ {
    if(predicted_size <= (residue_size + motion_size)) {

      /* Indicated in the code-stream which is an image I. */
      putc('I', frame_types_fd);

      /* Copy predicted to residue. */
      
      for(int c=0; c<COMPONENTS; c++) {
	for(int y=0; y<pixels_in_y[c] /* c */; y++) {
	  for(int x=0; x<pixels_in_x[c] /* c */; x++) {
	    residue[c][y][x] = predicted[c][y][x];
	    //printf("%d ",residue[c][y][x]);
	  }
	}
      }
      
      for(int c=0; c<COMPONENTS; c++) {
	//image.write(high_fd, residue[c], pixels_in_y[c], pixels_in_x[c]);
	// {{{ residue -> high
	texture.write_image(residue[c],
			    pixels_in_y[c], pixels_in_x[c],
			    high_fn,
			    i,
			    c
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
	// }}}
      }

      /* No motion field (other than 0) associated with an image I. */
      //motion.write(motion_out_fd, zeroes, blocks_in_y, blocks_in_x);
      // {{{ zeroes[0][0] -> motion_out
      motion.write_component(zeroes[0][0],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     0
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ zeroes[0][1] -> motion_out
      motion.write_component(zeroes[0][1],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     1
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ zeroes[1][0] -> motion_out
      motion.write_component(zeroes[1][0],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     2
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ zeroes[1][1] -> motion_out
      motion.write_component(zeroes[1][1],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     3
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
    } else {

      /* Indicated in the code-stream which is an image B. */
      putc('B', frame_types_fd);

      /* We turn to the range [0,255] possibly with clipping and write to disk. */

      for(int c=0; c<COMPONENTS; c++) {
	/* The following loop is only necessary if the dynamic range
	   of the residue image must be stored in the range
	   [0,255]. */
	for(int y=0; y<pixels_in_y[c]; y++) {
	  for(int x=0; x<pixels_in_x[c]; x++) {
	    int val = residue[c][y][x] + 128;
	    if(val < 0) val = 0;
	    else if(val > 255) val = 255;
	    residue[c][y][x] = val;
	  }
	}
	//image.write(high_fd, residue[c], pixels_in_y[c], pixels_in_x[c]);
	// {{{ residue -> high
	texture.write_image(residue[c],
			    pixels_in_y[c], pixels_in_x[c],
			    high_fn,
			    i,
			    c
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );

	// }}}
      }

      /* The images I have associated motion field. */
      //motion.write(motion_out_fd, mv, blocks_in_y, blocks_in_x);
      // {{{ mv[0][0] -> motion_out
      motion.write_component(mv[0][0],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     0
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ mv[0][1] -> motion_out
      motion.write_component(mv[0][1],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     1
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ mv[1][0] -> motion_out
      motion.write_component(mv[1][0],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     2
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ mv[1][1] -> motion_out
      motion.write_component(mv[1][1],
			     blocks_in_y, blocks_in_x,
			     motion_out_fn,
			     i,
			     3
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      
    }
    
#else /* __ANALYZE__ */

    info("%s: writing picture %d of \"%s\".\n", argv[0], i, odd_fn);

    /** Decorrelation. */

    if(fgetc(frame_types_fd) == 'I') {

      /* If the picture is of type I, copy residue to predicted. */
      for(int c=0; c<COMPONENTS; c++) {
	for(int y=0; y<pixels_in_y[c]; y++) {
	  for(int x=0; x<pixels_in_x[c]; x++) {
	    predicted[c][y][x] = residue[c][y][x] + 128;
	    /*	    if (predicted[c][y][x] < 0 ) predicted[c][y][x] = 0;
		    else if(predicted[c][y][x] > 255 ) predicted[c][y][x] = 255;*/
	  }
	}
      }
    } else {
      for(int c=0; c<COMPONENTS; c++) {
	for(int y=0; y<pixels_in_y[c]; y++) {
	  for(int x=0; x<pixels_in_x[c]; x++) {
	    int val = residue[c][y][x] + prediction[c][y][x];
	    if(val<0) val=0;
	    else if(val>255) val=255;
	    predicted[c][y][x] = val;
	  }
	}
      }
    }

    /* Write predicted image. */
    for(int c=0; c<COMPONENTS; c++) {
      //image.write(odd_fd, predicted[c], pixels_in_y[c], pixels_in_x[c]);
      // {{{ predicted -> odd
      texture.write_image(predicted[c],
			  pixels_in_y[c], pixels_in_x[c],
			  odd_fn,
			  i,
			  c
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
      // }}}			  
    }

#endif /* __ANALYZE__ */
    
    /* SWAP(&reference_picture[0], &reference_picture[1]). */ {
      TC_CPU_TYPE ***tmp = reference[0];
      reference[0] = reference[1];
      reference[1] = tmp;
    }
  }

  delete image_dwt;
}
