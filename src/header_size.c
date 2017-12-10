#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  FILE *f;
  int c1, c2, c3, c4;
  long cont;
  
  if (argc<2) {
    printf("\nUso: %s <archivo.j2c>\n",argv[0]);
    return 0;
  }
  
  f=fopen(argv[1],"rb");
  if (f==NULL) {
    printf("\nError al abrir el archivo: %s\n",argv[1]);
    return 0;
  }
  
  cont = 0;
  long numByte = 1;
  long startByte = -1;
  long firstByte = 0;
  long header_size = 0;
  long total = 0;
  
  while(!feof(f)) {

    c1 = fgetc(f);
    numByte++;
    if (c1==0xFF) {
      
      c2 = fgetc(f);
      numByte++;
      if (c2==0x91) {
	
	c3 = fgetc(f);
	numByte++;
	if (c3==0x00) {
	  
	  c4 = fgetc(f);
	  numByte++;
	  if (c4==0x04) {
	    
	    if (cont == 0){
	      firstByte = numByte - 4 - 1; // 4 bytes = 0xFF + 0x91 + 0x00 + 0x04
	    } else {
	      if ((numByte - startByte) == 7) {
		header_size = 7; // Empty layer header.
	      } else {
		header_size = 6; // Layer header.
	      }
	      total += header_size;
	      printf("  Packet size: %ld\tHeader size: %ld", (numByte - startByte), header_size);
	    }
	    
	    startByte = numByte;
	    
	    printf("\n%ld\tStart at Byte: %ld\t- %X %X -", cont, (numByte - 4), c1, c2); // 4 bytes = 0xFF + 0x91 + 0x00 + 0x04
	    cont++;
	    
	  }
	}
      }
    }
  }
  fclose(f);
  
  
  if ((numByte - startByte + 1) == 7) {
    header_size = 7; // Empty layer header.
  } else {
    header_size = 6; // Layer header.
  }
  total += header_size;
  printf("  Packet size: %ld\tHeader size: %ld", numByte - startByte + 1, header_size);
  
  
  printf("\n\n# SOPs: %ld", cont);
  printf("\n# Header codestream: %ld", firstByte);
  printf("\n# Header layers: %ld", total);
  printf("\n# Total headers: %ld", firstByte + total);
  printf("\nOUT %ld\n", firstByte + total + 2); // "+2" The last packet have added the item 0xFFD9 - EOC (End Of Code-stream)
  
  return 0;
}
