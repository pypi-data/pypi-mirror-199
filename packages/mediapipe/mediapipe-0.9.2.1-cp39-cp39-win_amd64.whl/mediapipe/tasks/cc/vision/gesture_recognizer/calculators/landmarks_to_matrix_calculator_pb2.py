# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/gesture_recognizer/calculators/landmarks_to_matrix_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/tasks/cc/vision/gesture_recognizer/calculators/landmarks_to_matrix_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\n]mediapipe/tasks/cc/vision/gesture_recognizer/calculators/landmarks_to_matrix_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xcf\x01\n\"LandmarksToMatrixCalculatorOptions\x12\x1c\n\x14object_normalization\x18\x01 \x01(\x08\x12-\n\"object_normalization_origin_offset\x18\x02 \x01(\x05:\x01\x30\x32\\\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xc7\xdc\xda\xe1\x01 \x01(\x0b\x32-.mediapipe.LandmarksToMatrixCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_LANDMARKSTOMATRIXCALCULATOROPTIONS = _descriptor.Descriptor(
  name='LandmarksToMatrixCalculatorOptions',
  full_name='mediapipe.LandmarksToMatrixCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object_normalization', full_name='mediapipe.LandmarksToMatrixCalculatorOptions.object_normalization', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object_normalization_origin_offset', full_name='mediapipe.LandmarksToMatrixCalculatorOptions.object_normalization_origin_offset', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.LandmarksToMatrixCalculatorOptions.ext', index=0,
      number=473345607, type=11, cpp_type=10, label=1,
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
  serialized_start=147,
  serialized_end=354,
)

DESCRIPTOR.message_types_by_name['LandmarksToMatrixCalculatorOptions'] = _LANDMARKSTOMATRIXCALCULATOROPTIONS

LandmarksToMatrixCalculatorOptions = _reflection.GeneratedProtocolMessageType('LandmarksToMatrixCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _LANDMARKSTOMATRIXCALCULATOROPTIONS,
  __module__ = 'mediapipe.tasks.cc.vision.gesture_recognizer.calculators.landmarks_to_matrix_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.LandmarksToMatrixCalculatorOptions)
  ))
_sym_db.RegisterMessage(LandmarksToMatrixCalculatorOptions)

_LANDMARKSTOMATRIXCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _LANDMARKSTOMATRIXCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_LANDMARKSTOMATRIXCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
