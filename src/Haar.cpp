/** \file Haar.cpp
 * \brief Applies Filter Bank (Haar).
 * \author Vicente Gonzalez-Ruiz
 * \date Last modification: 2015, January 7.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/*! \brief 2/1 (Haar) Biorthogonal Perfect Reconstruction Filter Bank */
class Haar {

 public:
  
  /*! \brief Filter identifies. 
  * \returns Filter name.
  */
  static char *get_filter_name() {
    return "2/1 (Haar) Biorthogonal Perfect Reconstruction Filter Bank";
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
    int i, k;
    for (i = k = 0; k < n; i++, k += 2) {
      h[i] = s[k+1] - s[k];
      l[i] = s[k] + h[i]/2;
    }
  }

  /*! \brief Analyzes the odd samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void odd_analyze(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i, k;
    for (i = k = 0; k < (n-1); i++, k += 2) {
      h[i] = s[k+1] - s[k];
      l[i] = s[k] + h[i]/2;
    }
    l[i] = s[k];
  }

  /*! \brief Synthesizing the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_synthesize(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i, k;
    for (i = k = 0; k < n; i++, k += 2) {
      s[k] = l[i] - h[i]/2;
      s[k+1] = s[k] + h[i];
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
    for (i = k = 0; k < (n-1); i++, k += 2) {
      s[k] = l[i] - h[i]/2;
      s[k+1] = s[k] + h[i];
    }
    s[k] = l[i];
  }

};
