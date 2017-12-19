/**
 * \file split.cpp
 * \author Vicente Gonzalez-Ruiz.
 * \date Last modification: 2015, January 7.
 * \brief Temporal wavelet transform "Lazzy" direct (split) and reverse (merge).
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include "display.cpp"

/** \brief Texture component type. */
#define TC_TYPE unsigned char
/** \brief Number of components. */
#define COMPONENTS 3
/** \brief Number of images of the video. */
#define PICTURES 9
/** \brief Dimension 'X' of a picture. */
#define PIXELS_IN_X 352
/** \brief Dimension 'Y' of a picture. */
#define PIXELS_IN_Y 288

#include <getopt.h>

/** \brief Provides a main function which reads in parameters from the command line and a parameter file.
 * \param argc The number of command line arguments of the program.
 * \param argv The contents of the command line arguments of the program.
 * \returns Notifies proper execution.
 */
int main(int argc, char *argv[]) {

#if defined DEBUG
  info("%s: ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif

  char *even_fn=(char *)"even";
  char *low_fn=(char *)"low";
  char *odd_fn=(char *)"odd";
  int components = COMPONENTS;
  int pictures = PICTURES;
  int pixels_in_x[COMPONENTS] = {PIXELS_IN_X, PIXELS_IN_X/2, PIXELS_IN_X/2};
  int pixels_in_y[COMPONENTS] = {PIXELS_IN_Y, PIXELS_IN_Y/2, PIXELS_IN_Y/2};
  
  int c;
  while(1) {

    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"even_fn", required_argument, 0, 'e'},
      {"low_fn", required_argument, 0, 'l'},
      {"odd_fn", required_argument, 0, 'o'},
      {"pictures", required_argument, 0, 'p'},
      {"pixels_in_x", required_argument, 0, 'x'},
      {"pixels_in_y", required_argument, 0, 'y'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };
    
    int option_index = 0;
    
    c = getopt_long(argc, argv, "e:l:o:p:x:y:?", long_options, &option_index);
    
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
      
    case 'e':
      even_fn = optarg;
      break;

    case 'l':
      low_fn = optarg;
      break;

    case 'o':
      odd_fn = optarg;
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
      
    case '?':
      //      print::info("[0;32m\n");
#if defined ANALYZE
      printf("+------------+\n");
      printf("| MCTF split |\n");
      printf("+------------+\n");
#else
      printf("+------------+\n");
      printf("| MCTF merge |\n");
      printf("+------------+\n");
#endif
      printf("\n");
#if defined ANALYZE
      printf("  Direct Lazzy wavelet transform over the time domain.\n");
#else
      printf("  Inverse Lazzy wavelet transform over the time domain.\n");
#endif
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-e]ven_fn = output file with the even pictures: (\"%s\")\n", even_fn);
      printf("   -[-l]ow_fn = input file with the low pictures (\"%s\")\n", low_fn);
      printf("   -[-o]dd_fn = output file with odd pictures (\"%s\")\n", odd_fn);
      printf("   -[-p]ictures = number of images to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x[0]);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y[0]);
      printf("\n");
      exit(1);
      break;
      
    default:
      error("%s: aborting ...\n", argv[0]);
    }
  }
  
  FILE *low_fd; {
    low_fd = fopen(low_fn,
#if defined ANALYZE
		   /** During analysis "split" reads the input video
		       sequence in order to separate it into even and
		       odd images.\n During synthesis (merge) does the
		       reverse process, read the sequences of even and
		       odd images and mixing to generate the
		       reconstructed video sequence. */
			"r"
#else
		   /* During synthesis (merge) does the reverse
		      process, read the sequences of even and odd
		      images and mixing to generate the reconstructed
		      video sequence. */
			"w"
#endif
			);
    if(!low_fd) {
#if defined ANALYZE
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], low_fn);
#else
      error("%s: unable to write \"%s\" ... aborting!\n",
	    argv[0], low_fn);    
#endif
      abort();
    }
  }
  
  FILE *even_fd; {
    even_fd = fopen(even_fn,
#if defined ANALYZE
		 "w"
#else
		 "r"
#endif
		 );
    
    if(!even_fd) {
#if defined ANALYZE
      error("%s: unable to write \"%s\" ... aborting!\n",
	    argv[0], even_fn);
#else
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], even_fn);    
#endif
      abort();
    }
  }
  
  FILE *odd_fd; {
    odd_fd = fopen(odd_fn,
#if defined ANALYZE
		"w"
#else
		"r"
#endif
		);
    
    if(!odd_fd) {
#if defined ANALYZE
      error("%s: unable to write \"%s\" ... aborting!\n",
	    argv[0], odd_fn);
#else
      error("%s: unable to read \"%s\" ... aborting!\n",
	    argv[0], odd_fn);
#endif
      abort();
    }
  }
  
  TC_TYPE *line = (TC_TYPE *)malloc(pixels_in_x[0]*sizeof(TC_TYPE));
  
  /* First image (even index). */
  for(int c=0; c<COMPONENTS; c++) {
    for(int y=0; y<pixels_in_y[c]; y++) {
#if defined ANALYZE
      int r = fread(line, sizeof(TC_TYPE), pixels_in_x[c], low_fd);
#if defined DEBUG
      if(r<pixels_in_x[c]) {
	error("%s: input error (read=%d, expected=%d) in picture 0 of \"%s\". Aborting!\n",
	      argv[0], r, pixels_in_x[c], low_fn);
	abort();
      }
#endif
      fwrite(line, sizeof(TC_TYPE), pixels_in_x[c], even_fd);
#else
      int r = fread(line, sizeof(TC_TYPE), pixels_in_x[c], even_fd);
#if defined DEBUG
      if(r<pixels_in_x[c]) {
	error("%s: input error (read=%d, expected=%d) in picture 0 of \"%s\". Aborting!\n",
	      argv[0], r, pixels_in_x[c], even_fn);
	abort();
      }
#endif
      fwrite(line, sizeof(TC_TYPE), pixels_in_x[c], low_fd);
#endif
    }
  }
  
#if defined DEBUG
  info("%s: pictures=%d\n", argv[0], pictures);
#ifdef ANALYZE
  info("%s: writing picture 0 from \"%s\" to \"%s\".\n",
       argv[0], low_fn,  even_fn);
#else
  info("%s: reading picture 0 from \"%s\" to \"%s\".\n",
       argv[0], even_fn, low_fn);
#endif
#endif

  for(int i=0; i<pictures/2; i++) {
    
    /* Images odd index. */
    for(int c=0; c<COMPONENTS; c++) {
      for(int y=0; y<pixels_in_y[c]; y++) {
#if defined ANALYZE
	int r = fread(line, sizeof(TC_TYPE), pixels_in_x[c], low_fd);
#if defined DEBUG
	if(r<pixels_in_x[c]) {
	  error("%s: input error (read=%d, expected=%d) in picture %d of \"%s\". Aborting!\n",
		argv[0], r, pixels_in_x[c], i, low_fn);
	  abort();
	}
#endif
	fwrite(line, sizeof(TC_TYPE), pixels_in_x[c], odd_fd);
#else
	int r = fread(line, sizeof(TC_TYPE), pixels_in_x[c], odd_fd);
#if defined DEBUG
	if(r<pixels_in_x[c]) {
	  error("%s: input error (read=%d, expected=%d) in picture %d of \"%s\". Aborting!\n",
		argv[0], r, pixels_in_x[c], i, odd_fn);
	  abort();
	}
#endif
	fwrite(line, sizeof(TC_TYPE), pixels_in_x[c], low_fd);
#endif
      }
    }

#if defined DEBUG
#if defined ANALYZE
    info("%s: writing picture %d from \"%s\" to \"%s\".\n",
	 argv[0], i*2+1, low_fn, odd_fn);
#else
    info("%s: reading picture %d from \"%s\" to \"%s\".\n",
	 argv[0], i*2+1, odd_fn, low_fn);
#endif
#endif
    
    /* Pictures of even index. */
    for(int c=0; c<COMPONENTS; c++) {
      for(int y=0; y<pixels_in_y[c]; y++) {
#if defined ANALYZE
	int r = fread(line, sizeof(TC_TYPE), pixels_in_x[c], low_fd);
#if defined DEBUG
	if(r< pixels_in_x[c]) {
	  error("%s: input error (read=%d, expected=%d) in picture %d of \"%s\". Aborting!\n",
		argv[0], r, pixels_in_x[c], i, low_fn);
	  abort();
	}
#endif
	fwrite(line, sizeof(TC_TYPE), pixels_in_x[c], even_fd);
#else
	int r = fread(line, sizeof(TC_TYPE), pixels_in_x[c], even_fd);
#if defined DEBUG
	if(r<pixels_in_x[c]) {
	  error("%s: input error (read=%d, expected=%d) in picture %d of \"%s\". Aborting!\n",
		argv[0], r, pixels_in_x[c], i, even_fn);
	  abort();
	}
#endif
	fwrite(line, sizeof(TC_TYPE), pixels_in_x[c], low_fd);
#endif
      }
    }

#if defined DEBUG
#ifdef ANALYZE
    info("%s: writing picture %d from \"%s\" to \"%s\".\n",
	 argv[0], i*2+2, low_fn, even_fn);
#else
    info("%s: reading picture %d from \"%s\" to \"%s\".\n",
	 argv[0], i*2+2, even_fn, low_fn);
#endif
#endif
    
  }
}
