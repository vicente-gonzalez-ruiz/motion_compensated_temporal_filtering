/** \file 13_7.cpp
 * \brief Applies Filter Bank (13_7).
 * \author Vicente Gonzalez-Ruiz
 * \date Last modification: 2015, January 7.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

/** \tparam TYPE is a data type indicating that it does not use any particular template. */
template <typename TYPE>

/*! \brief 13/7 (Cubic) Birthogonal Perfect Reconstruction Filter Bank. */
class _13_7 {

 public:
  
  /*! \brief Filter identifies. 
  * \returns Filter name.
  */
  static char *get_filter_name() {
    return "13/7 (Cubic) Birthogonal Perfect Reconstruction Filter Bank";
  }

  /*! \brief Tap identifies. 
   * \returns Filter number.
   */
  int get_tap() {
    return 13;
  }

  /*! \brief Analyzes the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_analyze(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    h[0] = s[1] - s[0];
    
    if(n>2) {
      for(i=1;i<n/2-2;i++) {
	int i2 = i<<1;
	h[i] = s[i2+1] - ((9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4])+8)>>4);
	//h[i] = s[i2+1] - (9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4])/16);
      }
      h[n/2-2] = s[n-3] - ((s[n-4]+s[n-2]+1)>>1);
      //h[n/2-2] = s[n-3] - (s[n-4]+s[n-2])/2;
      h[n/2-1] = s[n-1] - s[n-2];
    }
    
    l[0] = s[0] + ((h[0])>>1);
    //l[0] = s[0] + h[0]/2;
    
    if(n>2) {
      l[1] = s[2] + ((h[0]+h[1]+1)>>2);
      //l[1] = s[2] + (h[0]+h[1])/4;
      for(i=2; i<n/2-1; i++) {
	int i2 = i<<1;
	l[i] = s[i2] + ((-h[i-2]+9*(h[i-1]+h[i])-h[i+1]+16)>>5);
	//l[i] = s[i2] + (-h[i-2]+9*(h[i-1]+h[i])-h[i+1])/32;
      }
      l[n/2-1] = s[n-2] + ((h[n/2-2]+h[n/2-1]+1)>>2);
      //l[n/2-1] = s[n-2] + (h[n/2-2]+h[n/2-1]+1)/4;
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
    h[0] = s[1] - ((s[0]+s[2]+1)>>1);
    //h[0] = s[1] - (s[0]+s[2])/2;
    for(i=1;i<n/2-1;i++) {
      int i2 = i<<1;
      h[i] = s[i2+1] - ((9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4])+8)>>4);
      //h[i] = s[i2+1] - (9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4]))/16;
    }
    h[n/2-1] = s[n-2] - ((s[n-3]+s[n-1]+1)>>1);
    //h[n/2-1] = s[n-2] - (s[n-3]+s[n-1])/2;
    
    l[0] = s[0] + (h[0]>>1);
    //l[0] = s[0] + h[0]/2;
    l[1] = s[2] + ((h[0]+h[1]+1)>>2);
    //l[1] = s[2] + (h[0]+h[1])/4;
    
    for(i=2; i<n/2-1; i++) {
      int i2 = i<<1;
      l[i] = s[i2] + ((-h[i-2]+9*(h[i-1]+h[i])-h[i+1]+16)>>5);
      //l[i] = s[i2] + (-h[i-2]+9*(h[i-1]+h[i])-h[i+1])/32;
    }
    l[n/2-1] = s[n-3] + ((h[n/2-2]+h[n/2-1]+1)>>2);
    //l[n/2-1] = s[n-3] + (h[n/2-2]+h[n/2-1])/4;
    l[n/2] = s[n-1] + (h[n/2-1]>>1);
    //l[n/2] = s[n-1] + h[n/2-1]/2;
  }

  /*! \brief Synthesizing the even samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void even_synthesize(TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    s[0] = l[0] - ((h[0])>>1);
    //s[0] = l[0] - h[0]/2;
    
    if(n>2) {
      s[2] = l[1] - ((h[0]+h[1]+1)>>2);
      //s[2] = l[1] - (h[0]+h[1])/4;
      for(i=2; i<n/2-1; i++) {
	int i2 = i<<1;
	s[i2] = l[i] - ((-h[i-2]+9*(h[i-1]+h[i])-h[i+1]+16)>>5);
	//s[i2] = l[i] - (-h[i-2]+9*(h[i-1]+h[i])-h[i+1])/32;
      }
      s[n-2] = l[n/2-1] - ((h[n/2-2]+h[n/2-1]+1)>>2);
      //s[n-2] = l[n/2-1] - (h[n/2-2]+h[n/2-1])/4;
    }
    
    s[1] = h[0] + s[0];
    if(n>2) {
      for(i=1;i<n/2-2;i++) {
	int i2 = i<<1;
	s[i2+1] = h[i] + ((9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4])+8)>>4);
	//s[i2+1] = h[i] + (9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4]))/16;
      }
      s[n-3] = h[n/2-2] + ((s[n-4]+s[n-2]+1)>>1);
      //s[n-3] = h[n/2-2] + (s[n-4]+s[n-2])/2;
      s[n-1] = h[n/2-1] + s[n-2];
    }
  }

  /*! \brief Synthesizing the odd samples.
   * \param s Signal.
   * \param l Low.
   * \param h High.
   * \param n Number of samples.
   */
  void odd_synthesize (TYPE s[], TYPE l[], TYPE h[], int n) {
    int i;
    s[0] = l[0] - (h[0]>>1);
    //s[0] = l[0] - h[0]/2;
    s[2] = l[1] - ((h[0]+h[1]+1)>>2);
    //s[2] = l[1] - (h[0]+h[1])/4;
    
    for(i=2; i<n/2-1; i++) {
      int i2 = i<<1;
      s[i2] = l[i] - ((-h[i-2]+9*(h[i-1]+h[i])-h[i+1]+16)>>5);
      //s[i2] = l[i] - (-h[i-2]+9*(h[i-1]+h[i])-h[i+1])/32;
    }
    s[n-3] = l[n/2-1] - ((h[n/2-2]+h[n/2-1]+1)>>2);
    //s[n-3] = l[n/2-1] - (h[n/2-2]+h[n/2-1])/4;
    s[n-1] = l[n/2] - (h[n/2-1]>>1);
    //s[n-1] = l[n/2] - h[n/2-1]/2;
    
    s[1] = h[0] + ((s[0]+s[2]+1)>>1);
    //s[1] = h[0] + (s[0]+s[2])/2;
    for(i=1;i<n/2-1;i++) {
      int i2 = i<<1;
      s[i2+1] = h[i] + ((9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4])+8)>>4);
      //s[i2+1] = h[i] + (9*(s[i2]+s[i2+2]) - (s[i2-2]+s[i2+4]))/16;
    }
    s[n-2] = h[n/2-1] + ((s[n-3]+s[n-1]+1)>>1);
    //s[n-2] = h[n/2-1] + (s[n-3]+s[n-1])/2;
  }

};
