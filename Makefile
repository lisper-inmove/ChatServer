dev:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/app.py
install-lib:
	pip install -r requirement.txt
test-create-message:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/create-message.py
test-login:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/login.py
test-sign-up:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/sign_up.py
test-token-authorize:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/token_authorize.py
test-stop-generate:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/tests/stop_generate.py

api:
	cd src/proto && make api-python
grpc:
	cd src/proto && make grpc-python
entity:
	cd src/proto && make entity
