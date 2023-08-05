# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/face_landmarker/proto/tensors_to_face_landmarks_graph_options.proto

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
from mediapipe.framework import calculator_options_pb2 as mediapipe_dot_framework_dot_calculator__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/tasks/cc/vision/face_landmarker/proto/tensors_to_face_landmarks_graph_options.proto',
  package='mediapipe.tasks.vision.face_landmarker.proto',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n]mediapipe/tasks/cc/vision/face_landmarker/proto/tensors_to_face_landmarks_graph_options.proto\x12,mediapipe.tasks.vision.face_landmarker.proto\x1a$mediapipe/framework/calculator.proto\x1a,mediapipe/framework/calculator_options.proto\"\xff\x01\n\"TensorsToFaceLandmarksGraphOptions\x12!\n\x12is_attention_model\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x19\n\x11input_image_width\x18\x02 \x01(\x05\x12\x1a\n\x12input_image_height\x18\x03 \x01(\x05\x32\x7f\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x8c\xe8\x80\xf3\x01 \x01(\x0b\x32P.mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,mediapipe_dot_framework_dot_calculator__options__pb2.DESCRIPTOR,])




_TENSORSTOFACELANDMARKSGRAPHOPTIONS = _descriptor.Descriptor(
  name='TensorsToFaceLandmarksGraphOptions',
  full_name='mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_attention_model', full_name='mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions.is_attention_model', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_image_width', full_name='mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions.input_image_width', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_image_height', full_name='mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions.input_image_height', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions.ext', index=0,
      number=509621260, type=11, cpp_type=10, label=1,
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
  serialized_start=228,
  serialized_end=483,
)

DESCRIPTOR.message_types_by_name['TensorsToFaceLandmarksGraphOptions'] = _TENSORSTOFACELANDMARKSGRAPHOPTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TensorsToFaceLandmarksGraphOptions = _reflection.GeneratedProtocolMessageType('TensorsToFaceLandmarksGraphOptions', (_message.Message,), dict(
  DESCRIPTOR = _TENSORSTOFACELANDMARKSGRAPHOPTIONS,
  __module__ = 'mediapipe.tasks.cc.vision.face_landmarker.proto.tensors_to_face_landmarks_graph_options_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.vision.face_landmarker.proto.TensorsToFaceLandmarksGraphOptions)
  ))
_sym_db.RegisterMessage(TensorsToFaceLandmarksGraphOptions)

_TENSORSTOFACELANDMARKSGRAPHOPTIONS.extensions_by_name['ext'].message_type = _TENSORSTOFACELANDMARKSGRAPHOPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TENSORSTOFACELANDMARKSGRAPHOPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
