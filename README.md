Question classification
=======================

To run this script you need to have GloVe pre-trained word vector in text format in data folder. The file has to have number
of lines and number of vector dimensions separated by space on the first line.
The script searches for file glove.6B.50d.txt (for now).
You can run this script simply without parameters:

    python classify-question.py

DATASETS
========

The pretrained word vectors can be downloaded from this site:

    http://nlp.stanford.edu/projects/glove/

In this project, we use the one from Wikipedia 2014 with 50 dimensions.

The training and testing dataset can be downloaded from here:

    http://cogcomp.cs.illinois.edu/Data/QA/QC/