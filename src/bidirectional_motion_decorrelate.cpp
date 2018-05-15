/* Bidirectionan motion vectors decorrelation.

   In most sequences, the movement is almos linear (at least in short
   intervals of time), so, the backward vector can be used to predict
   the forward one, simply by changing the sign.
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <sys/stat.h>
#include <sys/types.h>

#define __INFO__
#define __DEBUG__
#define __WARNING__

#include "display.cpp"
#include "motion.cpp"

void decorrelate_field
(
 int blocks_in_x,
 int blocks_in_y,
 MVC_TYPE ****field
 ) {
  for (int y=0; y<blocks_in_y; y++) {
    for (int x=0; x<blocks_in_x; x++) {
#if defined __ANALYZE__
      /* Decorrelation.*/
      field[NEXT][X_FIELD][y][x] -= field[PREV][X_FIELD][y][x];
      field[NEXT][Y_FIELD][y][x] -= field[PREV][Y_FIELD][y][x];
      /* No decorrelation.
      field[NEXT][X_FIELD][y][x] -= 0;
      field[NEXT][Y_FIELD][y][x] -= 0;
      */
#else /* __ANALYZE__ */
      /* Correlation.*/
      field[NEXT][X_FIELD][y][x] += field[PREV][X_FIELD][y][x];
      field[NEXT][Y_FIELD][y][x] += field[PREV][Y_FIELD][y][x];
      /* No correlation.
      field[NEXT][X_FIELD][y][x] += 0;
      field[NEXT][Y_FIELD][y][x] += 0;
      */
#endif /* __ANALYZE__ */
    }
  }
}

#include <getopt.h>

int main(int argc, char *argv[]) {

#if defined __INFO__
  info("%s: ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif /* __INFO__ */

  int blocks_in_x = 11;                  /* blocks_in_x Dimension 'X' of blocks in a picture. */
  int blocks_in_y = 9;                   /* blocks_in_y Dimension 'Y' of blocks in a picture. */
  int fields = 1;                        /* field A field. */
  char *input_fn = (char *)"/dev/zero";  /* input_fn Input file. */
  char *output_fn = (char *)"/dev/zero"; /* input_fn Input file. */

  int c;
  while(1) {
    
    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"blocks_in_x", required_argument, 0, 'x'},
      {"blocks_in_y", required_argument, 0, 'y'},
      {"fields", required_argument, 0, 'f'},
      {"input_fn", required_argument, 0, 'i'},
      {"output_fn", required_argument, 0, 'o'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };
    
    int option_index = 0;
    
    c = getopt_long(argc, argv, "x:y:f:i:o:?", long_options, &option_index);
    
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
      fields = atoi(optarg);
      info("%s: fields=%d\n", argv[0], fields);
      break;
      
    case 'i':
      input_fn = optarg;
      info("%s: input = \"%s\"\n", argv[0], input_fn);
      break;

    case 'o':
      output_fn = optarg;
      info("%s: output = \"%s\"\n", argv[0], output_fn);
     break;

    case '?':
#if defined __ANALYZE__
      printf("+---------------------------------------+\n");
      printf("| MCTF bidirectional_motion_decorrelate |\n");
      printf("+---------------------------------------+\n");
#else /* __ANALYZE__ */
      printf("+-------------------------------------+\n");
      printf("| MCTF bidirectional_motion_correlate |\n");
      printf("+-------------------------------------+\n");
#endif /* __ANALYZE__ */
      printf("\n");
#if defined __ANALYZE__
      printf("  Bidirectional decorrelation of the motion information.\n");
#else /* __ANALYZE__ */
      printf("  Bidirectional correlation of the motion information.\n");
#endif /* __ANALYZE__ */
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-]blocks_in_[x]=number of blocks in the X direction (%d)\n", blocks_in_x);
      printf("   -[-]blocks_in_[y]=number of blocks in the Y direction (%d)\n", blocks_in_y);
      printf("   -[-f]ields=number of fields in input (%d)\n", fields);
      printf("   -[-i]nput=name of the file with the input fields (\"%s\")\n", input_fn);
      printf("   -[-o]utput=name of the file with the output fields (\"%s\")\n", output_fn);
      printf("\n");
      exit(1);
      break;

    default:
      error("%s: Unrecognized argument.\n", argv[0]);
      abort();
    }
  }

  {
    int err = mkdir(output_fn, 0700);
#ifdef __DEBUG__
    if(err) {
      error("%s: \"%s\" cannot be created ... aborting!\n", argv[0], output_fn);
      abort();
    }
#endif /* __DEBUG__ */
  }
  
  motion < MVC_TYPE > motion;
  MVC_TYPE ****field = motion.alloc(blocks_in_y, blocks_in_x);
  
  for(int i=0; i<fields; i++) {
    
    info("%s: reading field %d\n", argv[0], i);
    //motion.read(input_fd, field, blocks_in_y, blocks_in_x);
    motion.read_field(field, blocks_in_y, blocks_in_x, input_fn, i
#if defined __INFO__
		      , argv[0]
#endif /* __INFO__ */
		      );
			  
#ifdef _1_
    // {{{ field[0][0] <- input
    motion.read_component(field[0][0],
			  blocks_in_y, blocks_in_x,
			  input_fn,
			  i,
			  0
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ field[0][1] <- input
    motion.read_component(field[0][1],
			  blocks_in_y, blocks_in_x,
			  input_fn,
			  i,
			  1
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ field[1][0] <- input
    motion.read_component(field[1][0],
			  blocks_in_y, blocks_in_x,
			  input_fn,
			  i,
			  2
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ field[1][1] <- input
    motion.read_component(field[1][1],
			  blocks_in_y, blocks_in_x,
			  input_fn,
			  i,
			  3
#if defined __INFO__
			  ,
			  argv[0]
#endif /* __INFO__ */
			  );
    // }}}
#endif / _1_ */
    
    decorrelate_field
      (blocks_in_x,
       blocks_in_y,
       field);

    info("%s: writing field %d\n", argv[0], i);
    //motion.write(output_fd, field, blocks_in_y, blocks_in_x);
#ifdef _1_
    // {{{ field[0][0] -> output
    motion.write_component(field[0][0],
			   blocks_in_y, blocks_in_x,
			   output_fn,
			   i,
			   0
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    // }}}
    // {{{ 
    motion.write_component(field[0][1],
			   blocks_in_y, blocks_in_x,
			   output_fn,
			   i,
			   1
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ field[1][0] -> output
    motion.write_component(field[1][0],
			   blocks_in_y, blocks_in_x,
			   output_fn,
			   i,
			   2
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			  );
    // }}}
    // {{{ field[1][1] -> output
    motion.write_component(field[1][1],
			   blocks_in_y, blocks_in_x,
			   output_fn,
			   i,
			   3
#if defined __INFO__
			   ,
			   argv[0]
#endif /* __INFO__ */
			   );
    // }}}
#endif /* _1_ */
  }
}
