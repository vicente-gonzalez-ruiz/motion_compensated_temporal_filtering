# MCTF-video-coding

MCTF = Motion Compensated Temporal Filtering

* Directory contents:

  1. The "bin" directory which contains the MCTS's executables.

  2. The "compile" script that compiles the MCTF's executables.

  3. The "README.txt" file (this, file).

  4. The "src" directory, which stores the source files of MCTF.

## Compilation and environment variable declaration:

  ```
  source ./compile
  ```
  
## Basic MCJ2K encoding/decoding:
  ```
  mkdir tmp
  cd tmp
  ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
  mcj2k compress --TRLs=6 --GOPs=9 --quantizations="45000"
  mcj2k info --TRLs=6 --GOPs=9
  mkdir tmp
  cp *.j2c *type* tmp
  cd tmp
  mcj2k expand --TRLs=6 --GOPs=9
  mplayer low_0 -demuxer rawvideo -rawvideo cif -loop 0
  cd ../../..
  rm -rf tmp
  ```
  
## Basic MJ2K encoding/decoding (157 Kbps):
  ```
  mkdir mj2k
  cd mj2k
  ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
  mcmj2k compress --TRLs=1 --GOPs=289 --quantizations="45000"
  mcmj2k info --TRLs=1 --GOPs=289
  mkdir tmp
  cp *.mjc *type* tmp
  cd tmp
  mcmj2k expand --TRLs=1 --GOPs=289
  mplayer low_0 -demuxer rawvideo -rawvideo cif -loop 0
  cd ../../..
  rm -rf mj2k
  ```
  
## Basic MCMJ2K encoding/decoding (154 Kbps):
  ```
  mkdir mcj2k
  cd mcj2k
  ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
  mcmj2k compress --TRLs=6 --GOPs=9 --quantizations="44098"
  mcmj2k info --TRLs=6 --GOPs=9
  mkdir tmp
  cp *.mjc *type* tmp
  cd tmp
  mcmj2k expand --TRLs=6 --GOPs=9
  mplayer low_0 -demuxer rawvideo -rawvideo cif -loop 0
  cd ../../..
  rm -rf mcj2k
  ```
  
## How I can control the number of encoded frames?:
   ```
   :
   rm -f *motion*
   mcj2k compress --pictures=289
   mcj2k info --pictures=289
   mcj2k expand --pictures=289
   ```
   
## How I can define the number of quality layers?:
   ```
   :
   mcj2k compress --quantizations="44000,43500,43000 # Higher slopes,
   # worst qualities
   mcj2k info
   mcj2k expand # 44000
   mcj2k expand --layers=2 # 43500
   mcj2k expand --layers=3 # 43000
   ```
   
## How I can specify the number of temporal resolution levels?:
   ```
   :
   rm -f *motion*
   mcj2k compress --temporal_levels=6
   mcj2k info --temporal_levels=6
   mcj2k expand --temporal_levels=6
   ```
   
## Basic MCJPG encoding/decoding:
   ```
   mkdir tmp
   cd tmp
   ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
   mcjpg compress
   mcjpg info
   mkdir tmp
   cp *.mjpeg *.mjc *type* tmp
   cd tmp
   mcjpg expand
   mplayer low_0 -demuxer rawvideo -rawvideo cif -loop 0
   cd ../../..
   rm -rf tmp
   ```

## How I can define the quality of the unique layer:
   ```
   :
   mcjpg compress --slopes="25" # Higher slope, worst quality
   mcjpg info
   mcjpg expand
   ```
   
## Limitations:

The current version of MCTF has the following limitations:

  1. The number of encoded images must be a multiply of the GOP-size
     plus one. Thus, for example, if GOP-size=32, the number of
     compressed images have to be 33, 65, 97, ...

  2. The size of the images must be a multiply of the macro-block
     size. This means that, for example, if the image is 1280x720
     pixels, only up to 16x16 macro-blocks can be used.

The MCTF project has been supported by the Junta de Andalucía through
the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
sobre Internet" (P10-TIC-6548).
