# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2013, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
import lxml.etree


__all__ = (
    'Abstract', 'Collection', 'License', 'Metadata',
    'main',
    )


def _generate_xpath_func(xml_doc, default_namespace_name='base'):
    """Generates an easy to work with xpath function."""
    nsmap = xml_doc.nsmap.copy()
    try:
        nsmap[default_namespace_name] = nsmap.pop(None)
    except KeyError:
        # There isn't a default namespace.
        pass
    if "http://cnx.rice.edu/mdml/0.4" in nsmap.values():
        # Fixes an issue where the namespace is defined twice, once in the
        #   document tag and again in the metadata tag.
        nsmap['md4'] = "http://cnx.rice.edu/mdml/0.4"
        nsmap['md'] = "http://cnx.rice.edu/mdml"
    return lambda xpth: xml_doc.xpath(xpth, namespaces=nsmap)


class Abstract:
    """A Connexions document abstract"""
    text = ''

    def __init__(self, text=''):
        self.id = None
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<{} - [{}] '{}...'>".format(self.__class__.__name__,
                                            self.id, self.text[:10])


class License:
    """A license entry"""
    id = None
    name = None
    code = None
    version = None
    url = None

    def __init__(self, id, name, code, version, url):
        self.id = id
        self.name = name
        self.code = code
        self.version = version
        self.url = url


class Licenses:
    """A collection of ``License`` objects. This object is a singleton
    that is created at runtime. The data for this singleton is populated
    on first use. It is done this way because license data is constant.
    """

    def __init__(self):
        self._is_cached = False
        self._licenses = []

    @property  # Read-only property
    def licenses(self):
        return self._licenses

    def _populate_cache(self):
        raise NotImplemented
        self._is_cached = True

    def retrieve_by_url(self, url):
        if not self._is_cached:
            self._populate_cache()
        try:
            license = [l for l in self.licenses if l.url == url][0]
        except IndexError:
            license = None
        return license

licenses = Licenses()


class Metadata(MutableMapping):
    """A Connexions document metadata object"""
    # This ``special_attrs`` is used to specify fields outside the object's
    #   main dictionary data set.
    _special_attrs = ('abstract', 'license',)

    def __init__(self, data={}, abstract=None, license=None):
        self._data = data
        # There are two special case objects, abstract and license.
        self.abstract = abstract
        self.license = license

    @classmethod
    def from_xml(cls, xml):
        """Parse the metadata elements of an xml document."""
        xpath = _generate_xpath_func(xml)

        # Pull the abstract
        try:
            abstract = Abstract(xpath('//md:abstract/text()')[0])
        except IndexError:
            abstract = Abstract()

        # Pull the license
        try:
            license = licenses.retrieve_by_url(xpath('//md:license/@url')[0])
        except IndexError:
            raise ValueError("Missing license metadata.")

        # Pull the collection metadata
        metadata = {
            'moduleid': xpath('//md:content-id/text()')[0],
            'version': xpath('//md:version/text()')[0],
            'name': xpath('//md:title/text()')[0],
            # FIXME Don't feel like parsing the dates at the moment.
            # 'created': ?,
            # 'revised': ?,
            'doctype': '',  # Can't be null, but appears unused.
            'submitter': '',
            'submitlog': '',
            'language': xpath('//md:language/text()')[0],
            'authors': xpath('//md:roles/md:role[type="author"]/text()')[:],
            'maintainers': xpath('//md:roles/md:role[type="maintainer"]/text()')[:],
            'licensors': xpath('//md:roles/md:role[type="licensor"]/text()')[:],
            # 'parentauthors': None,
            # 'portal_type': 'Collection' or 'Module',

            # Related on insert...
            # 'parent': 1,
            # 'stateid': 1,
            # 'licenseid': 1,
            # 'abstractid': 1,
            }

        # TODO Make objects for abstract and license.
        return cls(metadata, abstract=abstract, license=license)

    # Special case field properties

    def get_abstract(self):
        return self._abstract

    def set_abstract(self, value):
        if value is not None and not isinstance(value, Abstract):
            raise ValueError("'{}' was given".format(type(value)))
        self._abstract = value

    def del_abstract(self):
        # FIXME Remove its database entry too.
        self._abstract = None

    abstract = property(get_abstract, set_abstract, del_abstract)

    def get_license(self):
        return self._license

    def set_license(self, value):
        # TODO In the follow if statement do 'and value.is_saved', because
        #      the license values are constant.
        if value is not None and not isinstance(value, License):
            raise ValueError("'{}' was given".format(type(value)))
        self._license = value

    def del_license(self):
        # FIXME Remove its database entry too.
        self._license = None

    license = property(get_license, set_license, del_license)

    # Abstract Base Class (ABC) methods

    def __getitem__(self, key):
        if key in self._special_attrs:
            value = getattr(self, key)
        else:
            value = self._data[key]
        return value

    def __setitem__(self, key, value):
        if key in self._special_attrs:
            setattr(self, key, value)
        else:
            self._data[key] = value

    def __delitem__(self, key):
        if key in self._special_attrs:
            delattr(self, key, value)
        else:
            del self._data[key]

    def __iter__(self):
        keys = list(self._special_attrs)
        keys.extend(self._data.keys())
        return iter(keys)

    def __len__(self):
        return len(self._data) + len(self._special_attrs)


class Collection:
    """A Connexions collection"""
    metadata = None

    @classmethod
    def from_file_buffer(cls, fb):
        """Initializes the class from a file buffer of a collections.xml."""
        obj = cls()
        # Parse the file buffer to an xml tree.
        xml_tree = lxml.etree.parse(fb)
        obj.metadata = Metadata.from_xml(xml_tree.getroot())

        # TODO Need file to hang off this object.

        return obj


def main(argv=None):
    """Main Command Line Interface (CLI)"""
    raise NotImplemented
