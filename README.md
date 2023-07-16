
# Table of Contents

1.  [ChatServer](#orgff4cab2)
2.  [ChatGPTClient](#org3a5615c)
3.  [ChatClient](#org3555467)
4.  [ChatApiProtobuf](#orgfddb6f8)



<a id="orgff4cab2"></a>

# ChatServer

[ChatServer](https://github.com/lisper-inmove/ChatServer)

<p class="verse">
服务端使用Python实现的Websocket,给ChatClient提供服务以及调用ChatGPTClient的接口<br />
1. make install-lib: 安装依赖库<br />
2. make api-python: 编译proto/api下的proto<br />
3. make grpc-python: 编译proto/grpc\_api下的proto<br />
4. make entity: 编译proto/entities下的proto<br />
5. make dev: 开发模式运行<br />
</p>


<a id="org3a5615c"></a>

# ChatGPTClient

[ChatGPTClient](https://github.com/lisper-inmove/ChatGPTClient)

<p class="verse">
一个gRPC的服务,用于对接chatgpt的api<br />
1. make install-lib<br />
2. make grpc-python<br />
3. make dev<br />
</p>


<a id="org3555467"></a>

# ChatClient

[ChatClient](https://github.com/lisper-inmove/ChatClient)

<p class="verse">
用Typescript实现的前端页面<br />
1. npm i<br />
2. make api-typescript<br />
3. make entity-typescript<br />
4. npm run dev<br />
</p>


<a id="orgfddb6f8"></a>

# ChatApiProtobuf

[ChatApiProtobuf](https://github.com/lisper-inmove/ChatApiProtobuf)

<p class="verse">
用于保存protobuf相关的文件,包括api,grpc以及实体对象。<br />
作为上面三个项目的子模块存在<br />
</p>
