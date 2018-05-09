/* Bidirectional Motion Vector Fields (BMVF) stuff */

#define PREV     0 /* Backwards motion vector field */
#define NEXT     1 /* Forwards motion vector field */
#define X_FIELD  0 /* X components of a field */
#define Y_FIELD  1 /* Y components of a field */

/* Limits */
#define PIXELS_IN_X_MAX 16384
#define MVC_TYPE short

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
  void read(FILE *fd, TYPE ****data, int y_dim, int x_dim) {
    for(int i=0; i<2; i++) {
      for(int f=0; f<2; f++) {
	for(int y=0; y<y_dim; y++) {
	  int read = fread(data[i][f][y], x_dim, sizeof(TYPE), fd);
#if defined INFO /** Sign and magnitude */
	  for(int x=0; x<x_dim; x++) {
	    info("%d ", data[i][f][y][x]);
	  }
#endif
	}
      }
    }
  }

  /* Writes to disk a BMVF */
  void write(FILE *fd, TYPE ****data, int y_dim, int x_dim) {
    for(int i=0; i<2; i++) {
      for(int f=0; f<2; f++) {
	for(int y=0; y<y_dim; y++) {
	  fwrite(data[i][f][y], x_dim, sizeof(TYPE), fd);
	}
      }
    }
  }

};
