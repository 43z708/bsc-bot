# 実行(サンプル)

docker exec -it python3 python sample.py

# bsc 接続テスト

docker-compose exec python3 python bsc/bsc_test.py

# bnb 残高

docker-compose exec python3 python bsc/get_balance_bnb.py

# トークン 残高

docker-compose exec python3 python bsc/get_balance.py
