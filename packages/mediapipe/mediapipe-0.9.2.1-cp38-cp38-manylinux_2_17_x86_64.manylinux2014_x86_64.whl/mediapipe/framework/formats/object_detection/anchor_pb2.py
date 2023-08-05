# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/object_detection/anchor.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/formats/object_detection/anchor.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n9mediapipe/framework/formats/object_detection/anchor.proto\x12\tmediapipe\"B\n\x06\x41nchor\x12\x10\n\x08x_center\x18\x01 \x02(\x02\x12\x10\n\x08y_center\x18\x02 \x02(\x02\x12\t\n\x01h\x18\x03 \x02(\x02\x12\t\n\x01w\x18\x04 \x02(\x02')
)




_ANCHOR = _descriptor.Descriptor(
  name='Anchor',
  full_name='mediapipe.Anchor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x_center', full_name='mediapipe.Anchor.x_center', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y_center', full_name='mediapipe.Anchor.y_center', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='h', full_name='mediapipe.Anchor.h', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='w', full_name='mediapipe.Anchor.w', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=72,
  serialized_end=138,
)

DESCRIPTOR.message_types_by_name['Anchor'] = _ANCHOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Anchor = _reflection.GeneratedProtocolMessageType('Anchor', (_message.Message,), dict(
  DESCRIPTOR = _ANCHOR,
  __module__ = 'mediapipe.framework.formats.object_detection.anchor_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.Anchor)
  ))
_sym_db.RegisterMessage(Anchor)


# @@protoc_insertion_point(module_scope)
