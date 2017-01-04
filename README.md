# neural-n-tree
Neural N-Tree is a tree-based neural network for cluster analysis that aims to reduce the dimensionality of high dimensional feature vectors though 2d abstraction. Neural N-Tree preserves the cluster realtionships within the inter-cluster levels and thus similar clusters (terminal nodes of Neural N-Tree) are located under the same parent node (low silhouette indexes), quite similar clusters are located under the parent of parent and so on.

Neural N-Tree ultimately is a tree, which nodes are points in the inner product space (that is a vector space with an additional structure called inner product to measure the angles between two vectors). Training Neural N-Tree adjusts the points to be more similar with a feature vectors.

Training of Neural N-Tree consists of two phases: backward training and forward training. Backward training takes place before foward training.

While consisting of the points in the inner product space, the measurement of similarity in Neural N-Tree is cosine similarity.

Neural N-Tree works best when the number of clusters is relatively large.
