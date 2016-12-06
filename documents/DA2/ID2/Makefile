##
## Makefile for  in /home/eax/dev/vigilate/labeip/documents/ede
## 
## Made by eax
## Login   <soules_k@epitech.net>
## 
## Started on  Sat Jan 31 20:01:50 2015 eax
## Last update Tue Dec  6 20:16:53 2016 eax
##

LATEX	= pdflatex
MAINSRC	= 2017_ID2_vigilate.tex

TARGET	= $(MAINSRC:.tex=.pdf)

all: $(TARGET)

#this is uglyy, need to fix
$(TARGET): $(MAINSRC)
	$(LATEX) $<
	$(LATEX) $<
	$(LATEX) $<
	$(LATEX) $<

clean:
	$(RM) $(TARGET:.pdf=.aux) $(TARGET:.pdf=.toc) $(TARGET:.pdf=.log) $(TARGET:.pdf=.out) texput.log

fclean: clean
	$(RM) $(TARGET)

.PHONY: all clean fclean
