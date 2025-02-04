bolt://localhost:7687

python build_up_graph.py --website bolt://localhost:7687 --user neo4j --password neo4jneo4j --dbname neo4j



ssh -L 11434:202.118.19.61:11434 mayrain@202.118.19.61



ssh -L 11434:202.118.11.9:11434 mayrain@202.118.11.9





ssh -L 11434:202.118.11.25:11434 mayrain@202.118.11.25



netsh interface portproxy add v4tov4 listenport=11434 listenaddress=0.0.0.0 connectport=11434 connectaddress=172.22.231.22 protocol=tcp