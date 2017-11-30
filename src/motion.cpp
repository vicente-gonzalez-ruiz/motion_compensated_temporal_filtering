/**
 * \file motion.cpp
 * \brief Simple operation on components.
 * \author Vicente Gonzalez-Ruiz.
 * \date Last modification: 2015, January 7.
 */

/** \brief Reference to previous picture. */
#define PREV     0
/** \brief Reference to next picture. */
#define NEXT     1
/** \brief X component of a 2D point. */
#define X_FIELD  0
/** \brief Y component of a 2D point. */
#define Y_FIELD  1
/** \brief Maximum width of a component. */
#define PIXELS_IN_X_MAX 16384
/** \brief Motion vector component type. */
#define MVC_TYPE short

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>       

/** 
 * \brief A motion vector class.
 */
class motion {

public:

  /*! \brief The constructor.
   * \param y_dim Dimension 'Y' of a picture.
   * \param x_dim Dimension 'X' of a picture.
   * \returns Two motion vectors with their components.
   */
  TYPE ****alloc(int y_dim, int x_dim) {
    TYPE ****data = new TYPE *** [ 2 ]; /** Create two motion vectors for the previous and next frames. */
    for(int i=0; i<2; i++) {
      data[i] = new TYPE ** [2]; /** Create the 'X' and 'Y' components for each motion vector. */
      for(int f=0; f<2; f++) {
	data[i][f] = new TYPE * [y_dim];
	for(int y=0; y<y_dim; y++) {
	  data[i][f][y] = new TYPE [x_dim];
	}
      }
    }
    return data;
  }

  /*! \brief The destructor.
   * \param data Two motion vectors with their components.
   * \param y_dim Dimension 'Y' of a picture.
   */
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

  /*! \brief Reading motion vectors from disk to memory.
   * \param fd File.
   * \param data Two motion vectors.
   * \param y_dim Dimension 'Y' of a picture.
   * \param x_dim Dimension 'X' of a picture.
   */
  void read(FILE *fd, TYPE ****data, int y_dim, int x_dim) {
    for(int i=0; i<2; i++) {
      for(int f=0; f<2; f++) {
	for(int y=0; y<y_dim; y++) {
	  int read = fread(data[i][f][y], x_dim, sizeof(TYPE), fd);
#if defined DEBUG /** Sign and magnitude */
	  for(int x=0; x<x_dim; x++) {
	    info("%d ", data[i][f][y][x]);
	  }
#endif
	}
      }
    }
  }

  /*! \brief Writing motion vectors from memory to disk.
   * \param fd File.
   * \param data Two motion vectors.
   * \param y_dim Dimension 'Y' of a picture.
   * \param x_dim Dimension 'X' of a picture.
   */
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
