# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/face_geometry/proto/environment.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/tasks/cc/vision/face_geometry/proto/environment.proto',
  package='mediapipe.tasks.vision.face_geometry.proto',
  syntax='proto2',
  serialized_pb=_b('\n?mediapipe/tasks/cc/vision/face_geometry/proto/environment.proto\x12*mediapipe.tasks.vision.face_geometry.proto\"L\n\x11PerspectiveCamera\x12\x1c\n\x14vertical_fov_degrees\x18\x01 \x01(\x02\x12\x0c\n\x04near\x18\x02 \x01(\x02\x12\x0b\n\x03\x66\x61r\x18\x03 \x01(\x02\"\xc8\x01\n\x0b\x45nvironment\x12^\n\x15origin_point_location\x18\x01 \x01(\x0e\x32?.mediapipe.tasks.vision.face_geometry.proto.OriginPointLocation\x12Y\n\x12perspective_camera\x18\x02 \x01(\x0b\x32=.mediapipe.tasks.vision.face_geometry.proto.PerspectiveCamera*B\n\x13OriginPointLocation\x12\x16\n\x12\x42OTTOM_LEFT_CORNER\x10\x01\x12\x13\n\x0fTOP_LEFT_CORNER\x10\x02\x42H\n4com.google.mediapipe.tasks.vision.facegeometry.protoB\x10\x45nvironmentProto')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_ORIGINPOINTLOCATION = _descriptor.EnumDescriptor(
  name='OriginPointLocation',
  full_name='mediapipe.tasks.vision.face_geometry.proto.OriginPointLocation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BOTTOM_LEFT_CORNER', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOP_LEFT_CORNER', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=392,
  serialized_end=458,
)
_sym_db.RegisterEnumDescriptor(_ORIGINPOINTLOCATION)

OriginPointLocation = enum_type_wrapper.EnumTypeWrapper(_ORIGINPOINTLOCATION)
BOTTOM_LEFT_CORNER = 1
TOP_LEFT_CORNER = 2



_PERSPECTIVECAMERA = _descriptor.Descriptor(
  name='PerspectiveCamera',
  full_name='mediapipe.tasks.vision.face_geometry.proto.PerspectiveCamera',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vertical_fov_degrees', full_name='mediapipe.tasks.vision.face_geometry.proto.PerspectiveCamera.vertical_fov_degrees', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='near', full_name='mediapipe.tasks.vision.face_geometry.proto.PerspectiveCamera.near', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='far', full_name='mediapipe.tasks.vision.face_geometry.proto.PerspectiveCamera.far', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
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
  serialized_start=111,
  serialized_end=187,
)


_ENVIRONMENT = _descriptor.Descriptor(
  name='Environment',
  full_name='mediapipe.tasks.vision.face_geometry.proto.Environment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='origin_point_location', full_name='mediapipe.tasks.vision.face_geometry.proto.Environment.origin_point_location', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='perspective_camera', full_name='mediapipe.tasks.vision.face_geometry.proto.Environment.perspective_camera', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
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
  serialized_start=190,
  serialized_end=390,
)

_ENVIRONMENT.fields_by_name['origin_point_location'].enum_type = _ORIGINPOINTLOCATION
_ENVIRONMENT.fields_by_name['perspective_camera'].message_type = _PERSPECTIVECAMERA
DESCRIPTOR.message_types_by_name['PerspectiveCamera'] = _PERSPECTIVECAMERA
DESCRIPTOR.message_types_by_name['Environment'] = _ENVIRONMENT
DESCRIPTOR.enum_types_by_name['OriginPointLocation'] = _ORIGINPOINTLOCATION

PerspectiveCamera = _reflection.GeneratedProtocolMessageType('PerspectiveCamera', (_message.Message,), dict(
  DESCRIPTOR = _PERSPECTIVECAMERA,
  __module__ = 'mediapipe.tasks.cc.vision.face_geometry.proto.environment_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.vision.face_geometry.proto.PerspectiveCamera)
  ))
_sym_db.RegisterMessage(PerspectiveCamera)

Environment = _reflection.GeneratedProtocolMessageType('Environment', (_message.Message,), dict(
  DESCRIPTOR = _ENVIRONMENT,
  __module__ = 'mediapipe.tasks.cc.vision.face_geometry.proto.environment_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.tasks.vision.face_geometry.proto.Environment)
  ))
_sym_db.RegisterMessage(Environment)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n4com.google.mediapipe.tasks.vision.facegeometry.protoB\020EnvironmentProto'))
# @@protoc_insertion_point(module_scope)
