/**
 * \file dwt2d.cpp
 * \brief The 2D Discrete Wavelet Transform.
 * \author Vicente Gonzalez-Ruiz.
 * \date Last modification: 2015, January 7.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

#include <string.h>

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
/** \tparam FILTER is a class that represent a filter. */
template <typename TYPE, class FILTER>

/** \brief A class that inherits from FILTER class. */
class dwt2d: public FILTER /*, public mallok*/ {

  /*
#ifndef _DIAGRAMS_dwt2d_H
#define _DIAGRAMS_dwt2d_H
class dwt2d { public: FILTER; };
#endif
  */





private:
  /** \brief A input line of texture. */
  TYPE *in_line;
  /** \brief A output line of texture. */
  TYPE *out_line;
  
public:
  
  /** \brief The constructor. */
  dwt2d() {
    /*in_line = (TYPE *)mallok::alloc_1d(1,sizeof(TYPE));
      out_line = (TYPE *)mallok::alloc_1d(1,sizeof(TYPE));*/
    in_line = new TYPE [1];
    out_line = new TYPE [1];
  }

  /** \brief The destructor. */
  ~dwt2d() {
    /*mallok::free_1d(out_line);
      mallok::free_1d(in_line);*/
    delete out_line;
    delete in_line;
  }

  /** \brief Initialization input and output line.
   * \param max_line_size Maximum dimension of a line of textures.
   */
  void set_max_line_size(int max_line_size) {
    /*mallok::free_1d(out_line);
    mallok::free_1d(in_line);
    in_line = (TYPE *)mallok::alloc_1d(max_line_size,sizeof(TYPE));
    out_line = (TYPE *)mallok::alloc_1d(max_line_size,sizeof(TYPE));*/
    delete out_line;
    delete in_line;
    in_line = new TYPE [max_line_size];
    out_line = new TYPE [max_line_size];
  }

  /*! \brief Analyzes signal.
   * \param signal Signal.
   * \param y Number of columns.
   * \param x Number of rows.
   * \param levels Number of levels.
   */
  void analyze(TYPE **signal, int y, int x, int levels) {
    for(int lv=0;lv<levels;lv++) {
      int nx = x; x >>= 1;
      int ny = y; y >>= 1;
      if(y == 0) y = 1; /* New */
      if(x == 0) x = 1; /* New */
      
      /* Transform rows. */
      if(nx & 1) { /* Odd number of columns. */
	for(int j=0;j<ny;j++) {
	  memcpy(in_line, signal[j], nx*sizeof(TYPE));
	  this->odd_analyze(in_line, signal[j], signal[j] + x + 1, nx);
	}
      } else { /* Even number of columns. */
	for(int j=0;j<ny;j++) {
	  memcpy(in_line, signal[j], nx*sizeof(TYPE));
	  this->even_analyze(in_line, signal[j], signal[j] + x, nx);
	}
      }
      
      /* Transform columns. */
      if(ny & 1) { /* Odd number of rows. */
	for(int i=0;i<nx;i++) {
	  for(int j=0;j<ny;j++) {
	    in_line[j]=signal[j][i];
	  }
	  this->odd_analyze(in_line, out_line, out_line + y + 1, ny);
	  for(int j=0;j<ny;j++) {
	    signal[j][i]=out_line[j];
	  }
	}
      } else { /* Even number of rows. */
	for(int i=0;i<nx;i++) {
	  for(int j=0;j<ny;j++) {
	    in_line[j]=signal[j][i];
	  }
	  this->even_analyze(in_line, out_line, out_line + y, ny);
	  for(int j=0;j<ny;j++) {
	    signal[j][i]=out_line[j];
	  }
	}
      }
    }
  }


  /*! \brief Synthesize signal.
   * \param signal Signal.
   * \param y Number of columns.
   * \param x Number of rows.
   * \param levels Number of levels.
   */
  void synthesize(TYPE **signal, int y, int x, int levels) {
    int nx = x>>levels;
    int ny = y>>levels;
    
    for(int lv = levels-1; lv>=0; lv--) {
      int mx, my;
      mx = nx; nx=x>>lv;
      my = ny; ny=y>>lv;
      if(nx==0) nx=1; /* New */
      if(ny==0) ny=1; /* New */
      
      /* Transform columns. */
      if(ny & 1) { /* Number of odd rows. */
	for(int i=0;i<nx;i++) {
	  for(int j=0;j<ny;j++) {
	    in_line[j] = signal[j][i];
	  }
	  this->odd_synthesize(out_line, in_line, in_line + my + 1, ny);
	  for(int j=0;j<ny;j++) {
	    signal[j][i] = out_line[j];
	  }
	}
      } else { /* Number of even rows. */
	for(int i=0;i<nx;i++) {
	  for(int j=0;j<ny;j++) {
	    in_line[j] = signal[j][i];
	  }
	  this->even_synthesize(out_line, in_line, in_line + my, ny);
	  for(int j=0;j<ny;j++) {
	    signal[j][i] = out_line[j];
	  }
	}
      }
      
      /* Transform columns (i). */
      if(nx & 1) { /* Odd number of columns. */
	for(int j=0;j<ny;j++) {
	  memcpy(in_line, signal[j], nx*sizeof(TYPE));
	  this->odd_synthesize(signal[j], in_line, in_line + mx + 1, nx);
	}
      } else { /* Even number of columns. */
	for(int j=0;j<ny;j++) {
	  memcpy(in_line, signal[j], nx*sizeof(TYPE));
	  this->even_synthesize(signal[j], in_line, in_line + mx, nx);
	}
      }
    }
  }


};
//#endif
