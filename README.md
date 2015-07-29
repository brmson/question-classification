Question classification
=======================

To run this script you need to have GloVe pre-trained word vector in text format in data folder. The file has to have number
of lines and number of vector dimensions separated by space on the first line.
The script searches for file glove.6B.50d.txt (for now).
Before you can run the script you need to prepend line to glove.6B.50d.txt with 2 numbers. First is the number of lines in the file and 
the second is number of dimensions of the vector. For this task you can use the script:
    
    ./prepare-file.sh data/glove.6B.50d.txt 50

First parameter of the script is the file name and the second one is the number of dimension of the vector.

To run tests you should type command:

    ipython notebook

and then select classify-questions.ipynb notebook

Results
=======

The accuracy on test data set is around 72%. The question vector is computed as an average from first two words in the question.
If the first two words are "what is" then the question vector is computed as an averge over all words. The questions starting with "what"
or "what is" are hard to classify because it would need some more information about which word in question is relevant for its type.


DATASETS
========

The pretrained word vectors can be downloaded from this site:

    http://nlp.stanford.edu/projects/glove/

In this project, we use the one from Wikipedia 2014 with 50 dimensions.

The training and testing dataset can be downloaded from here:

    http://cogcomp.cs.illinois.edu/Data/QA/QC/