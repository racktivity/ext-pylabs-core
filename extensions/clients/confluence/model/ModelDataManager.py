# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>
 
import Page
import BlogEntry
import Space
import User
import Group

class ModelDataManager(object):
    """Generic class to handle model objects save, edit... etc by calling the corresponding XMLRPC methods"""

    def __init__(self, confluenceProxy):
        """
        @param confluenceProxy: Confluence XMLRPC Proxy, a connected instance of the Confluence class
        """
        self.confluenceProxy = confluenceProxy

    def saveObject(self, obj):
        """Generic save method, saves(if no created create) all model objects by calling the corresponding XMLRPC method to persist changes on the server

        @param obj: Model object
        @return: saved Model object"""
        if isinstance(obj, Page.Page):
            if obj.id:
                obj = self.confluenceProxy.addPage(obj.space, obj.title, obj.parent, obj.content)
            else:
                obj = self.confluenceProxy.editPage(obj) #returns reference to the updated page object, will all its attributes populated
        elif isinstance(obj, Space.Space):
            obj = self.confluenceProxy.addSpace(obj.key, obj.name, obj.description)
        elif isinstance(obj, User.User):
            obj = self.confluenceProxy.addUser(obj.key, obj.name, obj.description)
        elif isinstance(obj, Group.Group):
            obj = self.confluenceProxy.addGroup(obj.name)
        elif isinstance(obj, BlogEntry.BlogEntry):
            obj = self.confluenceProxy.addBlogEntry(obj.space, obj.title, obj.content)
        return obj

    def editObject(self, obj):
        """Generic edit method, saves the edited model objects by calling the corresponding XMLRPC method to persist changes on the server

        @param obj: Model object
        @return: saved Model object"""
        if isinstance(obj, Page.Page):
            if not obj.id:
                raise ValueError('Page ID cannot be None')
            obj = self.confluenceProxy.editPage(obj) #returns reference to the updated page object, will all its attributes populated
        return obj

    def loadObject(self, obj):
        """Generic load method, loads model objects from portal by calling the corresponding XMLRPC method to extract fields on the server

        @param obj: Model object
        @return: saved Model object"""
        if isinstance(obj, Page.Page):
            if not obj.id:
                raise ValueError('Page ID cannot be None')
            obj = self.confluenceProxy.getPage(obj) #returns reference to the updated page object, will all its attributes populated
        elif isinstance(obj, Space.Space):
            obj = self.confluenceProxy.getSpace(obj.key)
        elif isinstance(obj, User.User):
            obj = self.confluenceProxy.getUser(obj)
        elif isinstance(obj, Group.Group):
            obj = self.confluenceProxy.getGroup(obj.name)
        elif isinstance(obj, BlogEntry.BlogEntry):
            obj = self.confluenceProxy.getBlogEntry(obj.id)
        return obj