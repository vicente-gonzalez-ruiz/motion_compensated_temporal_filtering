## Makefile
#  It helps build a software from its source files, a way to organize
#  code, and its compilation and linking.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

default:	all

M4 := $(shell which m4)

ifeq ($(M4),)
$(warning No m4 found!)
false
endif

CC = g++

BIN = ../bin
EXE =
#CFLAGS = -g
CFLAGS = -O3 -pipe
GCC_FLAGS = -O3 -pipe
CPP_FLAGS = -O3 -pipe
DEFS =

# Enables debug mode and send messages through stdout.
DEFS += -D DEBUG

# Write the executed commands to a trace file
#DEFS += -D TRACE

GCC_FLAGS += $(DEFS)
CPP_FLAGS += $(DEFS)

# Rules.
$(BIN)/% :: %.c
	gcc $(GCC_FLAGS) $< -o $@ -lm

$(BIN)/% :: %.cpp
	g++ $(GCC_FLAGS) $< -o $@ -lm

PYs := $(willcard *.py)

TMPs =
TMPs += $(PYs:%.py=$(BIN)/%)
#$(BIN)/%:	%.py
#	(echo "changequote({{,}})dnl"; cat $*.py) | m4 $(DEFS) > $@; chmod +x $@
$(BIN)/%:	%.py
	cp $*.py $@; chmod +x $@

$(BIN)/%.py:	%.py
	cp $*.py $@; chmod +x $@

#CPPM4s := $(wildcard *.cpp.m4)

#TMPs =
#TMPs += $(CPPM4s:%.cpp.m4=%.cpp)
#%.cpp:	%.cpp.m4
#	(echo "changequote(\`[[[', \`]]]')"; cat $*.cpp.m4) | m4 $(DEFS) > $*.cpp

$(BIN)/trace:	trace.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/trace

$(BIN)/mctf:	mctf.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/mctf

$(BIN)/mcj2k:	mcj2k.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/mcj2k

$(BIN)/mcmj2k:	mcmj2k.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/mcmj2k

$(BIN)/mcmjpeg:	mcmjpeg.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/mcmjpeg

$(BIN)/mcltw:	mcltw.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/mcltw

$(BIN)/config-hfb.txt:	config-hfb.txt
	cp $< $@
EXE	+= $(BIN)/config-hfb.txt

$(BIN)/config-lfb.txt:	config-lfb.txt
	cp $< $@
EXE	+= $(BIN)/config-lfb.txt

$(BIN)/mccp:	mccp.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
#	m4 $(DEFS) < $< > $@; chmod +x $@
EXE	+= $(BIN)/mccp

$(BIN)/vshow:	vshow.sh
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
EXE	+= $(BIN)/vshow

$(BIN)/split:	split.cpp display.cpp
	$(CC) $(CFLAGS) -D ANALYZE $< -o $@ -lm
EXE += $(BIN)/split

$(BIN)/merge:	split.cpp display.cpp
	$(CC) $(CFLAGS) $< -o $@ -lm
EXE += $(BIN)/merge

$(BIN)/motion_estimate:	motion_estimate.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp display.cpp
EXE += $(BIN)/motion_estimate

$(BIN)/decorrelate:	decorrelate.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp display.cpp entropy.o
	$(CC) $(CFLAGS) -D ANALYZE -D DEBUG $< entropy.o -o $@ -lm
EXE += $(BIN)/decorrelate

$(BIN)/correlate:	decorrelate.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp display.cpp
	$(CC) $(CFLAGS) $< -o $@ -lm
EXE += $(BIN)/correlate

$(BIN)/update:	update.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp display.cpp
	$(CC) $(CFLAGS) -D ANALYZE $< -o $@ -lm
EXE += $(BIN)/update

$(BIN)/un_update:	update.cpp Haar.cpp 5_3.cpp dwt2d.cpp texture.cpp motion.cpp display.cpp
	$(CC) $(CFLAGS) $< -o $@ -lm
EXE += $(BIN)/un_update

$(BIN)/display.py:	display.py
	(echo "changequote({{,}})dnl"; cat $<) | m4 $(DEFS) > $@; chmod +x $@
EXE += $(BIN)/display.py

$(BIN)/MCTF_parser.py:	MCTF_parser.py
EXE += $(BIN)/MCTF_parser.py

$(BIN)/analyze_step:	analyze_step.py
EXE	+= $(BIN)/analyze_step

$(BIN)/GOP.py:	GOP.py
	cp $^ $@
EXE += $(BIN)/GOP.py

$(BIN)/analyze:	analyze.py
EXE	+= $(BIN)/analyze

$(BIN)/interlevel_motion_decorrelate:	interlevel_motion_decorrelate.cpp
	$(CC) $(CFLAGS) -D ANALYZE $^ -o $@ -lm
EXE += $(BIN)/interlevel_motion_decorrelate

$(BIN)/bidirectional_motion_decorrelate: bidirectional_motion_decorrelate.cpp
	$(CC) $(CFLAGS) -D ANALYZE $^ -o $@ -lm
EXE += $(BIN)/bidirectional_motion_decorrelate

$(BIN)/motion_compress_cp:	motion_compress_cp.py
EXE	+= $(BIN)/motion_compress_cp

$(BIN)/motion_compress_j2k:	motion_compress_j2k.py
EXE	+= $(BIN)/motion_compress_j2k

$(BIN)/motion_compress_gzip:	motion_compress_gzip.py
EXE	+= $(BIN)/motion_compress_gzip

$(BIN)/interlevel_motion_correlate:	interlevel_motion_decorrelate.cpp motion.cpp
	$(CC) $(CFLAGS) $(DEFS) $< -o $@ -lm
EXE += $(BIN)/interlevel_motion_correlate

$(BIN)/bidirectional_motion_correlate: bidirectional_motion_decorrelate.cpp motion.cpp
	$(CC) $(CFLAGS) $(DEFS) $< -o $@ -lm
EXE += $(BIN)/bidirectional_motion_correlate

$(BIN)/motion_compress:	motion_compress.py
EXE	+= $(BIN)/motion_compress

#$(BIN)/texture_compress_lfb_j2k:	texture_compress_lfb_j2k.py
#EXE	+= $(BIN)/texture_compress_lfb_j2k

$(BIN)/texture_compress_fb_j2k:		texture_compress_fb_j2k.py
EXE	+= $(BIN)/texture_compress_fb_j2k

$(BIN)/texture_compress_lfb_mj2k:	texture_compress_lfb_mj2k.py
EXE	+= $(BIN)/texture_compress_lfb_mj2k

$(BIN)/texture_compress_lfb_mjpeg:	texture_compress_lfb_mjpeg.py
EXE	+= $(BIN)/texture_compress_lfb_mjpeg

$(BIN)/texture_compress_lfb_ltw:	texture_compress_lfb_ltw.py
EXE	+= $(BIN)/texture_compress_lfb_ltw

$(BIN)/texture_compress_lfb_cp:	texture_compress_lfb_cp.py
EXE	+= $(BIN)/texture_compress_lfb_cp

#$(BIN)/texture_compress_hfb_j2k:	texture_compress_hfb_j2k.py
#EXE	+= $(BIN)/texture_compress_hfb_j2k

$(BIN)/texture_compress_hfb_mj2k:	texture_compress_hfb_mj2k.py
EXE	+= $(BIN)/texture_compress_hfb_mj2k

$(BIN)/texture_compress_hfb_mjpeg:	texture_compress_hfb_mjpeg.py
EXE	+= $(BIN)/texture_compress_hfb_mjpeg

$(BIN)/texture_compress_hfb_ltw:	texture_compress_hfb_ltw.py
EXE	+= $(BIN)/texture_compress_hfb_ltw

$(BIN)/texture_compress_hfb_cp:	texture_compress_hfb_cp.py
EXE	+= $(BIN)/texture_compress_hfb_cp

$(BIN)/texture_compress:	texture_compress.py
EXE	+= $(BIN)/texture_compress

$(BIN)/compress:	compress.py
EXE	+= $(BIN)/compress

$(BIN)/synthesize_step:	synthesize_step.py
EXE	+= $(BIN)/synthesize_step

$(BIN)/synthesize:	synthesize.py
EXE	+= $(BIN)/synthesize

$(BIN)/motion_expand_cp:	motion_expand_cp.py
EXE	+= $(BIN)/motion_expand_cp

$(BIN)/motion_expand_j2k:	motion_expand_j2k.py
EXE	+= $(BIN)/motion_expand_j2k

$(BIN)/motion_expand_gzip:	motion_expand_gzip.py
EXE	+= $(BIN)/motion_expand_gzip

$(BIN)/motion_expand:	motion_expand.py
EXE	+= $(BIN)/motion_expand

#$(BIN)/texture_expand_lfb_j2k:	texture_expand_lfb_j2k.py
#EXE	+= $(BIN)/texture_expand_lfb_j2k

$(BIN)/texture_expand_fb_j2k:	texture_expand_fb_j2k.py
EXE	+= $(BIN)/texture_expand_fb_j2k

$(BIN)/texture_expand_lfb_mj2k:	texture_expand_lfb_mj2k.py
EXE	+= $(BIN)/texture_expand_lfb_mj2k

$(BIN)/texture_expand_lfb_mjpeg:	texture_expand_lfb_mjpeg.py
EXE	+= $(BIN)/texture_expand_lfb_mjpeg

$(BIN)/texture_expand_lfb_ltw:	texture_expand_lfb_ltw.py
EXE	+= $(BIN)/texture_expand_lfb_ltw

$(BIN)/texture_expand_lfb_cp:	texture_expand_lfb_cp.py
EXE	+= $(BIN)/texture_expand_lfb_cp

#$(BIN)/texture_expand_hfb_j2k:	texture_expand_hfb_j2k.py
#EXE	+= $(BIN)/texture_expand_hfb_j2k

$(BIN)/texture_expand_hfb_mj2k:	texture_expand_hfb_mj2k.py
EXE	+= $(BIN)/texture_expand_hfb_mj2k

$(BIN)/texture_expand_hfb_mjpeg:	texture_expand_hfb_mjpeg.py
EXE	+= $(BIN)/texture_expand_hfb_mjpeg

$(BIN)/texture_expand_hfb_ltw:	texture_expand_hfb_ltw.py
EXE	+= $(BIN)/texture_expand_hfb_ltw

$(BIN)/texture_expand_hfb_cp:	texture_expand_hfb_cp.py
EXE	+= $(BIN)/texture_expand_hfb_cp

$(BIN)/texture_expand:	texture_expand.py
EXE	+= $(BIN)/texture_expand

$(BIN)/expand:	expand.py
EXE	+= $(BIN)/expand

$(BIN)/info.py:
EXE	+= $(BIN)/info.py

$(BIN)/info_j2k:	$(BIN)/info.py info_j2k.py
EXE	+= $(BIN)/info_j2k

$(BIN)/info_j2k.py:	$(BIN)/info_j2k
			ln -s $(BIN)/info_j2k $(BIN)/info_j2k.py
EXE	+= $(BIN)/info_j2k.py

$(BIN)/info_mj2k:	$(BIN)/info.py info_mj2k.py
EXE	+= $(BIN)/info_mj2k

$(BIN)/info_mjpeg:	$(BIN)/info.py info_mjpeg.py
EXE	+= $(BIN)/info_mjpeg

$(BIN)/info_ltw:	$(BIN)/info.py info_ltw.py
EXE	+= $(BIN)/info_ltw

$(BIN)/info_cp:	$(BIN)/info.py info_cp.py
EXE	+= $(BIN)/info_cp

$(BIN)/psnr:	psnr.py
EXE	+= $(BIN)/psnr

#$(BIN)/snr:	snr.c
#EXE	+= $(BIN)/snr

$(BIN)/vix2raw:	vix2raw.c
EXE	+= $(BIN)/vix2raw

$(BIN)/psnr_vs_br:	psnr_vs_br.py
EXE	+= $(BIN)/psnr_vs_br

$(BIN)/transcode:	transcode.py
EXE	+= $(BIN)/transcode

$(BIN)/header_size:	header_size.c
EXE	+= $(BIN)/header_size

$(BIN)/searchSlope_byDistortion_j2k:	searchSlope_byDistortion_j2k.py
EXE	+= $(BIN)/searchSlope_byDistortion_j2k

#$(BIN)/mcj2k:	$(shell which mcj2k)
#			ln -s $< $@
#EXE	+= $(BIN)/mcj2k

#$(BIN)/mcj2k:	$(shell which mcj2k)
#			ln -s $< $@
#EXE	+= $(BIN)/mcj2k

$(BIN)/demux:	demux.c
EXE	+= $(BIN)/demux

all:	$(EXE)

objetives:
	@echo $(EXE) all clean

info:	objetives

clean:
	rm -f $(EXE) ../bin/*.pyc ../bin/*.py $(TMPs)
