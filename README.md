# AOS_6_project
Classification and estimation in the Stochastic Blockmodel based on the empirical degrees

# Important !
This version of the project is the one presented in AOS6 Article session
So it only contains the partition problem and not the model selection and pi 
estimation (which is easy to compute giving the classes estimation, but I only
upload what I have shown in class)
To retrieve the article session version run thoses command in your shell (from the root of the project):
 -python live_demo.py n
 -python live_demo_2.py n
 with n the number of nodes.

You will remark that U need almost 2 or 3 times more nodes for the second run to have
the true partition than for the first run while the only change between the 2 runs
is the value of pi[1,3] = pi[3,1] which changes from 0.08 to 0.016.

For now did not manage to implement the EM algorithm, I've taken the implementation from a friend
of mine (in the RunEm class, in Run.py file) but it does not work well for all instances, so the run SBM_degree.py will not work, it's pointless to use it.

# How to make your own run
1) Specify the rates of classes and likelihood matrix as in live_demo.py
2) Instanciate SBM using SbmModel class from the parameters above
3) Instanciate a graph generator using SbmGraphGenerator class using the SBM model
4) Generate a graph g, giving n number of nodes, using generate_sbmgraph method
5) Instanciate an instance of RunLgMethod class, giving a graph g
6) Use the compute method from RunLgMethod class, giving the class number as parameters
7) Instanciate an instance of ResultAnalyzer class, giving the model, adjacency matrix,
classes from g and result of the previous run
8) Use the method class_count() from ResultAnalyzer class, that gives the true and estimated
partition

or 

1) Just modify the rates vector and likelihood matrix in live_demo.py as u wish

# Future updates (in the next days/weeks/months/lifes)
 -Pi matrix estimation
 -Comparison with EM Algorithms
 -Save/load run results
 -Few algorithm optimization 
 -Big algorithm optimization by using a different data structure to represent edges

Let's keep in touch ! https://github.com/Isma-mz/AOS_6_project
