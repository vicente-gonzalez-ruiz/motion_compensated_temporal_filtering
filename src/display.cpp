void info(const char *args, ...) {
#if defined __INFO__
  va_list ap;
  va_start(ap, args);
  vfprintf(stdout, args, ap);
  fflush(stdout);
#endif
}

void error(const char *args, ...) {
#if defined __DEBUG__
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;31m");
  vfprintf(stderr, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stderr);
#endif
}

void info_flush() {
#if defined __INFO__
  fflush(stdout);
#endif
}

void error_flush() {
#if defined __DEBUG__
  fflush(stderr);
#endif
}
