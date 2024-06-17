#!/bin/bash
set -x
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PROTO_DIR=".proto"
GEN_PY_DIR="example/generated"

rm ${GEN_PY_DIR}/*_pb2*.py*

bin/python -m grpc_tools.protoc \
  -I ${PROTO_DIR} \
  --python_out=./${GEN_PY_DIR} \
  --pyi_out=./${GEN_PY_DIR} \
  --grpc_python_out=./${GEN_PY_DIR} \
  ${PROTO_DIR}/*.proto

# fix stupid imports
SED_CMD1='s/import helloworld_pb2/from . import helloworld_pb2/g'
sed -i.bak "$SED_CMD1" "${GEN_PY_DIR}/helloworld_pb2.py"
sed -i.bak "$SED_CMD1" "${GEN_PY_DIR}/helloworld_pb2_grpc.py"

rm ${GEN_PY_DIR}/*.bak