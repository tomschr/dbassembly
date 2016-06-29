#
# Copyright (c) 2016 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of dbassembly.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com


class BaseAssemblyError(Exception):
    """
    Base class to handle all known exceptions.

    Specific exceptions are implemented as sub classes of :py:class:`DBAssemblyError`.

    Attributes

    * :attr:`message`
        Exception message text
    """
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(args, kwargs)

    def __str__(self):
        return format(self.message)


class NoAssemblyFileError(FileNotFoundError):
    """Error raised when there is no assembly file found"""
    pass


class MissingAttributeRessource(BaseAssemblyError):
    """Error raised when an expected attribute is not available"""
    pass


class NoStructure(BaseAssemblyError):
    """Error raised when no <structure> element found inside <assembly>"""
    pass


class ResourceNotFoundError(BaseAssemblyError):
    """Error raised when the referenced resource was not found"""
    pass


class NoResultDocumentError(BaseAssemblyError):
    """Error raised when no result document is created"""
    pass
