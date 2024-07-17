# Experiment for Count-Distinct with WatDiv

We have to compute Distinct values vs Distinct Frequencies.

* install blazegraph
```
wget https://github.com/blazegraph/database/releases/download/BLAZEGRAPH_2_1_6_RC/blazegraph.jar
```

* get WatDiv Data
```
wget http://dsg.uwaterloo.ca/watdiv/watdiv.10M.tar.bz2
tar -xvjf watdiv.10M.tar.bz2
```

* Ingest Data into Blazegraph
```
java -cp blazegraph.jar com.bigdata.rdf.store.DataLoader  config.properties watdiv.10M.nt
or
java -Djava.io.tmpdir=/GDD/tmp -cp blazegraph.jar com.bigdata.rdf.store.DataLoader -namespace kb -defaultGraph http://example.org/graph config.properties watdiv.10M.nt 
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

can use of https://github.com/Chat-Wane/sage-jena/tree/count_distinct/sage-blazegraph

snakemake needs pandas, need to be sure that pandas is available in the python used by snakemake, that can be different than the global python. on my mac:
```
/opt/homebrew/bin/snakemake
#!/opt/homebrew/Cellar/snakemake/8.16.0/libexec/bin/python
/opt/homebrew/Cellar/snakemake/8.16.0/libexec/bin/python -m pip install pandas
```
