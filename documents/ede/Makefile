##
## Makefile for  in /home/eax/dev/vigilate/labeip/documents/ede
## 
## Made by eax
## Login   <soules_k@epitech.net>
## 
## Started on  Sat Jan 31 20:01:50 2015 eax
## Last update Tue Nov 17 14:52:52 2015 
##

LATEX	= pdflatex
MAINSRC	= 2017_EDE_vigilate.tex

TARGET	= $(MAINSRC:.tex=.pdf)

all: $(TARGET)

$(TARGET): $(MAINSRC)
	$(LATEX) $<

clean:
	$(RM) $(TARGET:.pdf=.aux) $(TARGET:.pdf=.toc) $(TARGET:.pdf=.log) $(TARGET:.pdf=.out) texput.log

fclean: clean
	$(RM) $(TARGET)

.PHONY: all clean fclean
