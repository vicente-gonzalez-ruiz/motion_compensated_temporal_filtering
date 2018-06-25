void info(const char *args, ...) {
#if defined (__INFO__)
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;32m");
  vfprintf(stdout, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stdout);
#endif /* __INFO__ */
}

void error(const char *args, ...) {
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;31m");
  vfprintf(stderr, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stderr);
}

void warning(const char *args, ...) {
#if defined (__WARNING__)
  va_list ap;
  va_start(ap, args);
  fprintf(stderr,"[0;33m");
  vfprintf(stderr, args, ap);
  fprintf(stderr,"[1;0m");
  fflush(stderr);
#endif /* __WARNING__ */
}

void warning_flush() {
#if defined __WARNING__
  fflush(stderr);
#endif /* __WARNING__ */
}

void info_flush() {
#if defined __INFO__
  fflush(stdout);
#endif /* __INFO__ */
}

void error_flush() {
  fflush(stderr);
}

void test_display(char *msg) {
#if defined (__DEBUG__)
  fprintf(stderr, "%s: debugging enabled\n", msg);
#endif
#if defined (__WARNING__)
  warning("%s: warnings are in yellow\n", msg);
  warning_flush();
#endif
#if defined (__INFO__)
  info("%s: infos are in green\n", msg);
  info_flush();
  error("%s: errors are in red\n", msg);
  error_flush();
#endif
}

