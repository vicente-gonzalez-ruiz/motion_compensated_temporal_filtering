## Makefile
#  It helps build a software from its source files, a way to organize
#  code, and its compilation and linking.

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

default:	all

M4 := $(shell which m4)

#ifeq ($(M4),)
#$(warning No m4 found!)
#false
#endif

ifeq ($(shell which g++),)
$(warning No c++ found :-/)
false
endif

CC = g++

BIN = $(HOME)/bin
MCTF_BIN = $(MCTF)/bin
EXE =
#CFLAGS = -g
#CFLAGS = -O3 -pipe
#GCC_FLAGS = -O3 -pipe
GCC_FLAGS = -g
#CPP_FLAGS = -O3 -pipe
CPP_FLAGS = -g
DEFS =
GCC_FLAGS += $(DEFS)
CPP_FLAGS += $(DEFS)

# Rules.
$(BIN)/% :: %.c
	gcc $(GCC_FLAGS) $< -o $@ -lm

$(MCTF_BIN)/% :: %.c
	gcc $(GCC_FLAGS) $< -o $@ -lm

$(BIN)/% :: %.cpp
	g++ $(CPP_FLAGS) $< -o $@ -lm

$(MCTF_BIN)/% :: %.cpp
	g++ $(CPP_FLAGS) $< -o $@ -lm

PYs := $(willcard *.py)

TMPs =
TMPs += $(PYs:%.py=$(BIN)/%)
#$(BIN)/%:	%.py
#	(echo "changequote({{,}})dnl"; cat $*.py) | m4 $(DEFS) > $@; chmod +x $@
$(BIN)/%:	%.py
	cp $*.py $@; chmod +x $@

$(MCTF_BIN)/%:	%.py
	cp $*.py $@; chmod +x $@

$(BIN)/%.py:	%.py
	cp $*.py $@; chmod +x $@

$(MCTF_BIN)/%.py:	%.py
	cp $*.py $@; chmod +x $@

$(BIN)/%:	%.sh
#	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
	cp $*.sh $@; chmod +x $@

$(MCTF_BIN)/%:	%.sh
	cp $*.sh $@; chmod +x $@

#CPPM4s := $(wildcard *.cpp.m4)

#TMPs =
#TMPs += $(CPPM4s:%.cpp.m4=%.cpp)
#%.cpp:	%.cpp.m4
#	(echo "changequote(\`[[[', \`]]]')"; cat $*.cpp.m4) | m4 $(DEFS) > $*.cpp

$(BIN)/trace:	trace.sh
EXE	+= $(BIN)/trace

$(BIN)/mctf:	mctf.sh
EXE	+= $(BIN)/mctf

#$(MCTF_BIN)/clean:	clean.sh
#EXE	+= $(MCTF_BIN)/clean

#$(MCTF_BIN)/copy:	copy.sh
#EXE	+= $(MCTF_BIN)/copy

$(MCTF_BIN)/mcj2k:	mcj2k.sh
EXE	+= $(MCTF_BIN)/mcj2k

#$(MCTF_BIN)/mcmj2k:	mcmj2k.sh
#EXE	+= $(MCTF_BIN)/mcmj2k

#$(MCTF_BIN)/mcmjpeg:	mcmjpeg.sh
#EXE	+= $(MCTF_BIN)/mcmjpeg

#$(MCTF_BIN)/mcltw:	mcltw.sh
#EXE	+= $(MCTF_BIN)/mcltw

#$(MCTF_BIN)/config-hfb.txt:	config-hfb.txt
#	cp $< $@
#EXE	+= $(MCTF_BIN)/config-hfb.txt

#$(MCTF_BIN)/config-lfb.txt:	config-lfb.txt
#	cp $< $@
#EXE	+= $(MCTF_BIN)/config-lfb.txt

#$(MCTF_BIN)/mccp:	mccp.sh
#EXE	+= $(MCTF_BIN)/mccp

#$(BIN)/vshow:	vshow.sh
#EXE	+= $(BIN)/vshow
$(MCTF_BIN)/show:	show.sh
EXE	+= $(MCTF_BIN)/show

#$(MCTF_BIN)/split:	split.cpp display.cpp
#	$(CC) $(GCC_FLAGS) -D __ANALYZE__ $< -o $@ -lm
$(MCTF_BIN)/split:	split.sh
EXE += $(MCTF_BIN)/split

#$(MCTF_BIN)/merge:	split.cpp display.cpp
#	$(CC) $(GCC_FLAGS) $< -o $@ -lm
$(MCTF_BIN)/split:	merge.sh
EXE += $(MCTF_BIN)/merge

entropy.o:	entropy.cpp entropy.h

$(MCTF_BIN)/motion_estimate:	motion_estimate.cpp display.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp common.h
EXE += $(MCTF_BIN)/motion_estimate

$(MCTF_BIN)/zoomin_imotion:	zoomin_imotion.cpp display.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp common.h
EXE += $(MCTF_BIN)/zoomin_imotion

$(MCTF_BIN)/decorrelate:	decorrelate.cpp entropy.o
	$(CC) $(CPP_FLAGS) -D __ANALYZE__ $^ -o $@ -lm
EXE += $(MCTF_BIN)/decorrelate

$(MCTF_BIN)/correlate:		decorrelate.cpp display.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp entropy.o common.h
	$(CC) $(CPP_FLAGS) $< -o $@ -lm
EXE += $(MCTF_BIN)/correlate

$(MCTF_BIN)/update:		update.cpp display.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp common.h
	$(CC) $(CPP_FLAGS) -D __ANALYZE__ $< -o $@ -lm
EXE += $(MCTF_BIN)/update

$(MCTF_BIN)/un_update:		update.cpp display.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp common.h
	$(CC) $(CPP_FLAGS) $< -o $@ -lm
EXE += $(MCTF_BIN)/un_update

$(MCTF_BIN)/interlevel_motion_decorrelate:	interlevel_motion_decorrelate.cpp display.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp
	$(CC) $(CPP_FLAGS) -D __ANALYZE__ $< -o $@ -lm
EXE += $(MCTF_BIN)/interlevel_motion_decorrelate

$(MCTF_BIN)/interlevel_motion_correlate:	interlevel_motion_decorrelate.cpp display.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp
	$(CC) $(CPP_FLAGS) $(DEFS) $< -o $@ -lm
EXE += $(MCTF_BIN)/interlevel_motion_correlate

$(MCTF_BIN)/bidirectional_motion_decorrelate:	bidirectional_motion_decorrelate.cpp motion.cpp display.cpp
	$(CC) $(CPP_FLAGS) -D __ANALYZE__ $< -o $@ -lm
EXE += $(MCTF_BIN)/bidirectional_motion_decorrelate

$(MCTF_BIN)/bidirectional_motion_correlate:	 bidirectional_motion_decorrelate.cpp motion.cpp display.cpp
	$(CC) $(CPP_FLAGS) $(DEFS) $< -o $@ -lm
EXE += $(MCTF_BIN)/bidirectional_motion_correlate

#$(MCTF_BIN)/motion_compress_cp:	motion_compress_cp.py
#EXE	+= $(MCTF_BIN)/motion_compress_cp

$(MCTF_BIN)/display.py:	display.py
EXE += $(MCTF_BIN)/display.py

$(MCTF_BIN)/defaults.py:	defaults.py
EXE += $(MCTF_BIN)/defaults.py

$(MCTF_BIN)/arguments_parser.py:	arguments_parser.py $(MCTF_BIN)/defaults.py
EXE += $(MCTF_BIN)/arguments_parser.py

$(MCTF_BIN)/analyze_step:	analyze_step.py
EXE	+= $(MCTF_BIN)/analyze_step

$(MCTF_BIN)/GOP.py:	GOP.py
	cp $^ $@
EXE += $(MCTF_BIN)/GOP.py

$(MCTF_BIN)/create_zero_texture:	create_zero_texture.py
EXE += $(MCTF_BIN)/create_zero_texture

$(MCTF_BIN)/shell.py:	shell.py
	cp $^ $@
EXE += $(MCTF_BIN)/shell.py

$(MCTF_BIN)/colorlog.py:	colorlog.py
	cp $^ $@
EXE += $(MCTF_BIN)/colorlog.py

$(MCTF_BIN)/analyze:	analyze.py
EXE	+= $(MCTF_BIN)/analyze

$(MCTF_BIN)/subband_motion_compress__j2k:	subband_motion_compress__j2k.py
EXE	+= $(MCTF_BIN)/subband_motion_compress__j2k

#$(MCTF_BIN)/motion_compress_gzip:	motion_compress_gzip.py
#EXE	+= $(MCTF_BIN)/motion_compress_gzip

$(MCTF_BIN)/motion_compress:	motion_compress.py
EXE	+= $(MCTF_BIN)/motion_compress

#$(MCTF_BIN)/texture_compress_lfb_j2k:	texture_compress_lfb_j2k.py
#EXE	+= $(MCTF_BIN)/texture_compress_lfb_j2k

$(MCTF_BIN)/subband_texture_compress__j2k:		subband_texture_compress__j2k.py
#	(echo "changequote({{,}})dnl"; cat $<) | m4 > $@; chmod +x $@
EXE	+= $(MCTF_BIN)/subband_texture_compress__j2k

#$(BIN)/texture_compress_lfb_mj2k:	texture_compress_lfb_mj2k.py
#EXE	+= $(BIN)/texture_compress_lfb_mj2k

#$(MCTF_BIN)/texture_compress_lfb_mjpeg:	texture_compress_lfb_mjpeg.py
#EXE	+= $(MCTF_BIN)/texture_compress_lfb_mjpeg

#$(MCTF_BIN)/texture_compress_lfb_ltw:	texture_compress_lfb_ltw.py
#EXE	+= $(MCTF_BIN)/texture_compress_lfb_ltw

#$(MCTF_BIN)/texture_compress_lfb_cp:	texture_compress_lfb_cp.py
#EXE	+= $(MCTF_BIN)/texture_compress_lfb_cp

#$(MCTF_BIN)/texture_compress_hfb_j2k:	texture_compress_hfb_j2k.py
#EXE	+= $(MCTF_BIN)/texture_compress_hfb_j2k

#$(MCTF_BIN)/texture_compress_hfb_mj2k:	texture_compress_hfb_mj2k.py
#EXE	+= $(MCTF_BIN)/texture_compress_hfb_mj2k

#$(MCTF_BIN)/texture_compress_hfb_mjpeg:	texture_compress_hfb_mjpeg.py
#EXE	+= $(MCTF_BIN)/texture_compress_hfb_mjpeg

#$(MCTF_BIN)/texture_compress_hfb_ltw:	texture_compress_hfb_ltw.py
#EXE	+= $(MCTF_BIN)/texture_compress_hfb_ltw

#$(MCTF_BIN)/texture_compress_hfb_cp:	texture_compress_hfb_cp.py
#EXE	+= $(MCTF_BIN)/texture_compress_hfb_cp

$(MCTF_BIN)/texture_compress__constant:	texture_compress__constant.py
EXE	+= $(MCTF_BIN)/texture_compress__constant

$(MCTF_BIN)/texture_compress__constant:	texture_compress__automatic.py
EXE	+= $(MCTF_BIN)/texture_compress__automatic

$(MCTF_BIN)/texture_compress__orthogonal:	texture_compress__orthogonal.py
EXE	+= $(MCTF_BIN)/texture_compress__orthogonal

$(MCTF_BIN)/compress:	compress.py
EXE	+= $(MCTF_BIN)/compress

#$(MCTF_BIN)/extract:	extract.py
#EXE	+= $(MCTF_BIN)/extract

$(MCTF_BIN)/synthesize_step:	synthesize_step.py
EXE	+= $(MCTF_BIN)/synthesize_step

$(MCTF_BIN)/synthesize:	synthesize.py
EXE	+= $(MCTF_BIN)/synthesize

#$(MCTF_BIN)/motion_expand_cp:	motion_expand_cp.py
#EXE	+= $(MCTF_BIN)/motion_expand_cp

$(MCTF_BIN)/subband_motion_expand__j2k:	subband_motion_expand__j2k.py
EXE	+= $(MCTF_BIN)/subband_motion_expand__j2k

#$(MCTF_BIN)/motion_expand_gzip:	motion_expand_gzip.py
#EXE	+= $(MCTF_BIN)/motion_expand_gzip

$(MCTF_BIN)/motion_expand:	motion_expand.py
EXE	+= $(MCTF_BIN)/motion_expand

#$(MCTF_BIN)/texture_expand_lfb_j2k:	texture_expand_lfb_j2k.py
#EXE	+= $(MCTF_BIN)/texture_expand_lfb_j2k

$(MCTF_BIN)/subband_texture_expand__j2k:	subband_texture_expand__j2k.py
EXE	+= $(MCTF_BIN)/subband_texture_expand__j2k

#$(MCTF_BIN)/texture_expand_lfb_mj2k:	texture_expand_lfb_mj2k.py
#EXE	+= $(MCTF_BIN)/texture_expand_lfb_mj2k

#$(MCTF_BIN)/texture_expand_lfb_mjpeg:	texture_expand_lfb_mjpeg.py
#EXE	+= $(MCTF_BIN)/texture_expand_lfb_mjpeg

#$(MCTF_BIN)/texture_expand_lfb_ltw:	texture_expand_lfb_ltw.py
#EXE	+= $(MCTF_BIN)/texture_expand_lfb_ltw

#$(MCTF_BIN)/texture_expand_lfb_cp:	texture_expand_lfb_cp.py
#EXE	+= $(MCTF_BIN)/texture_expand_lfb_cp

#$(MCTF_BIN)/texture_expand_hfb_j2k:	texture_expand_hfb_j2k.py
#EXE	+= $(MCTF_BIN)/texture_expand_hfb_j2k

#$(MCTF_BIN)/texture_expand_hfb_mj2k:	texture_expand_hfb_mj2k.py
#EXE	+= $(MCTF_BIN)/texture_expand_hfb_mj2k

#$(MCTF_BIN)/texture_expand_hfb_mjpeg:	texture_expand_hfb_mjpeg.py
#EXE	+= $(MCTF_BIN)/texture_expand_hfb_mjpeg

#$(MCTF_BIN)/texture_expand_hfb_ltw:	texture_expand_hfb_ltw.py
#EXE	+= $(MCTF_BIN)/texture_expand_hfb_ltw

#$(MCTF_BIN)/texture_expand_hfb_cp:	texture_expand_hfb_cp.py
#EXE	+= $(MCTF_BIN)/texture_expand_hfb_cp

$(MCTF_BIN)/texture_expand:	texture_expand.py
EXE	+= $(MCTF_BIN)/texture_expand

$(MCTF_BIN)/expand:	expand.py
EXE	+= $(MCTF_BIN)/expand

$(MCTF_BIN)/info:	info.py
EXE	+= $(MCTF_BIN)/info

$(MCTF_BIN)/copy:	copy.py
EXE	+= $(MCTF_BIN)/copy

#$(MCTF_BIN)/info_j2k:	$(MCTF_BIN)/info.py info_j2k.py
#EXE	+= $(MCTF_BIN)/info_j2k

#$(MCTF_BIN)/info_j2k.py:	$(MCTF_BIN)/info_j2k
#			ln -s $(MCTF_BIN)/info_j2k $(MCTF_BIN)/info_j2k.py
#EXE	+= $(MCTF_BIN)/info_j2k.py

#$(MCTF_BIN)/info_mj2k:	$(MCTF_BIN)/info.py info_mj2k.py
#EXE	+= $(MCTF_BIN)/info_mj2k

#$(MCTF_BIN)/info_mjpeg:	$(MCTF_BIN)/info.py info_mjpeg.py
#EXE	+= $(MCTF_BIN)/info_mjpeg

#$(MCTF_BIN)/info_ltw:	$(MCTF_BIN)/info.py info_ltw.py
#EXE	+= $(MCTF_BIN)/info_ltw

#$(MCTF_BIN)/info_cp:	$(MCTF_BIN)/info.py info_cp.py
#EXE	+= $(MCTF_BIN)/info_cp

$(MCTF_BIN)/psnr:	psnr.py
EXE	+= $(MCTF_BIN)/psnr

#$(BIN)/snr:	snr.c
#EXE	+= $(BIN)/snr

$(BIN)/vix2raw:	vix2raw.c
EXE	+= $(BIN)/vix2raw

$(BIN)/psnr_vs_br:	psnr_vs_br.py
EXE	+= $(BIN)/psnr_vs_br

$(MCTF_BIN)/transcode_quality_PLT:	transcode_quality_PLT.py
EXE	+= $(MCTF_BIN)/transcode_quality_PLT

$(MCTF_BIN)/transcode_quality_FSO:	transcode_quality_FSO.py
EXE	+= $(MCTF_BIN)/transcode_quality_FSO

$(MCTF_BIN)/transcode_quality_subband:	transcode_quality_subband.py
EXE	+= $(MCTF_BIN)/transcode_quality_subband

$(MCTF_BIN)/header_size:	header_size.c
EXE	+= $(MCTF_BIN)/header_size

#$(MCTF_BIN)/searchSlope_byDistortion_j2k:	searchSlope_byDistortion_j2k.py
#EXE	+= $(MCTF_BIN)/searchSlope_byDistortion_j2k

#$(MCTF_BIN)/mcj2k:	$(shell which mcj2k)
#			ln -s $< $@
#EXE	+= $(MCTF_BIN)/mcj2k

#$(MCTF_BIN)/mcj2k:	$(shell which mcj2k)
#			ln -s $< $@
#EXE	+= $(MCTF_BIN)/mcj2k

#$(BIN)/demux:	demux.c
#EXE	+= $(BIN)/demux

all:	$(EXE)

objetives:
	@echo $(EXE) all clean

info:	objetives

clean:
	rm -f $(EXE) ../bin/*.pyc ../bin/*.py $(TMPs)
