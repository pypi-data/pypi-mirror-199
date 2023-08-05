# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/stream_handler/fixed_size_input_stream_handler.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import mediapipe_options_pb2 as mediapipe_dot_framework_dot_mediapipe__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/stream_handler/fixed_size_input_stream_handler.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\nHmediapipe/framework/stream_handler/fixed_size_input_stream_handler.proto\x12\tmediapipe\x1a+mediapipe/framework/mediapipe_options.proto\"\xdc\x01\n\"FixedSizeInputStreamHandlerOptions\x12\x1d\n\x12trigger_queue_size\x18\x01 \x01(\x05:\x01\x32\x12\x1c\n\x11target_queue_size\x18\x02 \x01(\x05:\x01\x31\x12\x1d\n\x0e\x66ixed_min_size\x18\x03 \x01(\x08:\x05\x66\x61lse2Z\n\x03\x65xt\x12\x1b.mediapipe.MediaPipeOptions\x18\xbf\xe9\xfa; \x01(\x0b\x32-.mediapipe.FixedSizeInputStreamHandlerOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_mediapipe__options__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_FIXEDSIZEINPUTSTREAMHANDLEROPTIONS = _descriptor.Descriptor(
  name='FixedSizeInputStreamHandlerOptions',
  full_name='mediapipe.FixedSizeInputStreamHandlerOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trigger_queue_size', full_name='mediapipe.FixedSizeInputStreamHandlerOptions.trigger_queue_size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_queue_size', full_name='mediapipe.FixedSizeInputStreamHandlerOptions.target_queue_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fixed_min_size', full_name='mediapipe.FixedSizeInputStreamHandlerOptions.fixed_min_size', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.FixedSizeInputStreamHandlerOptions.ext', index=0,
      number=125744319, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=133,
  serialized_end=353,
)

DESCRIPTOR.message_types_by_name['FixedSizeInputStreamHandlerOptions'] = _FIXEDSIZEINPUTSTREAMHANDLEROPTIONS

FixedSizeInputStreamHandlerOptions = _reflection.GeneratedProtocolMessageType('FixedSizeInputStreamHandlerOptions', (_message.Message,), dict(
  DESCRIPTOR = _FIXEDSIZEINPUTSTREAMHANDLEROPTIONS,
  __module__ = 'mediapipe.framework.stream_handler.fixed_size_input_stream_handler_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.FixedSizeInputStreamHandlerOptions)
  ))
_sym_db.RegisterMessage(FixedSizeInputStreamHandlerOptions)

_FIXEDSIZEINPUTSTREAMHANDLEROPTIONS.extensions_by_name['ext'].message_type = _FIXEDSIZEINPUTSTREAMHANDLEROPTIONS
mediapipe_dot_framework_dot_mediapipe__options__pb2.MediaPipeOptions.RegisterExtension(_FIXEDSIZEINPUTSTREAMHANDLEROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
