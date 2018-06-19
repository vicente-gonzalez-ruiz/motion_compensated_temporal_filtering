/* Removes interlevel redundancy between motion subbands. If in the
   subband S a motion vector is V, in the subband S+1 the motion
   vector should be V/2.

       PREV
   +----------+
   |  ........|--+
   |  .       |  |
   |  .  X    |  | Reference Subband S+1
   |  .       |  |
   +----------+  |
      +----------+
          NEXT

       PREV             PREV
   +----------+     +----------+
   |  ........|--+  |  ........|--+
   |  .       |  |  |  .       |  |
   |  . X/2   |  |  |  . X/2   |  | Predicted (Residue) Subband S
   |  .       |  |  |  .       |  |
   +----------+  |  +----------+  |
      +----------+     +----------+
          NEXT             NEXT

   
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <sys/stat.h>
#include <sys/types.h>

//#define __INFO__
//#define __DEBUG__
#define __WARNING__

#include "display.cpp"
#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"

/*
  Inputs: a predicted field, a reference field.
  Outputs: a residue field.
*/
void decorrelate_field
(
 int blocks_in_x,
 int blocks_in_y,
 MVC_TYPE ****predicted, /* The motion vector field to decorrelate */
 MVC_TYPE ****reference, /* The reference motion vector field */
 MVC_TYPE ****residue    /* The decorrelated motion vector field */
 ) {
  for (int y=0; y<blocks_in_y; y++) {
    for (int x=0; x<blocks_in_x; x++) {
#if defined __ANALYZE__
      /* Decorrelation. */
      residue[PREV][X_FIELD][y][x] = predicted[PREV][X_FIELD][y][x] - reference[PREV][X_FIELD][y][x]/2;
      residue[PREV][Y_FIELD][y][x] = predicted[PREV][Y_FIELD][y][x] - reference[PREV][Y_FIELD][y][x]/2;
      residue[NEXT][X_FIELD][y][x] = predicted[NEXT][X_FIELD][y][x] - reference[NEXT][X_FIELD][y][x]/2;
      residue[NEXT][Y_FIELD][y][x] = predicted[NEXT][Y_FIELD][y][x] - reference[NEXT][Y_FIELD][y][x]/2;
      /* No decorrelation.
      residue[PREV][X_FIELD][y][x] = predicted[PREV][X_FIELD][y][x];
      residue[PREV][Y_FIELD][y][x] = predicted[PREV][Y_FIELD][y][x];
      residue[NEXT][X_FIELD][y][x] = predicted[NEXT][X_FIELD][y][x];
      residue[NEXT][Y_FIELD][y][x] = predicted[NEXT][Y_FIELD][y][x];
      */
#else /* __ANALYZE__ */
      /* Correlation. */
      predicted[PREV][X_FIELD][y][x] = residue[PREV][X_FIELD][y][x] + reference[PREV][X_FIELD][y][x]/2;
      predicted[PREV][Y_FIELD][y][x] = residue[PREV][Y_FIELD][y][x] + reference[PREV][Y_FIELD][y][x]/2;
      predicted[NEXT][X_FIELD][y][x] = residue[NEXT][X_FIELD][y][x] + reference[NEXT][X_FIELD][y][x]/2;
      predicted[NEXT][Y_FIELD][y][x] = residue[NEXT][Y_FIELD][y][x] + reference[NEXT][Y_FIELD][y][x]/2;
      /* No correlation.
      predicted[PREV][X_FIELD][y][x] = residue[PREV][X_FIELD][y][x];
      predicted[PREV][Y_FIELD][y][x] = residue[PREV][Y_FIELD][y][x];
      predicted[NEXT][X_FIELD][y][x] = residue[NEXT][X_FIELD][y][x];
      predicted[NEXT][Y_FIELD][y][x] = residue[NEXT][Y_FIELD][y][x];
      */
#endif /* __ANALYZE__ */
    }
  }
}

#include <getopt.h>

int main(int argc, char *argv[]) {

#if defined DEBUG
  info("%s: ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif

  int blocks_in_x = 11;
  int blocks_in_y = 9;
  int fields_in_reference = 1;
  char *predicted_fn = (char *)"/dev/zero";
  char *reference_fn = (char *)"/dev/zero";
  char *residue_fn = (char *)"/dev/zero";

  int c;
  while(1) {
  
    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"blocks_in_x", required_argument, 0, 'x'},
      {"blocks_in_y", required_argument, 0, 'y'},
      {"fields_in_reference", required_argument, 0, 'f'},
      {"predicted_fn", required_argument, 0, 'p'},
      {"reference_fn", required_argument, 0, 'r'},
      {"residue_fn", required_argument, 0, 'e'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };
    
    int option_index = 0;
    
    c = getopt_long(argc, argv, "x:y:f:p:r:e:?", long_options, &option_index);
    
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
      
    case 'x':
      blocks_in_x = atoi(optarg);
      info("%s: blocks_in_x=%d\n", argv[0], blocks_in_x);
      break;
      
    case 'y':
      blocks_in_y = atoi(optarg);
      info("%s: blocks_in_y=%d\n", argv[0], blocks_in_y);
      break;

    case 'f':
      fields_in_reference = atoi(optarg);
      info("%s: fields_in_reference=%d\n", argv[0], fields_in_reference);
      break;

    case 'p':
      predicted_fn = optarg;
      info("%s: predicted_fn = \"%s\"\n", argv[0], predicted_fn);
      break;

    case 'r':
      reference_fn = optarg;
      info("%s: reference_fn = \"%s\"\n", argv[0], reference_fn);
      break;

    case 'e':
      residue_fn = optarg;
      info("%s: residue_fn = \"%s\"\n", argv[0], residue_fn);
      break;
      
    case '?':
#if defined __ANALYZE__
      printf("+------------------------------------+\n");
      printf("| MCTF interlevel_motion_decorrelate |\n");
      printf("+------------------------------------+\n");
#else /* __ANALYZE__ */
      printf("+----------------------------------+\n");
      printf("| MCTF interlevel_motion_correlate |\n");
      printf("+----------------------------------+\n");
#endif /* __ANALYZE__ */
      printf("\n");
#if defined __ANALYZE__
      printf("  Interlevel decorrelation of the motion information\n");
#else /* __ANALYZE__ */
      printf("  Interlevel correlation of the motion information.\n");
#endif /* __ANALYZE__ */
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-]blocks_in_[x]=number of blocks in the X direction (%d)\n", blocks_in_x);
      printf("   -[-]blocks_in_[y]=number of blocks in the Y direction (%d)\n", blocks_in_y);
      printf("   -[-f]ields_in_reference=number of motion fields in the reference sequence of motion fields(%d)\n", fields_in_reference);
      printf("   -[-p]redicted=name of the file with the predicted fields(\"%s\")\n", predicted_fn);
      printf("   -[-r]eference=name of the file with the reference fields\"%s\"\n", reference_fn);
      printf("   -[-]r[e]sidue=name of the file with the residues(\"%s\")\n", residue_fn);
      printf("\n");
      exit(1);
      break;
      
    default:
      error("%s: Unrecognized argument\n", argv[0]);
      abort();
    }
  }

#ifdef _1_
#if not defined __ANALYZE__
  {
    int err = mkdir(predicted_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], predicted_fn);
      abort();
    }
#endif /* __DEBUG__ */
  }
#endif /* __ANALYZE__ */
#endif /* _1_ */

#ifdef _1_
#if defined __ANALYZE__
  {
    int err = mkdir(residue_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], residue_fn);
      abort();
    }
#endif /* __DEBUG__ */
  }
#endif /* __ANALYZE__ */
#endif /* _1_ */

  motion < MVC_TYPE > motion;
  MVC_TYPE ****predicted = motion.alloc(blocks_in_y, blocks_in_x);
  MVC_TYPE ****reference = motion.alloc(blocks_in_y, blocks_in_x);
  MVC_TYPE ****residue = motion.alloc(blocks_in_y, blocks_in_x);
  
  for(int i=0; i<fields_in_reference; i++) {
    
    info("%s: reading reference field %d\n", argv[0], i);
    // {{{ Read reference

    //motion.read(reference_fd, reference, blocks_in_y, blocks_in_x);
    motion.read_field(reference, blocks_in_y, blocks_in_x, reference_fn, i
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
		      ,	argv[0]
#endif /* __INFO__ */
		      );
#ifdef _1_
    // {{{ reference[0][0] <- reference
    motion.read_component(reference[0][0],
			  blocks_in_y, blocks_in_x,
			  reference_fn,
			  i,
			  0
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ reference[0][1] <- reference
    motion.read_component(reference[0][1],
			  blocks_in_y, blocks_in_x,
			  reference_fn,
			  i,
			  1
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ reference[1][0] <- reference
    motion.read_component(reference[1][0],
			  blocks_in_y, blocks_in_x,
			  reference_fn,
			  i,
			  2
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ reference[1][1] <- reference
    motion.read_component(reference[1][1],
			  blocks_in_y, blocks_in_x,
			  reference_fn,
			  i,
			  3
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
#endif /* _1_ */
    // }}}

    /** De/correlate two consecutive motion fields using the same
	reference. */
    for(int p=0; p<2; p++) {
      
#if defined __ANALYZE__
      info("%s: reading predicted field %d\n", argv[0], 2*i+p);
      // {{{ Read predicted
      //motion.read(predicted_fd, predicted, blocks_in_y, blocks_in_x);
      motion.read_field(predicted, blocks_in_y, blocks_in_x, predicted_fn, 2*i+p
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			, argv[0]
#endif /* __INFO__ */
			);
#ifdef _1_
      // {{{ predicted[0][0] <- predicted
      motion.read_component(predicted[0][0],
			    blocks_in_y, blocks_in_x,
			    predicted_fn,
			    i*2+p,
			    0
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );

      // }}}
      // {{{ predicted[0][1] <- predicted
      motion.read_component(predicted[0][1],
			    blocks_in_y, blocks_in_x,
			    predicted_fn,
			    i*2+p,
			    1
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
      // {{{ predicted[1][0] <- predicted
      motion.read_component(predicted[1][0],
			    blocks_in_y, blocks_in_x,
			    predicted_fn,
			    i*2+p,
			    2
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
      // {{{ predicted[1][1] <- predicted
      motion.read_component(predicted[1][1],
			    blocks_in_y, blocks_in_x,
			    predicted_fn,
			    i*2+p,
			    3
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
#endif /* _1_ */

      // }}}
#else /* __ANALYZE__ */
      info("%s: reading residue field %d\n", argv[0], 2*i+p);
      // {{{ Read residue
      //motion.read(residue_fd, residue, blocks_in_y, blocks_in_x);
      motion.read_field(residue, blocks_in_y, blocks_in_x, residue_fn, i*2+p
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
		       , argv[0]
#endif /* __INFO__ */
		       );

#ifdef _1_
      // {{{ residue[0][0] <- residue
      motion.read_component(residue[0][0],
			    blocks_in_y, blocks_in_x,
			    residue_fn,
			    i*2+1,
			    0
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
      // {{{ residue[0][1] <- residue
      motion.read_component(residue[0][1],
			    blocks_in_y, blocks_in_x,
			    residue_fn,
			    i*2+p,
			    1
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
      // {{{ residue[1][0] <- residue
      motion.read_component(residue[1][0],
			    blocks_in_y, blocks_in_x,
			    residue_fn,
			    i*2+p,
			    2
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
      // {{{ residue[1][1] <- residue
      motion.read_component(residue[1][1],
			    blocks_in_y, blocks_in_x,
			    residue_fn,
			    i*2+p,
			    3
#if defined __INFO__
			    ,
			    argv[0]
#endif /* __INFO__ */
			    );
      // }}}
#endif /* _1_ */
      // }}}
#endif /* __ANALYZE__ */

      decorrelate_field
	(blocks_in_x,
	 blocks_in_y,
	 predicted,
	 reference,
	 residue);
      
#if defined __ANALYZE__
      info("%s: writing residue field %d\n", argv[0], 2*i+p);
      // {{{ Write residue 
      //motion.write(residue_fd, residue, blocks_in_y, blocks_in_x);
      motion.write_field(residue, blocks_in_y, blocks_in_x, residue_fn, 2*i+p
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			 , argv[0]
#endif /* __INFO__ */
			 );
#ifdef _1_
      // {{{ residue[0][0] -> residue
      motion.write_component(residue[0][0],
			     blocks_in_y, blocks_in_x,
			     residue_fn,
			     i*2+p,
			     0
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ residue[0][1] -> residue
      motion.write_component(residue[0][1],
			     blocks_in_y, blocks_in_x,
			     residue_fn,
			     i*2+p,
			     1
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ residue[1][0] -> residue
      motion.write_component(residue[1][0],
			     blocks_in_y, blocks_in_x,
			     residue_fn,
			     i*2+p,
			     2
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ residue[1][1] -> residue
      motion.write_component(residue[1][1],
			     blocks_in_y, blocks_in_x,
			     residue_fn,
			     i*2+p,
			     3
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
#endif /* _1_ */

      // }}}
#else /* __ANALYZE__ */
      info("%s: writing predicted field %d\n", argv[0], 2*i+p);
      // {{{ Write predicted
      //motion.write(predicted_fd, predicted, blocks_in_y, blocks_in_x);
      motion.write_field(predicted, blocks_in_y, blocks_in_x, predicted_fn, 2*i+p
#if defined (__INFO__) || defined (__DEBUG__) || defined (__WARNING__)
			 , argv[0]
#endif /* __INFO__ */
			 );
#ifdef _1_
      // {{{ predicted[0][0] -> predicted
      motion.write_component(predicted[0][0],
			     blocks_in_y, blocks_in_x,
			     predicted_fn,
			     i*2+p,
			     0
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ predicted[0][1] -> predicted
      motion.write_component(predicted[0][1],
			     blocks_in_y, blocks_in_x,
			     predicted_fn,
			     i*2+p,
			     1
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ predicted[1][0] -> predicted
      motion.write_component(predicted[1][0],
			     blocks_in_y, blocks_in_x,
			     predicted_fn,
			     i*2+p,
			     2
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
      // {{{ predicted[1][1] -> predicted
      motion.write_component(predicted[1][1],
			     blocks_in_y, blocks_in_x,
			     predicted_fn,
			     i*2+p,
			     3
#if defined __INFO__
			     ,
			     argv[0]
#endif /* __INFO__ */
			     );
      // }}}
#endif /* _1_ */

      // }}}
#endif /* __ANALYZE__ */
      
    }
  }
}
