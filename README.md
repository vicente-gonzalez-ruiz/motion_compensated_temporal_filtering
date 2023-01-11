# Motion Compensated Temporal Filtering (MCTF)

## Texture processing:

Example for 2 TRLs (Temporal Resultion Levels):
```
         +-------+------+-------+ +-----------+    +-----+--------+
         | E_1   |      |       | | L_1       |    | E_1 |        |
	 |       v      v       v |           v    |     v        v
 L_0 +-------+ +----+ +----+ +--------+     +--------+ +----+ +-------+ L_0
---->| split | | ME | | MC | | update |     | etadpu | | CM | | merge |---->
     +-------+ +----+ +----+ +--------+     +--------+ +----+ +-------+
	 |       ^      ^ |       ^              ^      ^  |      ^
	 | O_1   |      | | H_1   |              |      |  | O_1  |
	 +-------+------+ +-------+--------------+------+  +------+
		 
	 <----------- anayze_step -----------><----- synthesize_step ------>
```

## Motion processing:

Example for 4 TRLs:
```
   +---+ +---+ +---+ +---+ +---+ +---+ +---+ +---+
   |   | |   | |   | |   | |   | |   | |   | |   | M_1
   v   | |   v v   | |   v v   | |   v v   | |   v
+---+ +---+ +---+ +---+ +---+ +---+ +---+ +---+ +---+
| 0 | | 1 | | 2 | | 3 | | 4 | | 5 | | 6 | | 7 | | 8 | L_0
+---+ +---+ +---+ +---+ +---+ +---+ +---+ +---+ +---+
L_0.0

   +---------+ +---------+ +---------+ +---------+
   |         | |         | |         | |         | M_2
   v         | |         v v         | |         v
+---+       +---+       +---+       +---+       +---+
| 0 |       | 2 |       | 4 |       | 6 |       | 8 |
+---+       +---+       +---+       +---+       +---+
L_1.0       H_1.0       L_1.1       H_1.1       L_1.2

   +---------------------+ +---------------------+
   |                     | |                     | M_3
   v                     v v                     v
+---+                   +---+                   +---+
| 0 |                   | 4 |                   | 8 |
+---+                   +---+                   +---+
L_2.0                   H_2.0                   L_2.1
```

* Directory contents:

  1. `bin`: MCTF's executables.
  2. `compile`: script for creating MCTF's executables.
  3. `README.txt`: this, file.
  4. `src`: source files of MCTF.
  5. `experiments`: experiment scripts.

## Compilation and environment variable declaration:

  ```
  source ./compile
  ```

remember to define the variable MCTF and to put the dir `~/bin` at the
beggining of the PATH variable:

  ```
  export MCTF=~/MCTF-video-coding/"
  export PATH=~/bin:$PATH
  ```
  
## Configuration:

```
export MCTF_TEXTURE_CODEC="j2k"
export MCTF_MOTION_CODEC="j2k"
#export MCTF_QUANTIZER="orthogonal"
export MCTF_QUANTIZER="automatic"
```

--------------


## MCJ2K encoding/decoding:

```
export MCTF_TEXTURE_CODEC="j2k"
export MCTF_MOTION_CODEC="j2k"
#export MCTF_QUANTIZER="orthogonal"
export MCTF_QUANTIZER="automatic"
mkdir tmp
cd tmp
wget http://www.hpca.ual.es/~vruiz/videos/container_352x288x30x420x300.avi
ffmpeg -i container_352x288x30x420x300.avi container_352x288x30x420x300.yuv
ln -s container_352x288x30x420x300.yuv low_0
mctf compress --TRLs=6 --GOPs=2 --quality=0.7
mctf info --TRLs=6 --GOPs=2
mkdir tmp
mctf copy tmp
cd tmp
mctf expand --TRLs=6 --GOPs=2
mplayer low_0 -demuxer rawvideo -rawvideo cif -loop 0
```

## Quality trancoding:

  ```
  export MCTF_TEXTURE_CODEC="j2k"
  export MCTF_MOTION_CODEC="j2k"
  mkdir tmp
  cd tmp
  wget http://www.hpca.ual.es/~vruiz/videos/container_352x288x30x420x300.avi
  ffmpeg -i container_352x288x30x420x300.avi container_352x288x30x420x300.yuv
  ln -s container_352x288x30x420x300.yuv low_0
  mctf compress --TRLs=2 --GOPs=2 --motion_layers=1 --texture_layers=8
  mctf info_j2k --TRLs=2 --GOPs=2
  mkdir transcode_quality
  mctf transcode_quality --TRLs=2 --GOPs=2 --QSLs=5  --motion_layers=1 --texture_layers=8
  cd transcode_quality
  mctf info_j2k --TRLs=2 --GOPs=2
  mctf expand --TRLs=2 --GOPs=2
  mplayer low_0 -demuxer rawvideo -rawvideo cif -loop 0
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

	```
	+-------+
	| split |
	+-------+
	```

## Limitations:

The current version of MCTF has the following limitations:

  1. The number of encoded images must be a multiply of the GOP-size
     plus one. Thus, for example, if GOP-size=32, the number of
     compressed images have to be 33, 65, 97, ...

  2. The size of the images must be a multiply of the macro-block
     size. This means that, for example, if the image is 1280x720
     pixels, only up to 16x16 macro-blocks can be used.

## Acknowledgments:

The MCTF project has been supported by the Junta de Andalucía through
the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
sobre Internet" (P10-TIC-6548).
