# flajolet-martin-algorithm

This implementation is based on Flajolet-Martin algorithm as described in the paper "TRIÈST: Counting Local and Global
Triangles in Fully-Dynamic Streams with Fixed Memory Size" by De Stefani, Lorenzo & Epasto, Alessandro & Riondato, Matteo & Upfal, Eli. (2016).
The datasets are from http://konect.uni-koblenz.de/networks/facebook-wosn-links and http://konect.uni-koblenz.de/networks/maayan-faa

This implementation counts the number of triangles in a graph processed on stream with limited size.

To run either TRIEST-BASE or TRIEST-IMPR, just run the file main file. To run the TRIEST-BASE, set parameter **impr** to False. Set **impr** to True to run the TRIE-IMPR. The hyperparameters can be set on top of the file. Set **Ms** in the form of a list and switch between smaller or larger dataset with the file variable. To use the smaller dataset with 2615 edges, set the file variable to **files[1]** and **Ms** to a list of values of stream sizes to explore. Bigger dataset with 817035 edges can be selected by setting **file = files[0]**. Since the algorithm is based on randomness (seeing how the elements are removed from the stream based on values sampled from Bernoulli and uniform distribution), the final count of triangles is the average of nr_samples times of runs of the algorithm. nr_samples can also be set in the beginning of the file, for instance:
``
impr=False
nr_samples = 100
Ms= [100, 500, 1000, 1500, 2500, 3000]
```
