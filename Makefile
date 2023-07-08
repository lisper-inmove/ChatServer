dev:
	export PYTHONPATH=`pwd`/src:`pwd`/src/proto/grpc_api && source bin/util.sh && python src/app.py
test-chat:
	export PYTHONPATH=`pwd`/src && python src/tests/chat.py
test-login:
	export PYTHONPATH=`pwd`/src && python src/tests/login.py
test-sign-up:
	export PYTHONPATH=`pwd`/src && python src/tests/sign_up.py
