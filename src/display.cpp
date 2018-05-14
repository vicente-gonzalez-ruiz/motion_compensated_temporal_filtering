void info(const char *args, ...) {
#if defined __INFO__
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;32m");
  vfprintf(stdout, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stdout);
#endif /* __INFO__ */
}

void error(const char *args, ...) {
#if defined __DEBUG__
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;31m");
  vfprintf(stderr, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stderr);
#endif /* __DEBUG__ */
}

void warning(const char *args, ...) {
#if defined __WARNING__
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;33m");
  vfprintf(stderr, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stderr);
#endif /* __WARNING__ */
}

void info_flush() {
#if defined __INFO__
  fflush(stdout);
#endif /* __INFO__ */
}

void error_flush() {
#if defined __DEBUG__
  fflush(stderr);
#endif /* __DEBUG__ */
}
