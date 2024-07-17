#!/bin/sh
java -server -Xmx16g -Dcom.bigdata.journal.AbstractJournal.file=data/blazegraph.jnl -jar server/blazegraph.jar

