# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/holistic_landmark/calculators/roi_tracking_calculator.proto

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
  name='mediapipe/modules/holistic_landmark/calculators/roi_tracking_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\nMmediapipe/modules/holistic_landmark/calculators/roi_tracking_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xbe\x04\n\x1cRoiTrackingCalculatorOptions\x12Q\n\x10iou_requirements\x18\x01 \x01(\x0b\x32\x37.mediapipe.RoiTrackingCalculatorOptions.IouRequirements\x12S\n\x11rect_requirements\x18\x02 \x01(\x0b\x32\x38.mediapipe.RoiTrackingCalculatorOptions.RectRequirements\x12]\n\x16landmarks_requirements\x18\x03 \x01(\x0b\x32=.mediapipe.RoiTrackingCalculatorOptions.LandmarksRequirements\x1a\'\n\x0fIouRequirements\x12\x14\n\x07min_iou\x18\x01 \x01(\x02:\x03\x30.5\x1a^\n\x10RectRequirements\x12\x1c\n\x10rotation_degrees\x18\x01 \x01(\x02:\x02\x31\x30\x12\x18\n\x0btranslation\x18\x02 \x01(\x02:\x03\x30.1\x12\x12\n\x05scale\x18\x03 \x01(\x02:\x03\x30.1\x1a\x36\n\x15LandmarksRequirements\x12\x1d\n\x12recrop_rect_margin\x18\x01 \x01(\x02:\x01\x30\x32V\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x86\xa3\xad\x9d\x01 \x01(\x0b\x32\'.mediapipe.RoiTrackingCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ROITRACKINGCALCULATOROPTIONS_IOUREQUIREMENTS = _descriptor.Descriptor(
  name='IouRequirements',
  full_name='mediapipe.RoiTrackingCalculatorOptions.IouRequirements',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='min_iou', full_name='mediapipe.RoiTrackingCalculatorOptions.IouRequirements.min_iou', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.5),
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
  serialized_start=426,
  serialized_end=465,
)

_ROITRACKINGCALCULATOROPTIONS_RECTREQUIREMENTS = _descriptor.Descriptor(
  name='RectRequirements',
  full_name='mediapipe.RoiTrackingCalculatorOptions.RectRequirements',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rotation_degrees', full_name='mediapipe.RoiTrackingCalculatorOptions.RectRequirements.rotation_degrees', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(10),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='translation', full_name='mediapipe.RoiTrackingCalculatorOptions.RectRequirements.translation', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scale', full_name='mediapipe.RoiTrackingCalculatorOptions.RectRequirements.scale', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.1),
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
  serialized_start=467,
  serialized_end=561,
)

_ROITRACKINGCALCULATOROPTIONS_LANDMARKSREQUIREMENTS = _descriptor.Descriptor(
  name='LandmarksRequirements',
  full_name='mediapipe.RoiTrackingCalculatorOptions.LandmarksRequirements',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='recrop_rect_margin', full_name='mediapipe.RoiTrackingCalculatorOptions.LandmarksRequirements.recrop_rect_margin', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
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
  serialized_start=563,
  serialized_end=617,
)

_ROITRACKINGCALCULATOROPTIONS = _descriptor.Descriptor(
  name='RoiTrackingCalculatorOptions',
  full_name='mediapipe.RoiTrackingCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iou_requirements', full_name='mediapipe.RoiTrackingCalculatorOptions.iou_requirements', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rect_requirements', full_name='mediapipe.RoiTrackingCalculatorOptions.rect_requirements', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='landmarks_requirements', full_name='mediapipe.RoiTrackingCalculatorOptions.landmarks_requirements', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.RoiTrackingCalculatorOptions.ext', index=0,
      number=329994630, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[_ROITRACKINGCALCULATOROPTIONS_IOUREQUIREMENTS, _ROITRACKINGCALCULATOROPTIONS_RECTREQUIREMENTS, _ROITRACKINGCALCULATOROPTIONS_LANDMARKSREQUIREMENTS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=705,
)

_ROITRACKINGCALCULATOROPTIONS_IOUREQUIREMENTS.containing_type = _ROITRACKINGCALCULATOROPTIONS
_ROITRACKINGCALCULATOROPTIONS_RECTREQUIREMENTS.containing_type = _ROITRACKINGCALCULATOROPTIONS
_ROITRACKINGCALCULATOROPTIONS_LANDMARKSREQUIREMENTS.containing_type = _ROITRACKINGCALCULATOROPTIONS
_ROITRACKINGCALCULATOROPTIONS.fields_by_name['iou_requirements'].message_type = _ROITRACKINGCALCULATOROPTIONS_IOUREQUIREMENTS
_ROITRACKINGCALCULATOROPTIONS.fields_by_name['rect_requirements'].message_type = _ROITRACKINGCALCULATOROPTIONS_RECTREQUIREMENTS
_ROITRACKINGCALCULATOROPTIONS.fields_by_name['landmarks_requirements'].message_type = _ROITRACKINGCALCULATOROPTIONS_LANDMARKSREQUIREMENTS
DESCRIPTOR.message_types_by_name['RoiTrackingCalculatorOptions'] = _ROITRACKINGCALCULATOROPTIONS

RoiTrackingCalculatorOptions = _reflection.GeneratedProtocolMessageType('RoiTrackingCalculatorOptions', (_message.Message,), dict(

  IouRequirements = _reflection.GeneratedProtocolMessageType('IouRequirements', (_message.Message,), dict(
    DESCRIPTOR = _ROITRACKINGCALCULATOROPTIONS_IOUREQUIREMENTS,
    __module__ = 'mediapipe.modules.holistic_landmark.calculators.roi_tracking_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.RoiTrackingCalculatorOptions.IouRequirements)
    ))
  ,

  RectRequirements = _reflection.GeneratedProtocolMessageType('RectRequirements', (_message.Message,), dict(
    DESCRIPTOR = _ROITRACKINGCALCULATOROPTIONS_RECTREQUIREMENTS,
    __module__ = 'mediapipe.modules.holistic_landmark.calculators.roi_tracking_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.RoiTrackingCalculatorOptions.RectRequirements)
    ))
  ,

  LandmarksRequirements = _reflection.GeneratedProtocolMessageType('LandmarksRequirements', (_message.Message,), dict(
    DESCRIPTOR = _ROITRACKINGCALCULATOROPTIONS_LANDMARKSREQUIREMENTS,
    __module__ = 'mediapipe.modules.holistic_landmark.calculators.roi_tracking_calculator_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.RoiTrackingCalculatorOptions.LandmarksRequirements)
    ))
  ,
  DESCRIPTOR = _ROITRACKINGCALCULATOROPTIONS,
  __module__ = 'mediapipe.modules.holistic_landmark.calculators.roi_tracking_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.RoiTrackingCalculatorOptions)
  ))
_sym_db.RegisterMessage(RoiTrackingCalculatorOptions)
_sym_db.RegisterMessage(RoiTrackingCalculatorOptions.IouRequirements)
_sym_db.RegisterMessage(RoiTrackingCalculatorOptions.RectRequirements)
_sym_db.RegisterMessage(RoiTrackingCalculatorOptions.LandmarksRequirements)

_ROITRACKINGCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _ROITRACKINGCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_ROITRACKINGCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
