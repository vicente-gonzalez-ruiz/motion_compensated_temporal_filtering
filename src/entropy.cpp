/**
 * \file entropy.cpp
 * \author Vicente Gonzalez-Ruiz.
 * \date Last modification: 2015, January 7.
 * \brief Compute the entropy of an histogram.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

#include <math.h>
#include "entropy.h"

/** \brief Compute the entropy of an histogram.
 * \param count Counter for alphabet.
 * \param alphabet_size Number of different elements.
 * \returns Entropy value.
 */
float entropy(int *count, int alphabet_size) {
  float entropy = 0.0;
  int total_count = 0;
  for(int i=0; i<alphabet_size; i++) {
    total_count += count[i];
  }

  for(int i=0; i<alphabet_size; i++) {
    if(count[i]) {
      float prob = (float)count[i]/total_count;
      entropy += prob*(float)(log(prob)/log(2.0));
    }
  }
  return -entropy;
}
