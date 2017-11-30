/**
 * \file entropy.h
 * 
 * \author Programmer. gse.
 * \date Last modification: 2003, September 29.
 * \brief Compute the entropy of an histogram.
 * 
 * \note
 * The entropy of a information source Z is:\n
   \verbatim
   H(Z) = - Sum P(i)*log_2(P(i))
   \endverbatim
 * Where i = [0, .., N). And where N is the size of\n
 * the alphabet (number of different symbols) and P(i)\n
 * is the probability of find the symbol i.
 * 
 * \param count Counter for alphabet.
 * \param ALPHABET_SIZE Number of different elements.
 * \returns Entropy value.
 * 
   \example entropy.h Usage
   \verbatim
   #include "entropy.h"
   #define ALPHABET_SIZE 256
   
   unsigned long *count = new unsigned long[ALPHABET_SIZE];
   // You should be sure that count[i]=0 for each i
   
   for (;;) {
	 int x;
	 x = file.get();
	 if ( x == EOF ) break;
	 count[x]++;
   }

   double entropy_value = entropy ( count, ALPHABET_SIZE ) ;
   \endverbatim
 */


/**
 * \brief Compute the entropy of an histogram.
 */
float entropy(int *count, int alphabet_size);

