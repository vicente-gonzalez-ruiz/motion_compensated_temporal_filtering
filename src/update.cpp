#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

//#define __INFO__
//#define __DEBUG__
#define __WARNING__

#include "display.cpp"
//#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include "common.h"

#define TEXTURE_INTERPOLATION_FILTER _5_3

/* Clipping. */
int clip(int x, int dim) {
  if(x<0) return 0;
  if(x>=dim) return dim-1;
  return x;   
}

/* Adds even pictures (S_ {2i}) to the prediction error.  This should
 * reduce the aliasing. A value for update_factor equal to 1/4 means
 * that the high-frequency subband is 4 times less important than the
 * low-frequency subband.
 */
void update
(
 int block_size,
 int blocks_in_y,
 int blocks_in_x,
 int components,
 MVC_TYPE ****mv,
 int *pixels_in_y,
 int *pixels_in_x,
 TC_CPU_TYPE ****reference_picture,
 TC_CPU_TYPE ***residue_picture,
 float update_factor
#if defined __WARNING__
 ,
 char *name
#endif
) {
  // {{{
  for(int c=0; c<components; c++) {
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	for(int y=0; y<block_size; y++) {
	  for(int x=0; x<block_size; x++) {
	    float aux;

	      /* Update the previous picture. ******************************/
	      aux = reference_picture[PREV][c]
		[clip(by*block_size + y + mv[PREV][Y_FIELD][by][bx],
		      pixels_in_y[c])]
		[clip(bx*block_size + x + mv[PREV][X_FIELD][by][bx],
		      pixels_in_x[c])];
	      //aux *= update_factor /* 1<<iteration */;

	      aux
#ifdef __ANALYZE__
		+= 
#else /* __ANALYZE__ */
		-=
#endif /* __ANALYZE__ */
		residue_picture
		[c]
		[by*block_size+y]
		[bx*block_size+x]
		* update_factor;

	      //aux /= update_factor;
#ifdef _1_
	      if(aux > MAX_TC_VAL) {
#if defined __WARNING__
		warning("%s: MAX_TC_VAL reached (clipping %f -> %d)!\n", name, aux, MAX_TC_VAL);
#endif
		aux = MAX_TC_VAL;
	      }
	      else if(aux < MIN_TC_VAL) {
#if defined __WARNING__
		warning("%s: MIN_TC_VAL reached (clipping %f -> %d)!\n", name, aux, MIN_TC_VAL);
#endif
		aux = MIN_TC_VAL;
	      }
#endif
	      reference_picture[PREV][c]
		[clip(by*block_size + y + mv[PREV][Y_FIELD][by][bx],
		      pixels_in_y[c])]
		[clip(bx*block_size + x + mv[PREV][X_FIELD][by][bx],
		      pixels_in_x[c])]
		= (TC_CPU_TYPE)round(aux);
	      
	      /* Update the next picture. **********************************/
	      aux = reference_picture[NEXT][c]
		[clip(by*block_size + y + mv[NEXT][Y_FIELD][by][bx],
		      pixels_in_y[c])]
		[clip(bx*block_size + x + mv[NEXT][X_FIELD][by][bx],
		      pixels_in_x[c])];
	      
	      //aux *= update_factor;

	      //fprintf(stderr,"(first) aux=%f\n", aux);
	      aux
#ifdef __ANALYZE__
		+= 
#else /* __ANALYZE__ */
		-=
#endif /* __ANALYZE__ */
		residue_picture[c][by*block_size+y][bx*block_size+x] * update_factor;

	      //aux /= update_factor;
#ifdef _1_	      
	      if(aux > MAX_TC_VAL) {
#if defined __WARNING__
		warning("%s: MAX_TC_VAL reached (clipping %f -> %d)!\n", name, aux, MAX_TC_VAL);
#endif
		aux = MAX_TC_VAL;
	      }
	      else if(aux < MIN_TC_VAL) {
#if defined __WARNING__
		warning("%s: MIN_TC_VAL reached (clipping %f -> %d)!\n", name, aux, MIN_TC_VAL);
#endif
		aux = MIN_TC_VAL;
	      }
	      //fprintf(stderr,"(after) aux=%f\n", aux);
#endif
	      reference_picture[NEXT][c]
		[clip(by*block_size+y+mv[NEXT][Y_FIELD][by][bx],pixels_in_y[c])]
		[clip(bx*block_size+x+mv[NEXT][X_FIELD][by][bx],pixels_in_x[c])]
		= (TC_CPU_TYPE)round(aux);

	  }	    
	}
      }
    }
  }
  // }}}
}


#include <getopt.h>

int main(int argc, char *argv[]) {
  // {{{

  // {{{ Command line support

#if defined __INFO__
  info("%s ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif /* __INFO__ */
  int block_size = 16;
  int components = COMPONENTS;
  char *even_fn = (char *)"E";
  char *frame_types_fn = (char *)"frame_types";
  char *high_fn = (char *)"H";
  char *low_fn = (char *)"L";
  char *motion_fn = (char *)"motion";
  int pictures = 33;
  int pixels_in_x[COMPONENTS] = {PIXELS_IN_X, PIXELS_IN_X/2, PIXELS_IN_X/2};
  int pixels_in_y[COMPONENTS] = {PIXELS_IN_Y, PIXELS_IN_Y/2, PIXELS_IN_Y/2};
  int pix[COMPONENTS], piy[COMPONENTS];
  int subpixel_accuracy = 0;
  float update_factor = 1.0/4; /*  This means that the high-frequency
				   subband is 4 times less important
				   than the low-frequency subband */

  
  int c;
  while(1) {

    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"block_size", required_argument, 0, 'b'},
      {"even_fn", required_argument, 0, 'e'},
      {"frame_types_fn", required_argument, 0, 'f'},
      {"high_fn", required_argument, 0, 'h'},
      {"low_fn", required_argument, 0, 'l'},
      {"motion_fn", required_argument, 0, 'm'},
      {"pictures", required_argument, 0, 'p'},
      {"pixels_in_x", required_argument, 0, 'x'},
      {"pixels_in_y", required_argument, 0, 'y'},
      {"subpixel_accuracy", required_argument, 0, 'a'},
      {"help", no_argument, 0, '?'},
      {"update_factor", required_argument, 0, 'u'},
      {0, 0, 0, 0}
    };

    int option_index = 0;

    c = getopt_long(argc, argv, "b:e:f:h:l:m:x:y:a:u:?", long_options, &option_index);

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

    case 'l':
      low_fn = optarg;
      info("%s: low_fn=%s\n", argv[0], low_fn);
      break;

    case 'm':
      motion_fn = optarg;
      info("%s: motion_fn=%s\n", argv[0], motion_fn);
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

    case 'a':
      subpixel_accuracy = atoi(optarg);
      info("%s: subpixel_accuracy=%d\n", argv[0], subpixel_accuracy);
      break;
      
    case 'u':
      update_factor = atof(optarg);
      info("%s: update_factor=%d\n", argv[0], update_factor);
      break;
      
    case '?':
#if defined __ANALYZE__
      printf("+-------------+\n");
      printf("| MCTF update |\n");
      printf("+-------------+\n");
#else /* __ANALYZE_ */
      printf("+----------------+\n");
      printf("| MCTF un_update |\n");
      printf("+----------------+\n");
#endif /* __ANALYZE__ */
      printf("\n");
#if defined __ANALYZE__
      printf("  Block-based time-domain motion updating\n");
#else /* __ANALYZE__ */
      printf("  Block-based time-domain motion updating\n");
#endif  /* __ANALYZE__ */
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-b]lock_size = size of the blocks in the motion estimation process (%d)\n", block_size);
      printf("   -[-e]ven_fn = input file with the even pictures (\"%s\")\n", even_fn);
      printf("   -[-f]rame_types_fn = output file with the frame types (\"%s\")\n", frame_types_fn);
      printf("   -[-h]igh_fn = input file with H-subband pictures (\"%s\")\n", high_fn);
      printf("   -[-l]ow_fn = output file with L-subband pictures (\"%s\")\n", low_fn);
      printf("   -[-m]otion_fn = input file with the motion fields (\"%s\")\n", motion_fn);
      printf("   -[-p]ictures = number of pictures to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x[0]);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y[0]);
      printf("   -[-]subpixel_[a]ccuracy = sub-pixel accuracy of the motion estimation (%d)\n", subpixel_accuracy);
      printf("   -[-u]pdate_factor = weight of the update step (%f)\n", update_factor);
      printf("\n");
      exit(1);
      break;

    default:
      error("%s: Unrecognized argument\n", argv[0]);
    }
  }

  // }}}

  // {{{
  
#if not defined __ANALYZE__
  int err = mkdir(even_fn, 0700);
#ifdef __DEBUG__
  if(err) {
    error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], even_fn);
    abort();
  }
#endif /* __DEBUG__ */
#endif /* __ANALYZE__ */

  // }}}

  // {{{
  
#if defined __ANALYZE__
  int err = mkdir(low_fn, 0700);
#ifdef __DEBUG__
  if(err) {
    error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], low_fn);
    abort();
  }
#endif /* __DEBUG__ */
#endif /* __ANALYZE__ */

  // }}}

  FILE *frame_types_fd; {
    // {{{

    frame_types_fd = fopen(frame_types_fn, "r");
    if(!frame_types_fd) {
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], frame_types_fn);    
      abort();
    }

    // }}}
  }

  class dwt2d <
    TC_CPU_TYPE,
    TEXTURE_INTERPOLATION_FILTER <
      TC_CPU_TYPE
      >
    > *picture_dwt = new class dwt2d <
      TC_CPU_TYPE,
    TEXTURE_INTERPOLATION_FILTER <
      TC_CPU_TYPE
      >
    >;
    picture_dwt->set_max_line_size(PIXELS_IN_X_MAX);
  
  class dwt2d <
    TC_CPU_TYPE,
    TEXTURE_INTERPOLATION_FILTER <
      TC_CPU_TYPE
      >
    > *error_dwt = new class dwt2d <
    TC_CPU_TYPE,
    TEXTURE_INTERPOLATION_FILTER <
      TC_CPU_TYPE
      >
    >;
    error_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  int blocks_in_y = pixels_in_y[0]/block_size;
  int blocks_in_x = pixels_in_x[0]/block_size;
#if defined __DEBUG__
  info("%s: blocks in Y=%d\n", argv[0], blocks_in_y);
  info("%s: blocks in X=%d\n", argv[0], blocks_in_x);
#endif /* __DEBUG__ */

  motion < MVC_TYPE > motion;

  MVC_TYPE ****mv; {
    mv = motion.alloc(blocks_in_y, blocks_in_x);
  }

  texture < TC_IO_TYPE, TC_CPU_TYPE > texture;//picture;
  //texture < TC_IO_TYPE, TC_CPU_TYPE > error;

  TC_CPU_TYPE ***reference[2] /* In (5/3) we have 2 references */; {
    // {{{

    for(int i=0; i<2; i++) {
      reference[i] = new TC_CPU_TYPE ** [COMPONENTS];
      for(int c=0; c<COMPONENTS; c++) {
	reference[i][c] = texture.alloc(pixels_in_y[0], pixels_in_x[0], 0);
      }
    }

    // }}}
  }
  TC_CPU_TYPE ***residue; {
    residue = new TC_CPU_TYPE ** [COMPONENTS];
    for (int c=0; c<COMPONENTS; c++) {
      residue[c] = texture.alloc(pixels_in_y[0], pixels_in_x[0], 0);
    }

    // }}}
  }

  piy[0] = piy[1] = piy[2] = pixels_in_y[0];
  pix[0] = pix[1] = pix[2] = pixels_in_x[0];

  // {{{ Read reference[0] from E_? 

#if defined __ANALYZE__
  info("%s: reading picture 0 (first) from \"%s\"\n", argv[0], even_fn);
#else /* __ANALYZE__ */
  info("%s: reading picture 0 (first) from \"%s\"\n", argv[0], low_fn);
#endif /* __ANALYZE__ */
  for(int c=0; c<COMPONENTS; c++) {
    texture.read_picture(reference[0][c], pixels_in_y[c], pixels_in_x[c],
#ifdef __ANALYZE__	       
		       even_fn,
#else /* __ANALYZE__ */
		       low_fn,
#endif /* __ANALYZE__ */
		       0, c
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
		       ,
		       argv[0]
#endif /* __INFO__ */
		       );
  }

  for(int y=0; y<pixels_in_y[0]/2; y++) {
    for(int x=pixels_in_x[0]/2; x<pixels_in_x[0]; x++) {
      reference[0][1][y][x] = 0;
      reference[0][2][y][x] = 0;
    }
  }
  
  for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
    for(int x=0; x<pixels_in_x[0]/2; x++) {
      reference[0][1][y][x] = 0;
      reference[0][2][y][x] = 0;
    }
  }
  
  for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
    for(int x=pixels_in_x[0]/2; x<pixels_in_x[0]; x++) {
      reference[0][1][y][x] = 0;
      reference[0][2][y][x] = 0;
    }
  }
  
  picture_dwt->synthesize(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);
  picture_dwt->synthesize(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1);
  
  // }}}

  int i;
  for(i=0; i<pictures/2; i++) {

    // {{{ Read residue de H_? 
    info("%s: reading picture %d from \"%s\"\n", argv[0], i, high_fn);
    for(int c=0; c<COMPONENTS; c++) {
      //error.read(H_fd, residue[c], pixels_in_y[c], pixels_in_x[c]);
      texture.read_picture(residue[c],
			   pixels_in_y[c], pixels_in_x[c],
			   high_fn,
			   i,
			   c
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
      // We recover the original dynamic range of the residue.
      for(int y=0; y<pixels_in_y[c]; y++) {
	for(int x=0; x<pixels_in_x[c]; x++) {
	  residue[c][y][x] -= 128;
	}
      }
    }
    
#if defined __UPDATE_STEP__
    for(int y=0; y<pixels_in_y[0]/2; y++) {
      for(int x=pixels_in_x[0]/2; x<pixels_in_x[0]; x++) {
	residue[1][y][x] = 0;
	residue[2][y][x] = 0;
      }
    }
    for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
      for(int x=0; x<pixels_in_x[0]/2; x++) {
	residue[1][y][x] = 0;
	residue[2][y][x] = 0;
      }
    }
    for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
      for(int x=pixels_in_x[0]/2; x<pixels_in_x[0]; x++) {
	residue[1][y][x] = 0;
	residue[2][y][x] = 0;
      }
    }
    error_dwt->synthesize(residue[1], pixels_in_y[0], pixels_in_x[0], 1);
    error_dwt->synthesize(residue[2], pixels_in_y[0], pixels_in_x[0], 1);
#endif /* __UPDATE_STEP__ */
    
    // }}}
    
    // {{{ Read reference[1] from E_? 
    
#ifdef __ANALYZE__ 
    info("%s: reading picture %d from \"%s\"\n", argv[0], i+1, even_fn);
#else /* __ANALYZE__ */
    info("%s: reading picture %d from \"%s\"\n", argv[0], i+1, low_fn);
#endif /* __ANALYZE__ */
    for(int c=0; c<COMPONENTS; c++) {
      texture.read_picture(reference[1][c], pixels_in_y[c], pixels_in_x[c],
#ifdef __ANALYZE__ 
			   even_fn,
#else /* __ANALYZE__ */
			   low_fn,
#endif /* __ANALYZE__ */
			   i+1, c
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    }
    
    //fprintf(stderr, "(read_1) reference[0][0][0][0]=%d reference[1][0][0][0]=%d\n", reference[0][0][0][0], reference[1][0][0][0]);

    for(int y=0; y<pixels_in_y[0]/2; y++) {
      for(int x=pixels_in_x[0]/2; x<pixels_in_x[0]; x++) {
	reference[1][1][y][x] = 0;
	reference[1][2][y][x] = 0;
      }
    }
    for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
      for(int x=0; x<pixels_in_x[0]/2; x++) {
	reference[1][1][y][x] = 0;
	reference[1][2][y][x] = 0;
      }
    }
    for(int y=pixels_in_y[0]/2; y<pixels_in_y[0]; y++) {
      for(int x=pixels_in_x[0]/2; x<pixels_in_x[0]; x++) {
	reference[1][1][y][x] = 0;
	reference[1][2][y][x] = 0;
      }
    }
    picture_dwt->synthesize(reference[1][1], pixels_in_y[0], pixels_in_x[0], 1);
    picture_dwt->synthesize(reference[1][2], pixels_in_y[0], pixels_in_x[0], 1);
    
    // }}}
    
    // {{{ Reading the motion fields

    //motion.read(motion_fd, mv, blocks_in_y, blocks_in_x);
    motion.read_field(mv, blocks_in_y, blocks_in_x, motion_fn, i
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
		      , argv[0]
#endif /* __INFO__ */
		      );
#ifdef _1_
    motion.read_component(mv[0][0],
			  blocks_in_y, blocks_in_x,
			  motion_fn,
			  i,
			  0
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    w
    motion.read_component(mv[0][1],
			  blocks_in_y, blocks_in_x,
			  motion_fn,
			  i,
			  1
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    
    motion.read_component(mv[1][0],
			  blocks_in_y, blocks_in_x,
			  motion_fn,
			  i,
			  2
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );

    motion.read_component(mv[1][1],
			  blocks_in_y, blocks_in_x,
			  motion_fn,
			  i,
			  3
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
#endif /* _1_ */
    
    // }}}
					    
    // {{{ Update
    
    if(fgetc(frame_types_fd) == 'B') {
      
      //fprintf(stderr, "(before) reference[0][0][0][0]=%d reference[1][0][0][0]=%d\n", reference[0][0][0][0], reference[1][0][0][0]);
      
      update(block_size,
	     blocks_in_y,
	     blocks_in_x,
	     COMPONENTS,
	     mv,
	     piy,
	     pix,
	     reference,
	     residue,
	     update_factor
#if defined (__INFO__) || defined (__WARNING__) || defined (__DEBUG__)
	     ,
	     argv[0]
#endif
	     );
      
      //fprintf(stderr,"(after) reference[0][0][0][0]=%d reference[1][0][0][0]=%d\n", reference[0][0][0][0], reference[1][0][0][0]);
      
    }
    
    // }}}
    
    // {{{ Write reference[0] en L_? 

#ifdef __ANALYZE__ 
    info("%s: writing picture %d to \"%s\"\n", argv[0], i, low_fn);
#else /* __ANALYZE__ */
    info("%s: writing picture %d to \"%s\"\n", argv[0], i, even_fn);
#endif /* __ANALYZE__ */
    
    picture_dwt->analyze(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);
    picture_dwt->analyze(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1);
    
    for(int c=0; c<COMPONENTS; c++) {
      texture.write_picture(reference[0][c],
			    pixels_in_y[c], pixels_in_x[c],
#ifdef __ANALYZE__
			    low_fn,
#else /* __ANALYZE__ */
			    even_fn,
#endif /* __ANALYZE__ */
			    i,
			    c
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      
    }
    
    // }}}

    // {{{ SWAP(&reference_picture[0], &reference_picture[1])

    {
      TC_CPU_TYPE ***tmp = reference[0];
      reference[0] = reference[1];
      reference[1] = tmp;
    }    
    
    // }}}
  }
  
  // {{{ Write reference[0] in L_? 
  
#ifdef __ANALYZE__ 
  info("%s: writing picture %d to \"%s\"\n", argv[0], i, low_fn);
#else /* __ANALYZE__ */
  info("%s: writing picture %d to \"%s\"\n", argv[0], i, even_fn);
#endif /* __ANALYZE__ */
  
  picture_dwt->analyze(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);
  picture_dwt->analyze(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1);
  
  for(int c=0; c<COMPONENTS; c++) {
    texture.write_picture(reference[0][c],
			  pixels_in_y[c], pixels_in_x[c],
#ifdef __ANALYZE__
			  low_fn,
#else /* __ANALYZE__ */
			  even_fn,
#endif /* __ANALYZE__ */
			  i,
			  c
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
  }
  
  // }}}
  
  // }}}
}
