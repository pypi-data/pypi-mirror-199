# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/filter_detections_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/calculators/util/filter_detections_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n=mediapipe/calculators/util/filter_detections_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xc3\x01\n!FilterDetectionsCalculatorOptions\x12\x11\n\tmin_score\x18\x01 \x01(\x02\x12\x16\n\x0emin_pixel_size\x18\x02 \x01(\x02\x12\x16\n\x0emax_pixel_size\x18\x03 \x01(\x02\x32[\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xf4\x88\xca\xbc\x01 \x01(\x0b\x32,.mediapipe.FilterDetectionsCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,])




_FILTERDETECTIONSCALCULATOROPTIONS = _descriptor.Descriptor(
  name='FilterDetectionsCalculatorOptions',
  full_name='mediapipe.FilterDetectionsCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='min_score', full_name='mediapipe.FilterDetectionsCalculatorOptions.min_score', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_pixel_size', full_name='mediapipe.FilterDetectionsCalculatorOptions.min_pixel_size', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_pixel_size', full_name='mediapipe.FilterDetectionsCalculatorOptions.max_pixel_size', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.FilterDetectionsCalculatorOptions.ext', index=0,
      number=395478132, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=115,
  serialized_end=310,
)

DESCRIPTOR.message_types_by_name['FilterDetectionsCalculatorOptions'] = _FILTERDETECTIONSCALCULATOROPTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FilterDetectionsCalculatorOptions = _reflection.GeneratedProtocolMessageType('FilterDetectionsCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _FILTERDETECTIONSCALCULATOROPTIONS,
  __module__ = 'mediapipe.calculators.util.filter_detections_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.FilterDetectionsCalculatorOptions)
  ))
_sym_db.RegisterMessage(FilterDetectionsCalculatorOptions)

_FILTERDETECTIONSCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _FILTERDETECTIONSCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_FILTERDETECTIONSCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
