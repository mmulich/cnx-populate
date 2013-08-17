# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2013 Michael Mulich
# This software is subject to the provisions of the MIT License (MIT).
# See LICENCE.txt for details.
# ###
# Partial usage of the kadabra package
import magic


__all__ = ('guess_type', 'guess_encoding',)

_mime_type_magic = None
_mime_encoding_magic = None


def guess_type(buf):
    """Guesses the mime-type"""
    global _mime_type_magic
    if _mime_type_magic is None:
        _mime_type_magic = magic.Magic(mime=True)
    try:
        return _mime_type_magic.from_buffer(buf.read())
    except AttributeError:
        return _mime_type_magic.from_buffer(buf)


def guess_encoding(buf):
    """Guesses the encoding type for the given buffer."""
    global _mime_encoding_magic
    if _mime_encoding_magic is None:
        _mime_encoding_magic = magic.Magic(mime_encoding=True)
    try:
        return _mime_encoding_magic.from_buffer(buf.read())
    except AttributeError:
        return _mime_encoding_magic.from_buffer(buf)
