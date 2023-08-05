# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/annotation/locus.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework.formats.annotation import rasterization_pb2 as mediapipe_dot_framework_dot_formats_dot_annotation_dot_rasterization__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/formats/annotation/locus.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=_b('\370\001\001'),
  serialized_pb=_b('\n2mediapipe/framework/formats/annotation/locus.proto\x12\tmediapipe\x1a:mediapipe/framework/formats/annotation/rasterization.proto\"\xdf\x02\n\x05Locus\x12.\n\nlocus_type\x18\x01 \x01(\x0e\x32\x1a.mediapipe.Locus.LocusType\x12\x10\n\x08locus_id\x18\x02 \x01(\x06\x12\x15\n\rlocus_id_seed\x18\x06 \x01(\x06\x12\x1c\n\x0e\x63oncatenatable\x18\x05 \x01(\x08:\x04true\x12,\n\x0c\x62ounding_box\x18\x03 \x01(\x0b\x32\x16.mediapipe.BoundingBox\x12\x15\n\ttimestamp\x18\x07 \x01(\x05:\x02-1\x12(\n\x06region\x18\x04 \x01(\x0b\x32\x18.mediapipe.Rasterization\x12)\n\x0f\x63omponent_locus\x18\x08 \x03(\x0b\x32\x10.mediapipe.Locus\"E\n\tLocusType\x12\n\n\x06GLOBAL\x10\x01\x12\x10\n\x0c\x42OUNDING_BOX\x10\x02\x12\n\n\x06REGION\x10\x03\x12\x0e\n\nVIDEO_TUBE\x10\x04\"P\n\x0b\x42oundingBox\x12\x0e\n\x06left_x\x18\x01 \x01(\x05\x12\x0f\n\x07upper_y\x18\x02 \x01(\x05\x12\x0f\n\x07right_x\x18\x03 \x01(\x05\x12\x0f\n\x07lower_y\x18\x04 \x01(\x05\x42\x03\xf8\x01\x01')
  ,
  dependencies=[mediapipe_dot_framework_dot_formats_dot_annotation_dot_rasterization__pb2.DESCRIPTOR,])



_LOCUS_LOCUSTYPE = _descriptor.EnumDescriptor(
  name='LocusType',
  full_name='mediapipe.Locus.LocusType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GLOBAL', index=0, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOUNDING_BOX', index=1, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REGION', index=2, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_TUBE', index=3, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=408,
  serialized_end=477,
)
_sym_db.RegisterEnumDescriptor(_LOCUS_LOCUSTYPE)


_LOCUS = _descriptor.Descriptor(
  name='Locus',
  full_name='mediapipe.Locus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locus_type', full_name='mediapipe.Locus.locus_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='locus_id', full_name='mediapipe.Locus.locus_id', index=1,
      number=2, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='locus_id_seed', full_name='mediapipe.Locus.locus_id_seed', index=2,
      number=6, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='concatenatable', full_name='mediapipe.Locus.concatenatable', index=3,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bounding_box', full_name='mediapipe.Locus.bounding_box', index=4,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mediapipe.Locus.timestamp', index=5,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='region', full_name='mediapipe.Locus.region', index=6,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='component_locus', full_name='mediapipe.Locus.component_locus', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LOCUS_LOCUSTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=126,
  serialized_end=477,
)


_BOUNDINGBOX = _descriptor.Descriptor(
  name='BoundingBox',
  full_name='mediapipe.BoundingBox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='left_x', full_name='mediapipe.BoundingBox.left_x', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='upper_y', full_name='mediapipe.BoundingBox.upper_y', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='right_x', full_name='mediapipe.BoundingBox.right_x', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lower_y', full_name='mediapipe.BoundingBox.lower_y', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=479,
  serialized_end=559,
)

_LOCUS.fields_by_name['locus_type'].enum_type = _LOCUS_LOCUSTYPE
_LOCUS.fields_by_name['bounding_box'].message_type = _BOUNDINGBOX
_LOCUS.fields_by_name['region'].message_type = mediapipe_dot_framework_dot_formats_dot_annotation_dot_rasterization__pb2._RASTERIZATION
_LOCUS.fields_by_name['component_locus'].message_type = _LOCUS
_LOCUS_LOCUSTYPE.containing_type = _LOCUS
DESCRIPTOR.message_types_by_name['Locus'] = _LOCUS
DESCRIPTOR.message_types_by_name['BoundingBox'] = _BOUNDINGBOX
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Locus = _reflection.GeneratedProtocolMessageType('Locus', (_message.Message,), dict(
  DESCRIPTOR = _LOCUS,
  __module__ = 'mediapipe.framework.formats.annotation.locus_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.Locus)
  ))
_sym_db.RegisterMessage(Locus)

BoundingBox = _reflection.GeneratedProtocolMessageType('BoundingBox', (_message.Message,), dict(
  DESCRIPTOR = _BOUNDINGBOX,
  __module__ = 'mediapipe.framework.formats.annotation.locus_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.BoundingBox)
  ))
_sym_db.RegisterMessage(BoundingBox)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
