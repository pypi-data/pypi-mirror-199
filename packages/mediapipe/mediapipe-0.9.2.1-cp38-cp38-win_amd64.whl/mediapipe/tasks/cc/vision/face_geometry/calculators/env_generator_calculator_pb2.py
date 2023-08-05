# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/face_geometry/calculators/env_generator_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2
from mediapipe.tasks.cc.vision.face_geometry.proto import environment_pb2 as mediapipe_dot_tasks_dot_cc_dot_vision_dot_face__geometry_dot_proto_dot_environment__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/tasks/cc/vision/face_geometry/calculators/env_generator_calculator.proto',
  package='mediapipe.tasks.vision.face_geometry',
  syntax='proto2',
  serialized_pb=_b('\nRmediapipe/tasks/cc/vision/face_geometry/calculators/env_generator_calculator.proto\x12$mediapipe.tasks.vision.face_geometry\x1a,mediapipe/framework/calculator_options.proto\x1a?mediapipe/tasks/cc/vision/face_geometry/proto/environment.proto\"\xf9\x01\n)FaceGeometryEnvGeneratorCalculatorOptions\x12L\n\x0b\x65nvironment\x18\x01 \x01(\x0b\x32\x37.mediapipe.tasks.vision.face_geometry.proto.Environment2~\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x81\xbc\xb0\xf4\x01 \x01(\x0b\x32O.mediapipe.tasks.vision.face_geometry.FaceGeometryEnvGeneratorCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__options__pb2.DESCRIPTOR,mediapipe_dot_tasks_dot_cc_dot_vision_dot_face__geometry_dot_proto_dot_environment__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS = _descriptor.Descriptor(
  name='FaceGeometryEnvGeneratorCalculatorOptions',
  full_name='mediapipe.tasks.vision.face_geometry.FaceGeometryEnvGeneratorCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='environment', full_name='mediapipe.tasks.vision.face_geometry.FaceGeometryEnvGeneratorCalculatorOptions.environment', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.tasks.vision.face_geometry.FaceGeometryEnvGeneratorCalculatorOptions.ext', index=0,
      number=512499201, type=11, cpp_type=10, label=1,
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
  serialized_start=236,
  serialized_end=485,
)

_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS.fields_by_name['environment'].message_type = mediapipe_dot_tasks_dot_cc_dot_vision_dot_face__geometry_dot_proto_dot_environment__pb2._ENVIRONMENT
DESCRIPTOR.message_types_by_name['FaceGeometryEnvGeneratorCalculatorOptions'] = _FACEGEOMETRYENVGENERATORCALCULATOROPTIONS

FaceGeometryEnvGeneratorCalculatorOptions = _reflection.GeneratedProtocolMessageType('FaceGeometryEnvGeneratorCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _FACEGEOMETRYENVGENERATORCALCULATOROPTIONS,
  __module__ = 'mediapipe.tasks.cc.vision.face_geometry.calculators.env_generator_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.vision.face_geometry.FaceGeometryEnvGeneratorCalculatorOptions)
  ))
_sym_db.RegisterMessage(FaceGeometryEnvGeneratorCalculatorOptions)

_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _FACEGEOMETRYENVGENERATORCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_FACEGEOMETRYENVGENERATORCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
