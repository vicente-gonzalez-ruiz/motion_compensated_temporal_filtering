/**
 * \file display.cpp
 * \author Vicente Gonzalez-Ruiz
 * \date Last modification: 2015, January 7.
 * \brief Shows real-time information about running processes.
 *
 * The MCTF project has been supported by the Junta de Andalucía through
 * the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
 * sobre Internet" (P10-TIC-6548).
 */

/**
 * \brief Shows information about variables.
 */
void info(const char *args, ...) {
  va_list ap;
  va_start(ap, args);
  vfprintf(stdout, args, ap);
  fflush(stdout);
}

/**
 * \brief Shows information about errors.
 */
void error(const char *args, ...) {
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;31m");
  vfprintf(stderr, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stderr);
}

/**
 * \brief Shows information about variables.
 */
void info_flush() {
  fflush(stdout);
}

/**
 * \brief Shows information about errors.
 */
void error_flush() {
  fflush(stderr);
}
