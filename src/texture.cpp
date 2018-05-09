/* Texture stuff */

/* Limits */
#define PIXELS_IN_X_MAX 16384

template <typename IO_TYPE, typename CPU_TYPE>
class texture {

private:
  IO_TYPE line[PIXELS_IN_X_MAX];

public:

  /* Allocate a texture image */
  CPU_TYPE **alloc(int y_dim, int x_dim, int border_dim) {
    CPU_TYPE **data = new CPU_TYPE * [ y_dim + border_dim*2 ];
    for(int y=0; y<(y_dim + border_dim*2); y++) {
      data[y] = new CPU_TYPE [ x_dim + border_dim*2 ];
    }

    for(int y=0; y<y_dim; y++) {
      data[y] += border_dim;
    }
    data += border_dim;

    return data;
  }

  /* Extends an image, copying the value of the nearest pixel (CPU_TYPE). */
  void fill_border(CPU_TYPE **data, int y_dim, int x_dim, int border_dim) {

    /** Region 1: Upper left corner. */
    for(int y=0-border_dim; y<0; y++) {
      for(int x=0-border_dim; x<0; x++) {
	data[y][x] = data[0][0];
      }
    }
    
    /** Region 2: Top. */
    for(int y=0-border_dim; y<0; y++) {
      for(int x=0; x<x_dim; x++) {
	data[y][x] = data[0][x];
      }
    }
    
    /** Region 3: Top right corner. */
    for(int y=0-border_dim; y<0; y++) {
      for(int x=x_dim; x<x_dim+border_dim; x++) {
	data[y][x] = data[0][x_dim-1];
      }
    }
    
    /** Region 4: Left Wing. */
    for(int y=0; y<y_dim; y++) {
      for(int x=0-border_dim; x<0; x++) {
	data[y][x] = data[y][0];
      }
    }
    
    /** Region 5: Right Wing. */
    for(int y=0; y<y_dim; y++) {
      for(int x=x_dim; x<x_dim+border_dim; x++) {
	data[y][x] = data[y][x_dim-1];
      }
    }
    
    /** Region 6: Lower left corner. */
    for(int y=y_dim; y<y_dim+border_dim; y++) {
      for(int x=0-border_dim; x<0; x++) {
	data[y][x] =  data[y_dim-1][x_dim-1];
      }
    }
    
    /** Region 7: Bottom. */
    for(int y=y_dim; y<y_dim+border_dim; y++) {
      for(int x=0; x<x_dim; x++) {
	data[y][x] = data[y_dim-1][x];
      }
    }
    
    /** Region 8: Bottom right corner. */
    for(int y=y_dim; y<y_dim+border_dim; y++) {
      for(int x=x_dim; x<x_dim+border_dim; x++) {
	data[y][x] = data[y_dim-1][x_dim-1];
      }
    }

  }


  /* Read an image from disk. */
  void read(FILE *fd, CPU_TYPE **img, int y_dim, int x_dim) {
    for(int y=0; y<y_dim; y++) {
      int read = fread(line, sizeof(IO_TYPE), x_dim, fd);
      for(int x=0; x<x_dim; x++) {
	img[y][x] = line[x];
      }
    }
  }

  /* Write an image to disk. */
  void write(FILE *fd, CPU_TYPE **img, int y_dim, int x_dim) {
    for(int y=0; y<y_dim; y++) {
      for(int x=0; x<x_dim; x++) {
	line[x] = img[y][x];
      }
      fwrite(line, sizeof(IO_TYPE), x_dim, fd);
    }
  }

};



#ifdef _1_

/*
template <typename TYPE>
class matrix_ops {

  void zerome(TYPE **data, int y_dim, int x_dim) {
    for(int y=0; y<y_dim; y++) {
      memset(data[y], 0, x_dim*sizeof(TYPE));
    }
  }

  void zerome(TYPE **data, int y, int x, int y_dim, int x_dim) {
    for(int _y=y; _y<y+y_dim; _y++) {
      memset(data[y] + x, 0, x_dim*sizeof(TYPE));
    }
  }

  void make_border(TYPE **data, int y_dim, int x_dim, int border_dim) {
  }

};
*/


/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/** \brief Set to 0 all data elements (without borders).
 * \param data A matrix (2D).
 * \param y_dim Dimension 'Y' of a picture.
 * \param x_dim Dimension 'X' of a picture.
*/
void zero(TYPE **data, int y_dim, int x_dim) {
  for(int y=0; y<y_dim; y++) {
    memset(data[y], 0, x_dim*sizeof(TYPE));
  }
}

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/** \brief Set to 0 all data elements (with borders).
 * \param data A matrix (2D).
 * \param y Dimension 'Y' of a border.
 * \param x Dimension 'X' of a border.
 * \param y_dim Dimension 'Y' of a picture.
 * \param x_dim Dimension 'X' of a picture.
 */
void zero(TYPE **data, int y, int x, int y_dim, int x_dim) {
  for(int _y=y; _y<y+y_dim; _y++) {
    memset(data[y] + x, 0, x_dim*sizeof(TYPE));
  }
}

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/** \brief The constructor of borders.
 * \param data A matrix (2D) with margins (border).
 * \param y_dim Dimension 'Y' of a picture.
 * \param border_dim Border size of a picture.
 */
void alloc_border(TYPE **data, int y_dim, int border_dim) {
  for(int y=0; y<y_dim; y++) {
    data[y] += border_dim;
  }
  data = border_dim;
}

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

  /** \brief Extends the image, copying the value of the nearest pixel.
   * \param data A matrix (2D) with margins (border).
   * \param y_dim Dimension 'Y' of a picture.
   * \param x_dim Dimension 'X' of a picture.
   * \param border_dim Border size of a picture.
   */
void fill_border(TYPE **data, int y_dim, int x_dim, int border_dim) {

  /* Region 1: Upper left corner. */
  for(int y=0-border_dim; y<0; y++) {
    for(int x=0-border_dim; x<0; x++) {
      data[y][x] = data[0][0];
    }
  }

  /* Region 2: Top. */
  for(int y=0-border_dim; y<0; y++) {
    for(int x=0; x<x_dim; x++) {
      data[y][x] = data[0][x];
    }
  }

  /* Region 3: Top right corner. */
  for(int y=0-border_dim; y<0; y++) {
    for(int x=x_dim; x<x_dim+border_dim; x++) {
      data[y][x] = data[0][x_size[c]-1];
    }
  }

  /* Region 4: Left Wing. */
  for(int y=0; y<y_dim; y++) {
    for(int x=0-border_dim; x<0; x++) {
      data[y][x] = data[y][0];
    }
  }

  /* Region 5: Right Wing. */
  for(int y=0; y<y_dim; y++) {
    for(int x=x_dim; x<x_dim+border_dim; x++) {
      data[y][x] = data[y][x_size[c]-1];
    }
  }

  /* Region 6: Lower left corner. */
  for(int y=y_dim; y<y_dim+border_dim; y++) {
    for(int x=0-border_dim; x<0; x++) {
      data[y][x] =  data[y_size[c]-1][x_size[c]-1];
    }
  }

  /* Region 7: Bottom. */
  for(int y=y_dim; y<y_dim+border_dim; y++) {
    for(int x=0; x<x_dim; x++) {
      data[y][x] = data[y_size[c]-1][x];
    }
  }

  /* Region 8: Bottom right corner. */
  for(int y=y_dim; y<y_dim+border_dim; y++) {
    for(int x=x_dim; x<x_dim+border_dim; x++) {
      data[y][x] = data[y_size[c]-1][x_size[c]-1];
    }
  }
}

// Separar cada función, en principio diferente, en ficheros
// distintos.

#endif
