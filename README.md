# Experiment for Count-Distinct with WatDiv

We have to compute Distinct values vs Distinct Frequencies.

* install blazegraph
```
wget https://github.com/blazegraph/database/releases/download/BLAZEGRAPH_RELEASE_2_1_5/blazegraph.jar
```

* get WatDiv Data
```
wget http://dsg.uwaterloo.ca/watdiv/watdiv.10M.tar.bz2
tar -xvjf watdiv.10M.tar.bz2
```

* Ingest Data into Blazegraph
```
java -cp blazegraph.jar com.bigdata.rdf.store.DataLoader  config.properties watdiv.10M.nt
```

* start blazegraph server
```
java -server -Xmx4g -jar blazegraph.jar
```

* run the experiment with snakemake
```
mkdir output/cd_watdiv
snakemake
```
