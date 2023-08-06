# Ԫ������ϵ
# һ�����ŵĳ�Ϊ0.15����Ϊ0.075
# һ�����ŵĳ�����ΪԪ������ϵ��x, y�ĵ�λ����
# z��ĵ�λ������ԭ����ϵ��0.1
#
# ���λ�˷�������Ԫ����λ�ñ��뾭����������ʹԪ����������
# x, z�᲻������
# y�������Ϊ +0.045

# _elementClassHead���element_Init_HEAD�в��ִ���Ԫ������ϵ�Ĵ���
# crt_ExperimentҲ�в��ִ���

from typing import Union

### define ###

# �Ƿ�ȫ������ΪԪ������ϵ
_elementXYZ = False

@property
def elementXYZ():
    return _elementXYZ

@elementXYZ.setter
def set_elementXYZ(boolen: bool) -> None:
    if not isinstance(boolen, bool):
        raise TypeError
    global _elementXYZ
    _elementXYZ = bool(boolen)

# ��ʵ����ϵx, y, z��λ1
_xUnit = 0.16
_yUnit = 0.08
_zUnit = 0.1
# big_element��������
_xAmend = 0.04

# Ԫ������ϵԭ��
_xOrigin, _yOrigin, _zOrigin = 0, 0, 0
### end define ###

# ��Ԫ������ϵת��Ϊ��ʵ֧�ֵ�����ϵ
def xyzTranslate(x: Union[int, float], y: Union[int, float], z: Union[int, float], isBigElement = False):
    x *= _xUnit
    y *= _yUnit
    z *= _zUnit
    # �޸�Ԫ������ϵԭ��
    x += _xOrigin
    y += _yOrigin
    # �޸Ĵ�����߼���·ԭ��������
    if isBigElement:
        y += _xAmend
    return x, y, z

# ����ʵ֧�ֵ�����ϵת��ΪԪ������ϵ
def translateXYZ(x: Union[int, float], y: Union[int, float], z: Union[int, float], isBigElement = False):
    x /= _xUnit
    y /= _yUnit
    z /= _zUnit
    # �޸�Ԫ������ϵԭ��
    x -= _xOrigin
    y -= _yOrigin
    # �޸Ĵ�����߼���·ԭ��������
    if isBigElement:
        y -= _xAmend
    return x, y, z

# ����Ԫ������ϵԭ��O������ֵΪ��ʵ����ϵ
def set_O(x: Union[int, float], y: Union[int, float], z: Union[int, float]) -> None:
    if (isinstance(x, (int, float)) and
        isinstance(y, (int, float)) and
        isinstance(z, (int, float))
    ):
        global _xOrigin, _yOrigin, _zOrigin
        _xOrigin, _yOrigin, _zOrigin = x, y, z
    else:
        raise TypeError