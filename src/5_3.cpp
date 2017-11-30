/** \file 5_3.cpp
 * \brief Applies Filter Bank (5_3).
 * \author Vicente Gonzalez-Ruiz
 * \date Last modification: 2015, January 7.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/*! \brief 5/3 (Lineal) Biorthogonal Perfect Reconstruction Filter Bank. */
class _5_3 {

 public:
  
  /*! \brief Filter identifies. 
  * \returns Filter name.
  */
  static char *get_filter_name() {
    return "5/3 (Lineal) Biorthogonal Perfect Reconstruction Filter Bank";
  }

  /*! \brief Tap identifies. 
   * \returns Filter number.
   */
  int get_tap() {
    return 5;
  }

  /*! \brief Analyzes the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_analyze(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    for(i=0;i<n/2-1;i++) {
      int i2 = i<<1;
      h[i] = s[i2+1] - (s[i2]+s[i2+2])/2;
    }
    h[i] = s[n-1] - s[n-2];
    
    l[0] = s[0] + h[0]/2;
    for(i=1;i<n/2;i++) {
      int i2 = i<<1;
      l[i] = s[i2] + (h[i]+h[i-1])/4;
    }
  }

  /*! \brief Analyzes the odd samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void odd_analyze(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    for(i=0;i<n/2;i++) {
      int i2 = i<<1;
      h[i] = s[i2+1] - (s[i2]+s[i2+2])/2;
    }
    
    l[0] = s[0] + h[0]/2;
    for(i=1;i<n/2;i++) {
      int i2 = i<<1;
      l[i] = s[i2] + (h[i]+h[i-1])/4;
    }
    l[i] = s[n-1] + h[i-1]/2;
  }

  /*! \brief Synthesizing the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_synthesize(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    s[0] = l[0] - h[0]/2;
    for(i=1;i<n/2;i++) {
      int i2 = i<<1;
      s[i2] = l[i] - (h[i]+h[i-1])/4;
    }
    
    for(i=0;i<n/2-1;i++) {
      int i2 = i<<1;
      s[i2+1] = h[i] + (s[i2]+s[i2+2])/2;
    }
    s[n-1] = h[i] + s[n-2];
  }

  /*! \brief Synthesizing the odd samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void odd_synthesize(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    s[0] = l[0] - h[0]/2;
    for(i=1;i<n/2;i++) {
      int i2 = i<<1;
      s[i2] = l[i] - (h[i]+h[i-1])/4;
    }

    s[n-1] = l[i] - h[i-1]/2;
    for(i=0;i<n/2;i++) {
      int i2 = i<<1;
      s[i2+1] = h[i] + (s[i2]+s[i2+2])/2;
    } 
  }

};
