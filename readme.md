# basic bitcoin demo using python and flask

## run
    python app.py 5001
    python app.py 5002
    python app.py 5003

## test
    curl -X POST localhost:5001/connect_node
    curl -X POST localhost:5001/transaction
    curl -X POST localhost:5000/mine_block
    curl localhost:5000/replace_chain