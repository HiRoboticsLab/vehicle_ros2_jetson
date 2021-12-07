# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wxmp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='wxmp.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\nwxmp.proto\"\x0f\n\rRequestParams\"\x10\n\x0eResponseParams2/\n\x04WXMP\x12\'\n\x04\x63trl\x12\x0e.RequestParams\x1a\x0f.ResponseParamsb\x06proto3'
)




_REQUESTPARAMS = _descriptor.Descriptor(
  name='RequestParams',
  full_name='RequestParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=29,
)


_RESPONSEPARAMS = _descriptor.Descriptor(
  name='ResponseParams',
  full_name='ResponseParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=47,
)

DESCRIPTOR.message_types_by_name['RequestParams'] = _REQUESTPARAMS
DESCRIPTOR.message_types_by_name['ResponseParams'] = _RESPONSEPARAMS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestParams = _reflection.GeneratedProtocolMessageType('RequestParams', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTPARAMS,
  '__module__' : 'wxmp_pb2'
  # @@protoc_insertion_point(class_scope:RequestParams)
  })
_sym_db.RegisterMessage(RequestParams)

ResponseParams = _reflection.GeneratedProtocolMessageType('ResponseParams', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSEPARAMS,
  '__module__' : 'wxmp_pb2'
  # @@protoc_insertion_point(class_scope:ResponseParams)
  })
_sym_db.RegisterMessage(ResponseParams)



_WXMP = _descriptor.ServiceDescriptor(
  name='WXMP',
  full_name='WXMP',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=49,
  serialized_end=96,
  methods=[
  _descriptor.MethodDescriptor(
    name='ctrl',
    full_name='WXMP.ctrl',
    index=0,
    containing_service=None,
    input_type=_REQUESTPARAMS,
    output_type=_RESPONSEPARAMS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WXMP)

DESCRIPTOR.services_by_name['WXMP'] = _WXMP

# @@protoc_insertion_point(module_scope)
