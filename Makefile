install-lib:
	pip install -r requirement.txt
dev:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/app.py
test-chat:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/chat.py
test-login:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/login.py
test-sign-up:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/sign_up.py
api-python:
	cd src/proto && make api-python
grpc-python:
	cd src/proto && make grpc-python
entity:
	cd src/proto && make entity
