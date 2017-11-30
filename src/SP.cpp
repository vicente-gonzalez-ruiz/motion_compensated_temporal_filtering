/** \file SP.cpp
 * \brief Applies Filter Bank (S+P).
 * \author Vicente Gonzalez-Ruiz
 * \date Last modification: 2015, January 7.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/** \brief S+P Biorthogonal Perfect Reconstruction Filter Bank. */ 
class SP {

 public:

  /*! \brief Filter identifies. 
  * \returns Filter name.
  */
  static char *get_filter_name() {
    return "S+P Biorthogonal Perfect Reconstruction Filter Bank";
  }

  /*! \brief Tap identifies. 
   * \returns Filter number.
   */
  int get_tap() {
    return 2;
  }

  /*! \brief Analyzes the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_analyze(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i, k, mm = n/2 - 1;
    int d1, d2;
    
    for (i = k = 0; k < n; i++, k += 2) {
      l[i] = (s[k] + s[k+1]) >> 1;
    }
    if(n>2) {
      h[0] -= (d2 = l[0] - l[1]) >> 2;
	for (i = 1; i < mm; i++) {
	  d1 = d2;  d2 = l[i] - l[i+1];
	  h[i] -= (((d1 + d2 - h[i+1]) << 1) + d2 + 3) >> 3;
	}
      h[i] -= d2 >> 2;
    }
  }

  /*! \brief Analyzes the odd samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void odd_analyze(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i, k, mm = n/2 - 1;
    int d1, d2;
    
    for (i = k = 0; k < (n-1); i++, k += 2) {
      l[i] = (s[k] + s[k+1]) >> 1;
      h[i] =  s[k] - s[k+1];
    }
    l[i] = s[n-1];
    if(n>2) {
      h[0] -= (d2 = l[0] - l[1]) >> 2;
      for (i = 1; i < mm; i++) {
	d1 = d2;  d2 = l[i] - l[i+1];
	h[i] -= (((d1 + d2 - h[i+1]) << 1) + d2 + 3) >> 3;
      }
      h[i] -= d2 >> 2;
    }
  }

  /*! \brief Synthesizing the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_synthesize(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i, k;
    int d1, d2, m=n/2;
    if(n>2) {
      h[m-1] += (d1 = l[m-2] - l[m-1]) >> 2;
      for (i = m - 2; i > 0; i--) {
	d2 = d1;  d1 = l[i-1] - l[i];
	h[i] += (((d1 + d2 - h[i+1]) << 1) + d2 + 3) >> 3;
      }
      h[0] += d1 >> 2;
    }
    for (i = k = 0; k < n; i++, k += 2) {
      s[k] = l[i] + ((h[i] + 1) >> 1);
      s[k+1] = s[k] - h[i];
    }
  }

  /*! \brief Synthesizing the odd samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void odd_synthesize (TYPE s[], TYPE l[], TYPE h[], int n) {
    int i, k;
    int d1, d2, m=n/2;
    if(n>2) {
      h[m-1] += (d1 = l[m-2] - l[m-1]) >> 2;
      for (i = m - 2; i > 0; i--) {
	d2 = d1;  d1 = l[i-1] - l[i];
	h[i] += (((d1 + d2 - h[i+1]) << 1) + d2 + 3) >> 3;
      }
      h[0] += d1 >> 2;
    }
    for (i = k = 0; k < (n-1); i++, k += 2) {
      s[k] = l[i] + ((h[i] + 1) >> 1);
      s[k+1] = s[k] - h[i];
    }
    s[k] = l[i];
  }

};
