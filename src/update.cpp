/**
 * \file update.cpp
 * \author Vicente Gonzalez-Ruiz.
 * \date Last modification: 2015, January 7.
 * \brief Update.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
//#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include "display.cpp"

/** \brief TC = Texture Component; IO = Input Output. */
#define TC_IO_TYPE unsigned char
/** \brief TC = Texture Component; CPU = Central Processing Unit. */
#define TC_CPU_TYPE short
/** \brief TEC = Texture Error Component; IO = Input Output. */
#define TEC_IO_TYPE unsigned char
/** \brief TEC = Texture Error Component; CPU = Central Processing Unit. */
#define TEC_CPU_TYPE short
/** \brief Maximum texture component value. */
#define MAX_TC_VAL 255
/** \brief Minimum texture component value. */
#define MIN_TC_VAL 0
/** \brief Filter bank type. */
#define TEXTURE_INTERPOLATION_FILTER _5_3
/** \brief Number of components. */
#define COMPONENTS 3
/** \brief Dimension 'X' of a picture. */
#define PIXELS_IN_X 352
/** \brief Dimension 'Y' of a picture. */
#define PIXELS_IN_Y 288
/* \brief If defined, shows information about the execution. */
//#define DEBUG

/** \brief Clipping.
 * \param x Element to clip.
 * \param dim Clipping dimension.
 * \returns Clipped element.
 */
int clip(int x, int dim) {
  if(x<0) return 0;
  if(x>=dim) return dim-1;
  return x;   
}

/** \brief Add the pairs images (S_ {2t}) to the prediction error. 
 * This should reduce the aliasing and therefore improve cornering 
 * R/D for maximum frame-rate. A lower frame-rate, should be improved 
 * visual quality.
 * \param block_size Size block.
 * \param blocks_in_y Dimension 'Y' of blocks in a picture.
 * \param blocks_in_x Dimension 'X' of blocks in a picture.
 * \param components Number of components.
 * \param mv Two motion vectors.
 * \param pixels_in_y Dimension 'Y' of pixels in a picture.
 * \param pixels_in_x Dimension 'X' of pixels in a picture.
 * \param reference_picture A reference picture.
 * \param residue_picture A residue picture.
 * \param update_factor Level update.\n For example, a value equal to 1/4 means that the high-frequency subband is 4 times less important than the low-frequency subband.
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
 TEC_CPU_TYPE ***residue_picture,
 float update_factor
) {
  // {{{
  for(int c=0; c<components; c++) {
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	for(int y=0; y<block_size; y++) {
	  for(int x=0; x<block_size; x++) {
	    float aux;

	      /* Updates the previous image. */
	      aux = reference_picture[PREV][c]
		[clip(by*block_size+y+mv[PREV][Y_FIELD][by][bx],pixels_in_y[c])]
		[clip(bx*block_size+x+mv[PREV][X_FIELD][by][bx],pixels_in_x[c])];

	      //aux *= update_factor /* 1<<iteration */;

	      aux
#ifdef ANALYZE
		+= 
#else
		-=
#endif
		residue_picture[c][by*block_size+y][bx*block_size+x] * update_factor;

	      //aux /= update_factor;

	      if(aux > MAX_TC_VAL) aux = MAX_TC_VAL;
	      else if(aux < MIN_TC_VAL) aux = MIN_TC_VAL;

	      reference_picture[PREV][c]
		[clip(by*block_size+y+mv[PREV][Y_FIELD][by][bx],pixels_in_y[c])]
		[clip(bx*block_size+x+mv[PREV][X_FIELD][by][bx],pixels_in_x[c])]
		= aux;
	      
	      /* Updates the afterimage. */
	      aux = reference_picture[NEXT][c]
		[clip(by*block_size+y+mv[NEXT][Y_FIELD][by][bx],pixels_in_y[c])]
		[clip(bx*block_size+x+mv[NEXT][X_FIELD][by][bx],pixels_in_x[c])];
	      
	      //aux *= update_factor;

	      aux
#ifdef ANALYZE
		+= 
#else
		-=
#endif
		residue_picture[c][by*block_size+y][bx*block_size+x] * update_factor;

	      //aux /= update_factor;
	      
	      if(aux > MAX_TC_VAL) aux = MAX_TC_VAL;
	      else if(aux < MIN_TC_VAL) aux = MIN_TC_VAL;

	      reference_picture[NEXT][c]
		[clip(by*block_size+y+mv[NEXT][Y_FIELD][by][bx],pixels_in_y[c])]
		[clip(bx*block_size+x+mv[NEXT][X_FIELD][by][bx],pixels_in_x[c])]
		= aux;

	  }	    
	}
      }
    }
  }
  // }}}
}


#include <getopt.h>

/** \brief Provides a main function which reads in parameters from the command line and a parameter file.
 * \param argc The number of command line arguments of the program.
 * \param argv The contents of the command line arguments of the program.
 * \returns Notifies proper execution.
 */
int main(int argc, char *argv[]) {
  // {{{

  // {{{ Command line support

#if defined DEBUG
  info("%s ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif
  int block_size = 16;
  int components = COMPONENTS;
  char *even_fn = (char *)"even";
  char *frame_types_fn = (char *)"frame_types";
  char *high_fn = (char *)"high";
  char *low_fn = (char *)"low";
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
      break;
      
    case 'e':
      even_fn = optarg;
      break;

    case 'f':
      frame_types_fn = optarg;
      break;

    case 'h':
      high_fn = optarg;
      break;

    case 'l':
      low_fn = optarg;
      break;

    case 'm':
      motion_fn = optarg;
      break;

    case 'p':
      pictures = atoi(optarg);
      break;
      
    case 'x':
      pixels_in_x[0] = atoi(optarg);
      pixels_in_x[1] = pixels_in_x[2] = pixels_in_x[0]/2;
      break;
      
    case 'y':
      pixels_in_y[0] = atoi(optarg);
      pixels_in_y[1] = pixels_in_y[2] = pixels_in_y[0]/2;
      break;

    case 'a':
      subpixel_accuracy = atoi(optarg);
      break;
      
    case 'u':
      update_factor = atof(optarg);
      break;
      
    case '?':
#if defined ANALYZE
      printf("+-------------+\n");
      printf("| MCTF update |\n");
      printf("+-------------+\n");
#else
      printf("+----------------+\n");
      printf("| MCTF un_update |\n");
      printf("+----------------+\n");
#endif
      printf("\n");
#if defined ANALYZE
      printf("  Block-based time-domain motion updating\n");
#else
      printf("  Block-based time-domain motion updating\n");
#endif
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-b]lock_size = size of the blocks in the motion estimation process (%d)\n", block_size);
      printf("   -[-e]ven_fn = input file with the even pictures (\"%s\")\n", even_fn);
      printf("   -[-f]rame_types_fn = output file with the frame types (\"%s\")\n", frame_types_fn);
      printf("   -[-h]igh_fn = input file with high-subband pictures (\"%s\")\n", high_fn);
      printf("   -[-l]ow_fn = output file with low-subband pictures (\"%s\")\n", low_fn);
      printf("   -[-m]otion_fn = input file with the motion fields (\"%s\")\n", motion_fn);
      printf("   -[-p]ictures = number of images to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x[0]);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y[0]);
      printf("   -[-]subpixel_[a]ccuracy = sub-pixel accuracy of the motion estimation (%d)\n", subpixel_accuracy);
      printf("   -[-u]pdate_factor = weight of the update step (%f)\n", update_factor);
      printf("\n");
      exit(1);
      break;

    default:
      error("%s: Unrecognized argument. Aborting ...\n", argv[0]);
    }
  }

  // }}}

  FILE *even_fd; {
    // {{{

    even_fd = fopen(even_fn,
#if defined ANALYZE
		    "r"
#else
		    "w"
#endif
		    );
    if(!even_fd) {
      
#if defined ANALYZE
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], even_fn);
#else
      error("%s: unable to write \"%s\" ... aborting!\n",
	    argv[0], even_fn);    
#endif
      abort();
    }

    // }}}
  }

  FILE *high_fd; {
    // {{{

    high_fd = fopen(high_fn, "r");
    if(!high_fd) {
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], high_fn);
      abort();
    }

    // }}}
  }

  FILE *low_fd; {
    // {{{

    low_fd = fopen(low_fn,
#if defined ANALYZE
		   "w"
#else
		   "r"
#endif
		   );
    if(!low_fd) {
#if defined ANALYZE
      error("%s: unable to write \"%s\" ... aborting!\n",
	    argv[0], low_fn);
#else
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], low_fn);    
#endif
      abort();
    }

    // }}}
  }


  FILE *motion_fd; {
    // {{{

    motion_fd = fopen(motion_fn, "r");
    if(!motion_fd) {
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], motion_fn);
      abort();
    }

    // }}}
  }

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


  class dwt2d < TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TC_CPU_TYPE > > *image_dwt; {
    // {{{

    image_dwt = new class dwt2d < TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TC_CPU_TYPE > >;
    image_dwt->set_max_line_size(PIXELS_IN_X_MAX);

    // }}}
  }
  
  class dwt2d < TEC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TEC_CPU_TYPE > > *error_dwt; {
    // {{{

    error_dwt = new class dwt2d < TEC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TEC_CPU_TYPE > >;
    error_dwt->set_max_line_size(PIXELS_IN_X_MAX);

    // }}}
  }

  int blocks_in_y = pixels_in_y[0]/block_size;
  int blocks_in_x = pixels_in_x[0]/block_size;
#if defined DEBUG
  info("%s: blocks in Y=%d\n", argv[0], blocks_in_y);
  info("%s: blocks in X=%d\n", argv[0], blocks_in_x);
#endif

  /** \tparam MVC_TYPE Motion vector component type. */
  motion < MVC_TYPE > motion;

  MVC_TYPE ****mv; {
    mv = motion.alloc(blocks_in_y, blocks_in_x);
  }

  texture < TC_IO_TYPE, TC_CPU_TYPE > image;
  texture < TEC_IO_TYPE, TEC_CPU_TYPE > error;

  TC_CPU_TYPE ***reference[2] /* In (5/3) we have 2 references */; {
    // {{{

    for(int i=0; i<2; i++) {
      reference[i] = new TC_CPU_TYPE ** [COMPONENTS];
      for(int c=0; c<COMPONENTS; c++) {
	reference[i][c] = image.alloc(pixels_in_y[0], pixels_in_x[0], 0);
      }
    }

    // }}}
  }
  TEC_CPU_TYPE ***residue; {
    residue = new TEC_CPU_TYPE ** [COMPONENTS];
    for (int c=0; c<COMPONENTS; c++) {
      residue[c] = error.alloc(pixels_in_y[0], pixels_in_x[0], 0);
    }

    // }}}
  }

  piy[0] = piy[1] = piy[2] = pixels_in_y[0];
  pix[0] = pix[1] = pix[2] = pixels_in_x[0];

  // {{{ Read reference[0] de even_? 

#if defined DEBUG
#ifdef ANALYZE
  info("%s: reading picture 0 from \"%s\".\n", argv[0], even_fn);
#else
  info("%s: reading picture 0 from \"%s\".\n", argv[0], low_fn);
#endif
#endif
  for(int c=0; c<COMPONENTS; c++) {
    image.read(
#ifdef ANALYZE
	       even_fd,
#else
	       low_fd,
#endif
	       reference[0][c], pixels_in_y[c], pixels_in_x[c]);
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
  image_dwt->synthesize(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);
  image_dwt->synthesize(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1);
  
  // }}}

  int i=0;
  for(i; i<pictures/2; i++) {

    // {{{ Read residue de high_? 
#if defined DEBUG
    info("%s: reading picture %d from \"%s\".\n", argv[0], i, high_fn);
#endif
    for(int c=0; c<COMPONENTS; c++) {
      error.read(high_fd, residue[c], pixels_in_y[c], pixels_in_x[c]);
      // We recover the original dynamic range of the residue.
      for(int y=0; y<pixels_in_y[c]; y++) {
	for(int x=0; x<pixels_in_x[c]; x++) {
	  residue[c][y][x] -= 128;
	}
      }
    }
    
#if defined UPDATE_STEP
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
#endif
    
    // }}}
    
    // {{{ Read reference[1] de even_? 
    
#if defined DEBUG
#ifdef ANALYZE 
    info("%s: reading picture %d from \"%s\".\n", argv[0], i, even_fn);
#else
    info("%s: reading picture %d from \"%s\".\n", argv[0], i, low_fn);
#endif
#endif
    for(int c=0; c<COMPONENTS; c++) {
      image.read(
#ifdef ANALYZE 
		 even_fd,
#else
		 low_fd,
#endif
		 reference[1][c], pixels_in_y[c], pixels_in_x[c]);
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
    image_dwt->synthesize(reference[1][1], pixels_in_y[0], pixels_in_x[0], 1);
    image_dwt->synthesize(reference[1][2], pixels_in_y[0], pixels_in_x[0], 1);
    
    // }}}
    
    // {{{ Reading the motion fields

    motion.read(motion_fd, mv, blocks_in_y, blocks_in_x);

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
	     update_factor);

      //fprintf(stderr,"(after) reference[0][0][0][0]=%d reference[1][0][0][0]=%d\n", reference[0][0][0][0], reference[1][0][0][0]);

    }
    
    // }}}
    
    // {{{ Write reference[0] en low_? 

#if defined DEBUG
#ifdef ANALYZE 
    info("%s: writing picture %d from \"%s\".\n", argv[0], i, low_fn);
#else
    info("%s: writing picture %d from \"%s\".\n", argv[0], i, even_fn);
#endif
#endif
    
    image_dwt->analyze(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);
    image_dwt->analyze(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1);
     
    for(int c=0; c<COMPONENTS; c++) {
      image.write(
#ifdef ANALYZE
		  low_fd,
#else
		  even_fd,
#endif
		  reference[0][c], pixels_in_y[c], pixels_in_x[c]);
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

  // {{{ Write reference[0] in low_? 

#if defined DEBUG
#ifdef ANALYZE 
  info("%s: writing picture %d from \"%s\".\n", argv[0], i, low_fn);
#else
  info("%s: writing picture %d from \"%s\".\n", argv[0], i, even_fn);
#endif
#endif
  
  image_dwt->analyze(reference[0][1], pixels_in_y[0], pixels_in_x[0], 1);
  image_dwt->analyze(reference[0][2], pixels_in_y[0], pixels_in_x[0], 1);
  
  for(int c=0; c<COMPONENTS; c++) {
    image.write(
#ifdef ANALYZE
		low_fd,
#else
		even_fd,
#endif
		reference[0][c], pixels_in_y[c], pixels_in_x[c]);
  }

  // }}}

  // }}}
}
