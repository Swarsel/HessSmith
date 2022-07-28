\ProvidesClass{BachelorBI}[2018/01/07]

\LoadClass{scrartcl}
\KOMAoptions{
fontsize=11pt,
parskip=false,
abstract=true,
twoside,
captions=tableheading
}

\addtokomafont{captionlabel}{\bfseries}

\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
\RequirePackage[babel]{microtype}     % improves the micro-typographic layout
\RequirePackage[english,ngerman]{babel} %% englisch and austrian language

\RequirePackage{graphicx} 
%Erweiterung graphic paket, optionale Parameter für \includegraphics
% Seitenrand neu definieren
\RequirePackage[left=2.5cm,right=2.5cm,top=1.5cm,bottom=2.5cm,includehead]{geometry}
%Seitenlayout anpassen
\RequirePackage[
headsepline,
automark
]{scrlayer-scrpage} %Kopf und Fußzeile

\pagestyle{scrheadings}
\clearpairofpagestyles
\ihead{\@title}
\ohead{\thepage}


\RequirePackage{setspace}

\RequirePackage[list=true]{subcaption}

\RequirePackage{mathtools} %% extension of amsmath (also loads amstext)
\RequirePackage{amssymb}   %% for complex formulas
\RequirePackage{xfrac}  %% diagonals fractions - e.g. numbers
\RequirePackage{siunitx} %% SI Units

\RequirePackage{booktabs} %% for better looking tables 

\RequirePackage{ragged2e,tabularx}
\RequirePackage{longtable}
\RequirePackage[para,flushleft]{threeparttable}
\RequirePackage{multirow}

\RequirePackage[table]{xcolor} %% improvement to the color package
\RequirePackage{url} %% links inside the document as well as to websites

\RequirePackage{pdfpages} %% to include pdf pages

\RequirePackage{textcomp} %% additional symbols
\RequirePackage{marvosym} %% additional symbols
\RequirePackage{pifont}   %% additional symbols
\RequirePackage{eurosym} %% for correct Euro-Symbol with \officialeuro{}

\RequirePackage{xspace}  %% for intelligent spacing after commands \xspace

\RequirePackage{enumitem}  %% to customize itemize, enumerate, description

\RequirePackage{listings} %% syntax highlighting - for program code

% Eigene Sprachabhängige Begriffe
\renewcaptionname{ngerman}{\tablename}{Tab.}
\renewcaptionname{ngerman}{\figurename}{Abb.}
\renewcaptionname{ngerman}{\bibname}{Literaturverzeichnis}
\renewcaptionname{ngerman}{\abstractname}{Kurzfassung}

\renewcaptionname{english}{\tablename}{Tab.}
\renewcaptionname{english}{\figurename}{Fig.}

%% Title Format
\subject{Bachelorarbeit}
\addtokomafont{subject}{\normalfont\sffamily\huge}
\newcommand{\studentname}[1]{\renewcommand\@studentname{#1}}
\newcommand\@studentname{\@latex@error{No \noexpand\studentname specified}\@ehc}
\newcommand{\email}[1]{\renewcommand\@email{#1}}
\newcommand\@email{\@latex@error{No \noexpand\email specified}\@ehc}
\newcommand{\MatrNr}[1]{\renewcommand\@MatrNr{#1}}
\newcommand\@MatrNr{\@latex@error{No \noexpand\MatrNr specified}\@ehc}
%\title{\Titel}

%% Typografische Einstellungen zu Gleitobjekten
\renewcommand{\floatpagefraction}{0.6}
\renewcommand{\textfraction}{0.15}
\renewcommand{\topfraction}{0.8}
\renewcommand{\bottomfraction}{0.5}
\setcounter{topnumber}{3}
\setcounter{totalnumber}{5}


\author{{\normalsize \sffamily \@studentname} \\ [2mm]
         {\small \@email} \\ [-2mm]
         {\small Matr.Nr. \@MatrNr} \\ [-2mm]
         {\small Datum: \today} }
         \addtokomafont{author}{\sffamily}
\date{}
%

%% Customize Listing
\lstset{
	basicstyle = \footnotesize\ttfamily,
	keywordstyle=\color{blue}\bfseries,
	tabsize=3,
	breaklines=true,
	showstringspaces = false,
	upquote = true,
	xleftmargin=4mm,
	xrightmargin=.25in,
	aboveskip=15pt,
	belowskip=12pt,
	belowcaptionskip=12pt,
	numbers=left,
	numberstyle=\tiny,
	frame=tb,
	moredelim=**[is][\color{blue}]{@}{@}
} 
\lstset{literate=%
   {Ö}{{\"O}}1
   {Ä}{{\"A}}1
   {Ü}{{\"U}}1
   {ß}{{\ss}}1
   {ü}{{\"u}}1
   {ä}{{\"a}}1
   {ö}{{\"o}}1
}
\renewcommand{\lstlistingname}{Program Code}