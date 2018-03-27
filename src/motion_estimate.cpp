/**
 * \file motion_estimate.cpp
 * \author Vicente Gonzalez-Ruiz.
 * \date Last modification: 2015, January 7.
 * \brief Motion estimation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <string.h>
#include "display.cpp"
#include "Haar.cpp"
#include "5_3.cpp"
//#include "13_7.cpp"
//#include "SP.cpp"
#include "dwt2d.cpp"
#include "texture.cpp"
#include "motion.cpp"
#include <limits>

/** \brief Trigger for if_defined.\n
 * Greatly accelerates the process of motion estimation, although the search is sub-optimal.\n
 * Estimates the motion of a block from the reference image to the predicted image, 
 * use a search area of +-1. Uses a spiral search, ending at (0,0).\n
 * The movement is estimated from a search point determined by the current value of 
 * the motion vectors.\n For example, if the input value of a motion vector is (-1,0), 
 * the spots are checked (-2,-1), (-2,0), (-2,1), (-1,-1), (-1,0), (-1,1), (0,-1), 
 * (0,0) and (0,1). */
#define FAST_SEARCH
/** \brief TC = Texture Component; IO = Input Output. */
#define TC_IO_TYPE unsigned char
/** \brief TC = Texture Component; CPU = Central Processing Unit. */
#define TC_CPU_TYPE short
/** \brief Filter bank type applied to textures. */
#define TEXTURE_INTERPOLATION_FILTER _5_3
/** \brief Filter bank type applied to motion vectors. */
#define MOTION_INTERPOLATION_FILTER Haar
/* \brief Motion vectors components. */
//#define MVC_TYPE char
/** \brief MVC = Motion Vectors Components; IO = Input Output. */
#define MVC_IO_TYPE short
/** \brief MVC = Motion Vectors Components; CPU = Central Processing Unit. */
#define MVC_CPU_TYPE short
/* \brief Trigger for if_defined.\n
 * Displays real time information about running. */
//#define DEBUG
/* \brief Trigger for if_defined.\n
 * Outputs the motion vectors to the stdout. */
//#define GNUPLOT
/* \brief Trigger for if_defined.\n
 * Set to zero the motion vectors. */
//#define CLEAR_MVS

#if defined FAST_SEARCH

/** \brief Motion estimation for blocks of variable size using only luminance.\n
 * Each block generates two motion vectors, one referring to the previous image and one to the next.\n
 * It plans to use a quad-tree to encode the location and size of the blocks and the blocks can be any size.
 * \param mv [PREV|NEXT][Y|X][coor_y][coor_x].
 * \param ref [PREV|NEXT][coor_y][coor_x]
 * \param pred [coor_y][coor_x]
 * \param luby Coordinate upper-left block, for the Y axis.
 * \param lubx Coordinate upper-left block, for the X axis.
 * \param rbby Coordinate lower-right block, for the Y axis.
 * \param rbbx Coordinate lower-right block, for the X axis.
 * \param by Vector coordinate in the field of movement, for the Y axis.
 * \param bx Vector coordinate in the field of movement, for the X axis.
 */
void local_me_for_block
(
 MVC_CPU_TYPE ****mv,/* [PREV|NEXT][Y|X][coor_y][coor_x] */
 TC_CPU_TYPE ***ref, /* [PREV|NEXT][coor_y][coor_x] */
 TC_CPU_TYPE **pred, /* [coor_y][coor_x] */
 int luby, int lubx, /* Coordinate upper-left block. */
 int rbby, int rbbx, /* Coordinate lower-right block. */
 int by, int bx      /* Vector coordinate in the field of movement. */
 ) {

  int min_error[2];
  int vy[2], vx[2];

  MVC_CPU_TYPE mv_prev_y_by_bx = mv[PREV][Y_FIELD][by][bx];
  MVC_CPU_TYPE mv_prev_x_by_bx = mv[PREV][X_FIELD][by][bx];
  MVC_CPU_TYPE mv_next_y_by_bx = mv[NEXT][Y_FIELD][by][bx];
  MVC_CPU_TYPE mv_next_x_by_bx = mv[NEXT][X_FIELD][by][bx];

  /** \brief For updating vectors is needed calculating the error vectors. */
#define COMPUTE_ERRORS(_y,_x)						\
  MVC_CPU_TYPE y[2] = {mv_prev_y_by_bx + _y, mv_next_y_by_bx - _y};	\
  MVC_CPU_TYPE x[2] = {mv_prev_x_by_bx + _x, mv_next_x_by_bx - _x};	\
  int errorPrev[block_size][block_size];  				\
  int errorNext[block_size][block_size];				\
                                                                        \
  long int contadorErrorPrediccionPrev[256];				\
  long int contadorErrorPrediccionNext[256];				\
  long int numTotalPixeles = block_size*block_size;			\
  int errorP = 0;							\
  int numVecesAparecido = 0;						\		
  double p_s = 0.0;							\
  double i_s = 0.0;							\
  double entropiaErrorPrev = 0.0;					\
  double entropiaErrorNext = 0.0; 					\
  double minEE_prev = std::numeric_limits<double>::max();		\
  double minEE_next = std::numeric_limits<double>::max();		\
                                                                        \
  /** Inicializo a 0 las matrices de errores de prediccion */ 		\
  for(int y=0; y<block_size; y++) {					\
    for(int x=0; x<block_size; x++) {					\
      errorPrev[y][x]=0;						\
      errorNext[y][x]=0;						\
    }									\
  }  									\
                                                                        \
  /** Calculo tanto el error previo como el error posterior */
  for(int py=luby; py<rbby; py++) {					\
    TC_CPU_TYPE *pred_py = pred[py];					\
    for(int px=lubx; px<rbbx; px++) {					\
      errorPrev[py-luby][px-lubx] =					\
	  (pred_py[px] - ref[PREV][py + y[PREV]][px + x[PREV]]);	\
      errorNext[py-luby][px-lubx] =					\
	  (pred_py[px] - ref[NEXT][py + y[NEXT]][px + x[NEXT]]);	\
    }									\
  }									\
                                                                        \
  /** Calculo la probabilad de error de cada pixel
  para la matriz que alberga los errores anteriores */                  \                                               
  for(int y=0; y<block_size; y++) {					\
    for(int x=0; x<block_size; x++) {					\
      int errorP = errorPrev[y][x] + 128;				\
      contadorErrorPrediccionPrev[errorP] = 				\
        contadorErrorPrediccionPrev[errorP]++;				\
    }									\
  }									\
                                                                        \
  /** Calculo la probabilad de error de cada pixel
  para la matriz que alberga los errores posteriores */                 \  
  for(int y=0; y<block_size; y++) {					\
    for(int x=0; x<block_size; x++) {					\
      int errorN = errorNext[y][x] + 128;				\
      contadorErrorPrediccionNext[errorN] = 				\
        contadorErrorPrediccionNext[errorN]++;				\
    }									\
  }									\
                                                                        \
  /** Calculo la entropia del error de prediccion 
  quedandome ademas con la mejor como UPDATE-VECTORS*/			\
  for(int y=0; y<block_size; y++) {					\
    for(int x=0; x<block_size; x++) {					\
      errorP = errorPrev[y][x] + 128;					\
      numVecesAparecido = contadorErrorPrediccionesPrev[errorP];	\
      p_s = numVecesAparecido/numTotalPixeles;				\
      i_s = -log2(p_s);							\
      entropiaErrorPrev += p_s * i_s;					\
      if(entropiaErrorPrev <= minEE_prev) {				\
        minEE_prev = entropiaErrorPrev;					\
      }									\
    }									\
  }									\
  entropiaErrorPrev = entropiaErrorPrev/numTotalPixeles;		\
                                                                        \
  /** Lo mismo para la entropia de la matriz Next */			\
    
#define MSE(_y,_x)						\
  MVC_CPU_TYPE y[2] = {mv_prev_y_by_bx + _y, mv_next_y_by_bx - _y};	\
  MVC_CPU_TYPE x[2] = {mv_prev_x_by_bx + _x, mv_next_x_by_bx - _x};	\
  int error[2] = {0, 0};						\
									\
  for(int py=luby; py<rbby; py++) {					\
    TC_CPU_TYPE *pred_py = pred[py];					\
      for(int px=lubx; px<rbbx; px++) {					\
	error[PREV] += 						\
	  (pred_py[px] - ref[PREV][py + y[PREV]][px + x[PREV]]) * (pred_py[px] - ref[PREV][py + y[PREV]][px + x[PREV]]);	\
	error[NEXT] += 						\
	  (pred_py[px] - ref[NEXT][py + y[NEXT]][px + x[NEXT]]) * (pred_py[px] - ref[NEXT][py + y[NEXT]][px + x[NEXT]]);	\
      }									\
    }									\    

  /** \brief The calculations needed to perform the upgrade mainly consist of:\n\n
   * Minimum mistake for all checked positions:\n
   * - min_error [PREV] refers to the previous image.\n
   * - min_error [NEXT] to the next. */
  /** \brief Best motion vector, calculated in each direction:\n

   * - (vy [PREV], vx [PREV]) points to the previous image.\n
   * - (vy [NEXT], vx [NEXT]) to the next image. */
#define UPDATE_VECTORS							\
  if(error[PREV] <= min_error[PREV]) {					\
    vy[PREV] = y[PREV];							\
    vx[PREV] = x[PREV];							\
    min_error[PREV] = error[PREV];					\
  }									\
									\
  if(error[NEXT] <= min_error[NEXT]) {					\
    vy[NEXT] = y[NEXT];							\
    vx[NEXT] = x[NEXT];							\
    min_error[NEXT] = error[NEXT];					\
  }

  /* 1. Position (-1,-1). Up - Left. */ {
    COMPUTE_ERRORS(-1,-1);
    
    min_error[PREV] = error[PREV];
    vy[PREV] = y[PREV];
    vx[PREV] = x[PREV];

    min_error[NEXT] = error[NEXT];
    vy[NEXT] = y[NEXT];
    vx[NEXT] = x[NEXT];
  }
  
  /* 1. Position (-1,-1). Up - Left. MSE*/ {
    MSE(-1,-1);
    
    min_error[PREV] = error[PREV];
    vy[PREV] = y[PREV];
    vx[PREV] = x[PREV];

    min_error[NEXT] = error[NEXT];
    vy[NEXT] = y[NEXT];
    vx[NEXT] = x[NEXT];
  }  
  
  /* 2. Position (-1,1). Up - Right. */ {
    COMPUTE_ERRORS(-1,1);
    UPDATE_VECTORS;
  }
  
  /* 2. Position (-1,1). Up - Right. MSE*/ {
    MSE(-1,1);
    UPDATE_VECTORS;
  }
  
  /* 3. Position (1,-1). Down - left. */ {
    COMPUTE_ERRORS(1,-1);
    UPDATE_VECTORS;
  }
  
  /* 3. Position (1,-1). Down - left. MSE*/ {
    MSE(1,-1);
    UPDATE_VECTORS;
  }
  
  /* 4. Position (1,1). Down - Right. */ {
    COMPUTE_ERRORS(1,1);
    UPDATE_VECTORS;
  }
  
  /* 4. Position (1,1). Down - Right. MSE*/ {
    MSE(1,1);
    UPDATE_VECTORS;
  }
  
  /* 5. Position (-1,0). Up. */ {
    COMPUTE_ERRORS(-1,0);
    UPDATE_VECTORS;
  }
  
  /* 5. Position (-1,0). Up. MSE*/ {
    MSE(-1,0);
    UPDATE_VECTORS;
  }
  
  /* 6. Position (1,0). Down. */ {
    COMPUTE_ERRORS(1,0);
    UPDATE_VECTORS;
  }
  
  /* 6. Position (1,0). Down. MSE*/ {
    MSE(1,0);
    UPDATE_VECTORS;
  }
  
  /* 7. Position (0,1). Right. */ {
    COMPUTE_ERRORS(0,1);
    UPDATE_VECTORS;
  }
  
  /* 7. Position (0,1). Right. MSE*/ {
    MSE(0,1);
    UPDATE_VECTORS;
  }
  
  /* 8. Position (0,-1). Left. */ {
    COMPUTE_ERRORS(0,-1);
    UPDATE_VECTORS;
  }
  
  /* 8. Position (0,-1). Left. MSE*/ {
    MSE(0,-1);
    UPDATE_VECTORS;
  }
  
  /* 9. Position (0,0). */ {
    COMPUTE_ERRORS(0,0);
    UPDATE_VECTORS;
  }
  
  /* 9. Position (0,0). MSE*/ {
    MSE(0,0);
    UPDATE_VECTORS;
  }
  
#undef COMPUTE_ERRORS
#undef MSE
#undef UPDATE_VECTORS
  
  mv[PREV][Y_FIELD][by][bx] = vy[PREV];
  mv[PREV][X_FIELD][by][bx] = vx[PREV];
  mv[NEXT][Y_FIELD][by][bx] = vy[NEXT];
  mv[NEXT][X_FIELD][by][bx] = vx[NEXT];

} /* local_me_for_block() */

/** \brief Estimates the motion of a block from the reference image to the predicted image, 
 * use a search area of +-1.
 * \param mv [PREV|NEXT][Y|X][coor_y][coor_x].
 * \param ref [PREV|NEXT][coor_y][coor_x].
 * \param pred [coor_y][coor_x].
 * \param block_size Size block.
 * \param border_size Size border or margins.
 * \param blocks_in_y Dimension 'Y' of blocks in a picture.
 * \param blocks_in_x Dimension 'X' of blocks in a picture.
 */
void local_me_for_image
(
 MVC_CPU_TYPE ****mv,         /* [PREV|NEXT][Y|X][coor_y][coor_x] */
 TC_CPU_TYPE ***ref,          /* [PREV|NEXT][coor_y][coor_x] */
 TC_CPU_TYPE **pred,          /* [coor_y][coor_x] */
 int block_size,
 int border_size,
 int blocks_in_y,
 int blocks_in_x
) {
  
  for(int by=0; by<blocks_in_y; by++) {
#if defined DEBUG_
    info("%d/%d ", by, blocks_in_y); info_flush();
#endif
    for(int bx=0; bx<blocks_in_x; bx++) {
	
      /* Region occupied by the block (including the border). */
      int luby = (by  ) * block_size - border_size;
      int lubx = (bx  ) * block_size - border_size;
      int rbby = (by+1) * block_size + border_size;
      int rbbx = (bx+1) * block_size + border_size;
      
      local_me_for_block(mv, ref, pred, luby, lubx, rbby, rbbx, by, bx);
    }
  }
#if defined DEBUG
  info("\n");
#endif
}

/** \brief Recalculates the number of blocks in each level DWT (Discrete Wavelet Transform).
 * \param x Number of blocks in a given axis (X or Y) of an image.
 * \param y level DWT.
 * \returns New number of blocks.
 */
int desp(int x, int y) {
  int i;
  for(i=0; i<y; i++) x = (x+1)/2;
  return x;
}

# endif /* FAST_SEARCH */

/** \brief Predicted_pic divided into square blocks disjoint and are
 * sought in reference_pic [0] and reference_pic [1]. Only the luma is
 * used to estimate the motion.\n As a result returned in 'mv' motion
 * vectors calculated.\n These vectors are also an input parameter when
 * we look at an area near an already precalculated displacement (eg, at
 * a level higher temporal resolution).
 * \param mv [PREV|NEXT][y_field|x_field][y_coor][x_coor].
 * \param ref [PREV|NEXT][y_coor][x_coor].
 * \param pred [coor_y][coor_x].
 * \param pixels_in_y Dimension 'Y' of pixels in a picture.
 * \param pixels_in_x Dimension 'X' of pixels in a picture.
 * \param block_size Size block.
 * \param border_size Size border or margins.
 * \param subpixel_accuracy Precision level 'sub-pixel'.
 * \param search_range Search range.
 * \param blocks_in_y Dimension 'Y' of blocks in a picture.
 * \param blocks_in_x Dimension 'X' of blocks in a picture.
 * \param pic_dwt Magnifying images by a factor of 2, to adapt to a new level of DWT.
 * \param mv_dwt Magnifying vectors by a factor of 2, to adapt to a new level of DWT.
*/
void me_for_image
(MVC_CPU_TYPE ****mv,           /* [PREV|NEXT][y_field|x_field][y_coor][x_coor] */
 TC_CPU_TYPE ***ref,            /* [PREV|NEXT][y_coor][x_coor] */
 TC_CPU_TYPE **pred,            /* [y_coor][x_coor] */
 int pixels_in_y,
 int pixels_in_x,
 int block_size,
 int border_size,
 int subpixel_accuracy,
 int search_range,
 int blocks_in_y,
 int blocks_in_x,
 class dwt2d < TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER < TC_CPU_TYPE > > *pic_dwt,
 class dwt2d < MVC_CPU_TYPE, MOTION_INTERPOLATION_FILTER < MVC_CPU_TYPE > > *mv_dwt) {

#if defined FAST_SEARCH
  
  int dwt_levels = (int)rint(log((double)search_range)/log(2.0)) - 1;
#if defined DEBUG
  info("motion_estimate: dwt_levels = %d\n", dwt_levels);
#endif

  /* DWT applied to images. */
  pic_dwt->analyze(ref[PREV], pixels_in_y, pixels_in_x, dwt_levels);
  pic_dwt->analyze(ref[NEXT], pixels_in_y, pixels_in_x, dwt_levels);
  pic_dwt->analyze(pred, pixels_in_y, pixels_in_x, dwt_levels);

  /** \brief Over-pixel estimation. */
#if defined DEBUG
  info("motion_estimate: over-pixel motion estimation level=%d\n", dwt_levels);
#endif

  local_me_for_image(mv,
		     ref,
		     pred,
		     block_size,
		     border_size,
		     desp(blocks_in_y, dwt_levels),
		     desp(blocks_in_x, dwt_levels));
    
  for(int l=dwt_levels-1; l>=0; --l) {
    int Y_l = desp(pixels_in_y, l);
    int X_l = desp(pixels_in_x, l);
    int blocks_in_y_l = desp(blocks_in_y, l);
    int blocks_in_x_l = desp(blocks_in_x, l);

    /** - Wide images on a factor of 2. */
    pic_dwt->synthesize(ref[PREV], Y_l, X_l, 1);
    pic_dwt->synthesize(ref[NEXT], Y_l, X_l, 1);
    pic_dwt->synthesize(pred, Y_l, X_l, 1);

    /** - Motion fields expanded by a factor of 2. This is necessary
	because in the next iteration the reference and predicted
	images are twice as large. */
    mv_dwt->synthesize(mv[PREV][Y_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    mv_dwt->synthesize(mv[NEXT][Y_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    mv_dwt->synthesize(mv[PREV][X_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    mv_dwt->synthesize(mv[NEXT][X_FIELD], blocks_in_y_l, blocks_in_x_l, 1);
    
    /** - Doubles the motion vectors, because the calculated values now
	referenced to an image twice as large in each dimension. */
    for(int by=0; by<blocks_in_y_l; by++) {
      for(int bx=0; bx<blocks_in_x_l; bx++) {

	mv[PREV][Y_FIELD][by][bx] *= 2;
	if(mv[PREV][Y_FIELD][by][bx] > search_range)
	  mv[PREV][Y_FIELD][by][bx] = search_range;
	if(mv[PREV][Y_FIELD][by][bx] < -search_range)
	  mv[PREV][Y_FIELD][by][bx] = -search_range;

	mv[NEXT][Y_FIELD][by][bx] *= 2;
	if(mv[NEXT][Y_FIELD][by][bx] > search_range)
	  mv[NEXT][Y_FIELD][by][bx] =  search_range;
	if(mv[NEXT][Y_FIELD][by][bx] < -search_range)
	  mv[NEXT][Y_FIELD][by][bx] = -search_range;

	mv[PREV][X_FIELD][by][bx] *= 2;
	if(mv[PREV][X_FIELD][by][bx] > search_range)
	  mv[PREV][X_FIELD][by][bx] =  search_range;
	if(mv[PREV][X_FIELD][by][bx] < -search_range)
	  mv[PREV][X_FIELD][by][bx] = -search_range;

	mv[NEXT][X_FIELD][by][bx] *= 2;
	if(mv[NEXT][X_FIELD][by][bx] > search_range)
	  mv[NEXT][X_FIELD][by][bx] =  search_range;
	if(mv[NEXT][X_FIELD][by][bx] < -search_range)
	  mv[NEXT][X_FIELD][by][bx] = -search_range;
      }
    }
#if defined DEBUG
    info("motion_estimate: over-pixel motion estimation level=%d\n",l);
#endif
    local_me_for_image(mv,
		       ref,
		       pred,
		       block_size,
		       border_size,
		       blocks_in_y_l, blocks_in_x_l);
  }
  
  /** Sub-pixel estimation. */
  for(int l=1; l<=subpixel_accuracy; l++) {
#if defined DEBUG
    info("motion_estimate: sub-pixel motion estimation level=%d\n",l);
#endif
    
    /** - Wide images on a factor of 2. */
    pic_dwt->synthesize(ref[PREV], pixels_in_y<<l, pixels_in_x<<l, 1);
    pic_dwt->synthesize(ref[NEXT], pixels_in_y<<l, pixels_in_x<<l, 1);
    pic_dwt->synthesize(pred, pixels_in_y<<l, pixels_in_x<<l, 1);
    
    /** - Motion fields expanded by a factor of 2. */
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {

	mv[PREV][Y_FIELD][by][bx] *= 2;
	if(mv[PREV][Y_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[PREV][Y_FIELD][by][bx] = search_range<<subpixel_accuracy;
	if(mv[PREV][Y_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[PREV][Y_FIELD][by][bx]= -(search_range<<subpixel_accuracy);

	mv[NEXT][Y_FIELD][by][bx] *= 2;
	if(mv[NEXT][Y_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[NEXT][Y_FIELD][by][bx] = search_range<<subpixel_accuracy;
	if(mv[NEXT][Y_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[NEXT][Y_FIELD][by][bx]= -(search_range<<subpixel_accuracy);

	mv[PREV][X_FIELD][by][bx] *= 2;
	if(mv[PREV][X_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[PREV][X_FIELD][by][bx] = (search_range<<subpixel_accuracy);
	if(mv[PREV][X_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[PREV][X_FIELD][by][bx]= -(search_range<<subpixel_accuracy);

	mv[NEXT][X_FIELD][by][bx] *= 2;
	if(mv[NEXT][X_FIELD][by][bx]>(search_range<<subpixel_accuracy))
	  mv[NEXT][X_FIELD][by][bx] = (search_range<<subpixel_accuracy);
	if(mv[NEXT][X_FIELD][by][bx]<-(search_range<<subpixel_accuracy))
	  mv[NEXT][X_FIELD][by][bx]= -(search_range<<subpixel_accuracy);
      }
    }
    
    local_me_for_image(mv,
		       ref,
		       pred,
		       block_size<<l,
		       border_size>>l,
		       blocks_in_y, blocks_in_x);
  }

  /* - The images as they were left to the next search. */
  pic_dwt->analyze(ref[PREV], pixels_in_y << subpixel_accuracy, pixels_in_x << subpixel_accuracy, subpixel_accuracy);
  pic_dwt->analyze(ref[NEXT], pixels_in_y << subpixel_accuracy, pixels_in_x << subpixel_accuracy, subpixel_accuracy);
  pic_dwt->analyze(pred, pixels_in_y << subpixel_accuracy, pixels_in_x << subpixel_accuracy, subpixel_accuracy);

  //pic_dwt->analyze(reference_pic, Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);
  //pic_dwt->analyze(predicted_pic, Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);

#else /* !defined FAST_SEARCH */

  pic_dwt->synthesize(reference_pic[0], Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);
  pic_dwt->synthesize(reference_pic[1], Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);
  pic_dwt->synthesize(predicted_pic, Y<<subpixel_accuracy, X<<subpixel_accuracy, subpixel_accuracy);
  
  block_size <<= subpixel_accuracy;
  search_range <<= subpixel_accuracy;
  border_size <<= subpixel_accuracy;
  
  int blocks_in_y = (Y<<subpixel_accuracy)/block_size;
  int blocks_in_x = (X<<subpixel_accuracy)/block_size;
  
  for(int by=0; by<blocks_in_y; by++) {
    print("%d/%d ",by,blocks_in_y); fflush(stderr);
    for(int bx=0; bx<blocks_in_x; bx++) {
      int min_error = 999999999;
      int vy, vx;
      
      /* For each point of the search area. */
      for(int ry=by*block_size-search_range; ry<=by*block_size+search_range; ry++) {
	for(int rx=bx*block_size-search_range; rx<=bx*block_size+search_range; rx++) {
	  /* For each point of the block to search. */
	  int error = 0;
	  for(int y=-border_size; y<block_size+border_size; y++) {
	    for(int x=-border_size; x<block_size+border_size; x++) {
	      error += abs(predicted_pic[by*block_size+y][bx*block_size+x] -
			   reference_pic
			   [0]
			   [ry + mv[NEXT][Y][by][bx] + y]
			   [rx + mv[NEXT][X][by][bx] + x]);
	      error += abs(predicted_pic[by*block_size+y][bx*block_size+x] -
			   reference_pic
			   [1]
			   [by*block_size*2 - ry + mv[PREV][Y][by][bx] + y]
			   [bx*block_size*2 - rx + mv[PREV][X][by][bx] + x]);
	    }
	  }
	  if(error < min_error) {
	    min_error = error;
	    vy = ry-by*block_size;
	    vx = rx-bx*block_size;
	  }
	  /*print("\n%d,%d  %d,%d %d %d",
	    ry + mv[NEXT][Y][by][bx],
	    rx + mv[NEXT][X][by][bx],
	    by*block_size*2 - ry + mv[PREV][Y][by][bx],
	    bx*block_size*2 - rx + mv[PREV][X][by][bx],
	    error, min_error
	    );*/
	}
      }
      
      mv[NEXT][Y][by][bx] += vy;
      mv[NEXT][X][by][bx] += vx;
      mv[PREV][Y][by][bx] += -vy;
      mv[PREV][X][by][bx] += -vx;
      
      //print("\nvector = %d,%d,%d,%d",mv[NEXT][Y][by][bx],mv[NEXT][X][by][bx],mv[PREV][Y][by][bx],mv[PREV][X][by][bx]);
    }
  }

#endif /* FAST_SEARCH */

} /* me_for_image */

#include <getopt.h>

/** \brief Provides a main function which reads in parameters from the command line and a parameter file.
 * \param argc The number of command line arguments of the program.
 * \param argv The contents of the command line arguments of the program.
 * \returns Notifies proper execution.
 */
int main(int argc, char *argv[]) {

#if defined DEBUG
  info("%s ", argv[0]);
  for(int i=1; i<argc; i++) {
    info("%s ", argv[i]);
  }
  info("\n");
#endif

  int block_size = 32;
  int border_size = 0;
  char *even_fn = (char *)"even";
  char *imotion_fn = (char *)"imotion";
  char *motion_fn = (char *)"motion";
  char *odd_fn = (char *)"odd";
  int pictures = 9;
  int pixels_in_x = 352;
  int pixels_in_y = 288;
  int search_range = 4;
  int subpixel_accuracy = 0;
  
  int c;
  while(1) {
    
    /* http://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Option-Example.html */
    static struct option long_options[] = {
      {"block_size", required_argument, 0, 'b'},
      {"border_size", required_argument, 0, 'd'},
      {"even_fn", required_argument, 0, 'e'},
      {"imotion_fn", required_argument, 0, 'i'},
      {"motion_fn", required_argument, 0, 'm'},
      {"odd_fn", required_argument, 0, 'o'},
      {"pictures", required_argument, 0, 'p'},
      {"pixels_in_x", required_argument, 0, 'x'},
      {"pixels_in_y", required_argument, 0, 'y'},
      {"search_range", required_argument, 0, 's'},
      {"subpixel_accuracy", required_argument, 0, 'a'},
      {"help", no_argument, 0, '?'},
      {0, 0, 0, 0}
    };

    int option_index = 0;
    
    c = getopt_long(argc, argv, "b:d:e:i:m:o:p:x:y:s:a:?", long_options, &option_index);

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
#if defined DEBUG
      info("%s: block_size=%d\n", argv[0], block_size);
#endif
      break;
      
    case 'e':
      even_fn = optarg;
#if defined DEBUG
      info("%s: even_fn=\"%s\"\n", argv[0], even_fn);
#endif
      break;

    case 'i':
      imotion_fn = optarg;
#if defined DEBUG
      info("%s: imotion_fn=\"%s\"\n", argv[0], imotion_fn);
#endif
      break;

    case 'm':
      motion_fn = optarg;
#if defined DEBUG
      info("%s: motion_fn=\"%s\"\n", argv[0], motion_fn);
#endif
      break;

    case 'o':
      odd_fn = optarg;
#if defined DEBUG
      info("%s: odd_fn=\"%s\"\n", argv[0], odd_fn);
#endif
      break;

    case 'd':
      border_size = atoi(optarg);
#if defined DEBUG
      info("%s: border_size=%d\n", argv[0], border_size);
#endif
      break;

    case 'p':
      pictures = atoi(optarg);
#if defined DEBUG
      info("%s: pictures=%d\n", argv[0], pictures);
#endif
      break;
      
    case 'x':
      pixels_in_x = atoi(optarg);
 #if defined DEBUG
     info("%s: pixels_in_x=%d\n", argv[0], pixels_in_x);
#endif
      break;
      
    case 'y':
      pixels_in_y = atoi(optarg);
#if defined DEBUG
      info("%s: pixels_in_y=%d\n", argv[0], pixels_in_y);
#endif
      break;
      
    case 's':
      search_range = atoi(optarg);
#if defined DEBUG
      info("%s: search_range=%d\n", argv[0], search_range);
#endif
      break;
      
    case 'a':
      subpixel_accuracy = atoi(optarg);
#if defined DEBUG
      info("%s: subpixel_accuracy=%d\n", argv[0], subpixel_accuracy);
#endif
      break;
      
    case '?':
      printf("+----------------------+\n");
      printf("| MCTF motion_estimate |\n");
      printf("+----------------------+\n");
      printf("\n");
      printf("   Block-based time-domain motion estimation.\n");
      printf("\n");
      printf("  Parameters:\n");
      printf("\n");
      printf("   -[-b]lock_size = size of the blocks in the motion estimation process (%d)\n", block_size);
      printf("   -[-]bor[d]der_size = size of the border of the blocks in the motion estimation process (%d)\n", border_size);
      printf("   -[-e]ven_fn = input file with the even pictures (\"%s\")\n", even_fn);
      printf("   -[-i]motion_fn = input file with the initial motion fields (\"%s\")\n", imotion_fn);
      printf("   -[-m]otion_fn = output file with the motion fields (\"%s\")\n", imotion_fn);
      printf("   -[-o]dd_fn = input file with odd pictures (\"%s\")\n", odd_fn);
      printf("   -[-p]ictures = number of images to process (%d)\n", pictures);
      printf("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n", pixels_in_x);
      printf("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n", pixels_in_y);
      printf("   -[-s]earch_range = size of the searching area of the motion estimation (%d)\n", search_range);
      printf("   -[-]subpixel_[a]ccuracy = sub-pixel accuracy of the motion estimation (%d)\n", subpixel_accuracy);
      printf("\n");
      exit(1);
      break;
      
    default:
      error("%s: Unrecognized argument. Aborting ...\n", argv[0]);
      abort();
    }
  }
  
  int reuse_motion = 1;

  FILE *motion_fd; {
    motion_fd = fopen(motion_fn, "r");
    if(!motion_fd) {
      reuse_motion = 0;
#if defined DEBUG
      info("%s: computing motion information\n", argv[0]);
#endif
      motion_fd = fopen(motion_fn, "w");
      if(!motion_fd) {
	error("%s: unable to create the file \"%s\" ... aborting!\n",
	      argv[0], motion_fn);
	abort();
      }
    } else {
#if defined DEBUG
      info("%s: reusing motion information \"%s\"\n",
	   argv[0], motion_fn);
#endif
    }
  }

  if(reuse_motion) exit(0);

  FILE *imotion_fd; {
    imotion_fd = fopen(imotion_fn, "r");
    if(!imotion_fd) {
#if defined DEBUG
      info("%s: \"%s\" does not exist: initial_motion_fn = \"%s\"\n",
	   argv[0], imotion_fn, "/dev/zero");
#endif
      imotion_fd = fopen("/dev/zero", "r");
      /* /dev/zero should always be. */
    }
  }

  FILE *even_fd; {
    even_fd = fopen(even_fn, "r");
    if(!even_fd) {
      error("%s: \"%s\" does not exist ... aborting!\n",
	    argv[0], even_fn);
      abort();
    }
  }

  FILE *odd_fd; {
    odd_fd = fopen(odd_fn, "r");
    if(!odd_fd) {
      error("%s: \"%s\" does not exist ... aborting!\n",
	    argv[0], odd_fn);
      abort();
    }
  }

  int picture_border_size = search_range + border_size;

  texture < TC_IO_TYPE, TC_CPU_TYPE > texture;

  TC_CPU_TYPE **reference[2];
  for(int i=0; i<2; i++) {
    reference[i] =
      texture.alloc(pixels_in_y << subpixel_accuracy,
		    pixels_in_x << subpixel_accuracy,
		    picture_border_size << subpixel_accuracy/*2*/);

    /* This initialization seems not necessary. */
    for(int y=0; y<pixels_in_y << subpixel_accuracy; y++) {
      for(int x=0; x<pixels_in_x <<subpixel_accuracy; x++) {
	reference[i][y][x] = 0;
      }
    }
  }
  
  TC_CPU_TYPE **predicted =
    texture.alloc(pixels_in_y << subpixel_accuracy,
		  pixels_in_x << subpixel_accuracy,
		  picture_border_size << subpixel_accuracy/*2*/);

  /* This initialization seems not necessary. */
  for(int y=0; y<pixels_in_y << subpixel_accuracy; y++) {
    for(int x=0; x<pixels_in_x <<subpixel_accuracy; x++) {
      predicted[y][x] = 0;
    }
  }

  int blocks_in_y = pixels_in_y/block_size;
  int blocks_in_x = pixels_in_x/block_size;
#if defined DEBUG
  info("%s: blocks_in_y=%d\n", argv[0], blocks_in_y);
  info("%s: blocks_in_x=%d\n", argv[0], blocks_in_x);
#endif

  motion < MVC_TYPE > motion;
  MVC_CPU_TYPE ****mv = motion.alloc(blocks_in_y, blocks_in_x);

  class dwt2d <
  TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER <
  TC_CPU_TYPE > > *texture_dwt
    = new class dwt2d <
  TC_CPU_TYPE, TEXTURE_INTERPOLATION_FILTER <
  TC_CPU_TYPE > >;
  texture_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  class dwt2d < 
  MVC_CPU_TYPE, MOTION_INTERPOLATION_FILTER <
  MVC_CPU_TYPE > > *motion_dwt
    = new class dwt2d <
  MVC_CPU_TYPE, MOTION_INTERPOLATION_FILTER <
  MVC_CPU_TYPE > >;
  motion_dwt->set_max_line_size(PIXELS_IN_X_MAX);

  /* Read the luma of reference[0]. */
  texture.read(even_fd, reference[0], pixels_in_y, pixels_in_x);

  /* Skip to the chroma. */
  fseek(even_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);
  fseek(even_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);

  /* Fill the edge of the read image. */
  texture.fill_border(reference[0],
		      pixels_in_y,
		      pixels_in_x,
		      picture_border_size);

  for(int i=0; i<pictures/2; i++) {

#if defined DEBUG
    info("%s: reading picture %d of \"%s\".\n",
	 argv[0], i, odd_fn);
#endif

    /* Luma. */
    texture.read(odd_fd, predicted, pixels_in_y, pixels_in_x);

    /* Chroma. */
    fseek(odd_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);
    fseek(odd_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);

#if defined DEBUG
    info("%s: reading picture %d of \"%s\".\n",
	 argv[0], i, even_fn);
#endif
    /* This initialization seems to do nothing. */
    for(int y=0; y<pixels_in_y << subpixel_accuracy; y++) {
      for(int x=0; x<pixels_in_x <<subpixel_accuracy; x++) {
	reference[1][y][x] = 0;
      }
    }

    /* Luma. */
    texture.read(even_fd, reference[1], pixels_in_y, pixels_in_x);

    /* Cromas. */
    fseek(even_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);
    fseek(even_fd, (pixels_in_y/2) * (pixels_in_x/2) * sizeof(unsigned char), SEEK_CUR);

    /* Fill the edge of the read image. */
    texture.fill_border(reference[1],
			pixels_in_y,
			pixels_in_x,
			picture_border_size);

#if defined DEBUG
    info("%s: reading initial motion vectors.\n", argv[0]);
#endif
    //motion.read(imotion_fd, mv, blocks_in_y, blocks_in_x);
    //This does nothing (leave the above).
    for(int by=0; by<blocks_in_y; by++) {
      for(int bx=0; bx<blocks_in_x; bx++) {
	mv[PREV][Y_FIELD][by][bx] = mv[PREV][X_FIELD][by][bx] = mv[NEXT][Y_FIELD][by][bx] = mv[NEXT][X_FIELD][by][bx] = 0;
      }
    }

    me_for_image(mv,
		 reference,
		 predicted,
		 pixels_in_y, pixels_in_x,
		 block_size,
		 border_size,
		 subpixel_accuracy,
		 search_range,
		 blocks_in_y,
		 blocks_in_x,
		 texture_dwt,
		 motion_dwt);
    
#ifdef CLEAR_MVS
    for(int y=0; y<blocks_in_y; y++) {
      for(int x=0; x<blocks_in_x; x++) {
	mv[PREV][Y_FIELD][y][x] = 0;
	mv[PREV][X_FIELD][y][x] = 0;
	mv[NEXT][Y_FIELD][y][x] = 0;
	mv[NEXT][X_FIELD][y][x] = 0;
      }
    }
#endif

#if defined DEBUG
    info("Backward motion vector field:");
    for(int y=0; y<blocks_in_y; y++) {
      info("\n");
      for(int x=0; x<blocks_in_x; x++) {
	static char aux[80];
	sprintf(aux,"%3d,%3d",
	     mv[PREV][Y_FIELD][y][x],
	     mv[PREV][X_FIELD][y][x]);
	info("%8s",aux);
      }
    }
    info("\n");

    info("Forward motion vector field:");
    for(int y=0; y<blocks_in_y; y++) {
      info("\n");
      for(int x=0; x<blocks_in_x; x++) {
	static char aux[80];
	sprintf(aux,"%3d,%3d",
	     mv[NEXT][Y_FIELD][y][x],
	     mv[NEXT][X_FIELD][y][x]);
	info("%8s",aux);
      }
    }
    info("\n");
#endif

#if defined GNUPLOT
    for(int y=0; y<blocks_in_y; y++) {
      for(int x=0; x<blocks_in_x; x++) {
	printf("GNUPLOT %d %d %f %f %f %f\n",
	       x*block_size, y*block_size,
	       (float)mv[PREV][X_FIELD][y][x], (float)mv[PREV][Y_FIELD][y][x],
	       (float)mv[NEXT][X_FIELD][y][x], (float)mv[NEXT][Y_FIELD][y][x]);
      }
    }
#endif

#if defined DEBUG
    info("%s: writing motion vector field %d in \"%s\".\n",
	 argv[0], i, motion_fn);
#endif
    motion.write(motion_fd, mv, blocks_in_y, blocks_in_x);

    /* SWAP(&reference_pic[0], &reference_pic[1]). */ {
      TC_CPU_TYPE **tmp = reference[0];
      reference[0] = reference[1];
      reference[1] = tmp;
    }
  }

  delete motion_dwt;
  delete texture_dwt;

}
