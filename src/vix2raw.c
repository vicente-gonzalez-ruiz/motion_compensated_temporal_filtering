/**
 * \file vix2raw.c
 * 
 * \author Vicente Gonzalez-Ruiz
 * \date Last modification: 2015, January 7.
 * \brief Transforms from a type header "vix" to "raw".
 */


#include <stdio.h>

/*! \brief Buffer size */
#define BUF_SIZE 16384

/** \brief Provides a main function which reads in parameters from the command line and a parameter file.
 * \param arg The number of command line arguments of the program.
 * \param argv The contents of the command line arguments of the program.
 * \returns Notifies proper execution.
 */
int main(int arg, char *argv[]) {

  int ch;

  /** \brief Read the magic number "vix" */
  {
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif
  }
  
  /** \brief Read the video section */
  {
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif
  }
  
  /** \brief Read the color section */
  {
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif
  }
  
  /** \brief Read the image section */
  {
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif
    while((ch = getchar())!='\n') {
#if defined DEBUG
      putc(ch,stderr);
#endif
    }
#if defined DEBUG
    putc('\n',stderr);
#endif

    int x, y, c;
    scanf("%d %d %d",&x,&y,&c);
#if defined DEBUG
    fprintf(stderr,"%d %d %d\n",x,y,c);
#endif
    int i;
    for(i=0; i<c; i++) {
      int a,b;
      scanf("%d %d",&a,&b);
#if defined DEBUG
      fprintf(stderr,"%d %d\n",a,b);
#endif
    }
  }
  
  ch = getchar();
#if defined DEBUG
  putc(ch,stderr);
#endif
  
  char x[BUF_SIZE];
  for(;;) {
    int r = fread(x,sizeof(char),BUF_SIZE,stdin);
    if(r==0) break;
    fwrite(x,sizeof(char),r,stdout);
  }
}
