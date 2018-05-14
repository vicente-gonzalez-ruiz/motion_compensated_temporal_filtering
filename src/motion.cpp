/* Bidirectional Motion Vector Fields (BMVF) stuff */

#define PREV     0 /* Backwards motion vector field */
#define NEXT     1 /* Forwards motion vector field */
#define X_FIELD  0 /* X components of a field */
#define Y_FIELD  1 /* Y components of a field */

#define MVC_TYPE short  /* MVC = Motion Vectors Components */

/* Limits */
#define PIXELS_IN_X_MAX 16384

template <typename TYPE>       
class motion {

public:

  /* Allocates a bidirectional motion vector field */
  TYPE ****alloc(int y_dim, int x_dim) {
    TYPE ****data = new TYPE *** [ 2 ];
    for(int i=0; i<2; i++) {
      data[i] = new TYPE ** [2];
      for(int f=0; f<2; f++) {
	data[i][f] = new TYPE * [y_dim];
	for(int y=0; y<y_dim; y++) {
	  data[i][f][y] = new TYPE [x_dim];
	}
      }
    }
    return data;
  }

  /* Deallocates a BMVF */
  void free(TYPE ****data, int y_dim) {
    for(int i=0; i<2; i++) {
      for(int f=0; f<2; f++) {
	for(int y=0; y<y_dim; y++) {
	  delete data[i][f][y];
	}
 	delete data[i][f];
      }
      delete data[i];
    }
  }

  /* Reads from disk a BMVF */
  void read_(FILE *fd, TYPE ****data, int y_dim, int x_dim) {
    char x[80];
    fgets(x, 80, fd); /* Magic number */
    fgets(x, 80, fd); /* rows and cols */
    fgets(x, 80, fd); /* Max value */
    for(int i=0; i<2; i++) {
      for(int f=0; f<2; f++) {
	for(int y=0; y<y_dim; y++) {
	  int read = fread(data[i][f][y], x_dim, sizeof(TYPE), fd);
#if defined __INFO__ /** Sign and magnitude */
	  for(int x=0; x<x_dim; x++) {
	    info("%d ", data[i][f][y][x]);
	  }
#endif /* __INFO__ */
	}
      }
    }
  }
  
  void read(FILE *fd, TYPE **data, int y_dim, int x_dim) {
    char x[80];
    fgets(x, 80, fd); /* Magic number */
    fgets(x, 80, fd); /* rows and cols */
    fgets(x, 80, fd); /* Max value */
    for(int y=0; y<y_dim; y++) {
      int read = fread(data[y], x_dim, sizeof(TYPE), fd);
#if defined __INFO__ /** Sign and magnitude */
      for(int x=0; x<x_dim; x++) {
	info("%d ", data[y][x]);
      }
#endif /* __INFO__ */
    }
  }

  void write(FILE *fd, TYPE **data, int y_dim, int x_dim) {
    fprintf(fd, "P5\n");
    fprintf(fd, "%d %d\n", x_dim, y_dim);
    fprintf(fd, "65535\n");
    for(int y=0; y<y_dim; y++) {
      fwrite(data[y], x_dim, sizeof(TYPE), fd);
    }
  }
  
  /* Writes to disk a BMVF */
  void write_(FILE *fd, TYPE ****data, int y_dim, int x_dim) {
    fprintf(fd, "P5\n");
    fprintf(fd, "%d %d\n", x_dim, y_dim);
    fprintf(fd, "65535\n");
    for(int i=0; i<2; i++) {
      for(int f=0; f<2; f++) {
	for(int y=0; y<y_dim; y++) {
	  fwrite(data[i][f][y], x_dim, sizeof(TYPE), fd);
	}
      }
    }
  }

  void read_component(TYPE **component,
		      int blocks_in_y,
		      int blocks_in_x,
		      char *fn,
		      int field_number,
		      int FB,
		      int YX
#if defined __INFO__
		      ,
		      char *argv[]
#endif /* __INFO__ */
		      ) {
    char fn_[80];
    sprintf(fn_, "%s/%4d_%d_%d.pgm", fn, field_number, FB, YX);
    FILE *fd  = fopen(fn_, "r");
    if(!fd) {
#if defined __INFO__
      info("%s: using \"/dev/zero\" instead of \"%s\"\n", argv[0], fn_);
#endif /* __INFO__ */
      fd = fopen("/dev/zero", "r");
    }
    motion::read(fd, component, blocks_in_y, blocks_in_x);
    fclose(fd);
  }

  void write_component(TYPE **component,
		       int blocks_in_y,
		       int blocks_in_x,
		       char *fn,
		       int image_number,
		       int FB,
		       int YX
#if defined __INFO__
		       ,
		       char *argv[]
#endif /* __INFO__ */
		       ) {
    char fn_[80];
    sprintf(fn_, "%s/%4d_%d_%d.pgm", fn, image_number, FB, YX);
    FILE *fd  = fopen(fn_, "w");
#ifdef __DEBUG__
    if(!fd) {
      error("%s: unable to create the file \"%s\" ... aborting!\n", argv[0], fn_);
      abort();
    }
#endif /* __DEBUG__ */
    motion::write(fd, component, blocks_in_y, blocks_in_x);
    fclose(fd);
  }

};

