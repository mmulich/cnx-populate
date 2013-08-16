# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2013, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import os
import json
import unittest

here = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIRECTORY = os.path.join(here, 'test-data')
TEST_COLLECTION_XML = os.path.join(TEST_DATA_DIRECTORY,
                                   'collection.xml')
TEST_COLLECTION_METADATA = {
    'licensors': [],
    'name': 'Intro to Logic',
    'authors': [],
    'doctype': '',
    'language': 'en',
    'maintainers': [],
    'version': '1.20',
    'submitlog': '',
    'submitter': '',
    'moduleid': 'col10154',
    }
TEST_COLLECTION_ABSTRACT_TEXT = """\
An introduction to reasoning with propositional and first-order logic, with applications to computer science.\n\nPart of the TeachLogic Project (www.teachlogic.org).\n"""
TEST_COLLECTION_LICENSE_ID = 1


class CollectionTestCase(unittest.TestCase):
    # This test case does not concern itself with a database connection.

    def monkey_patch_licenses(self):
        import cnxpopulate as pkg  # 'import . as <name>' doesn't work. :(
        # Easy way to do this is to say that we have already cached it
        #   and set the license on the object manually.
        pkg.licenses._is_cached = True
        # Now set the licenses.
        pkg.licenses._licenses = self._get_licenses()
        # The only cleanup needed is to invalidate the cache.
        self.addCleanup(setattr, pkg.licenses, '_is_cached', False)

    def _get_licenses(self):
        licenses_filepath = os.path.join(TEST_DATA_DIRECTORY, 'licenses.json')
        with open(licenses_filepath, 'r') as f:
            data = json.load(f)

        from . import License

        deliverable = []
        for license in data:
            deliverable.append(License(**license))
        return deliverable

    def test_from_file_buffer_loads_metadata(self):
        # Case to test that a file can be loaded into the model.

        # The License collection object will need to be populated in
        #   a way that does not involve touching the database.
        self.monkey_patch_licenses()
        from . import Licenses

        # Create the object to be tested.
        from . import Collection
        with open(TEST_COLLECTION_XML, 'r') as fb:
            obj = Collection.from_file_buffer(fb)

        # Check the metadata has the data.
        metadata_wo_special_attrs = dict(obj.metadata)
        del metadata_wo_special_attrs['abstract']
        del metadata_wo_special_attrs['license']
        self.assertEqual(metadata_wo_special_attrs, TEST_COLLECTION_METADATA)
        self.assertEqual(str(obj.metadata.abstract),
                         TEST_COLLECTION_ABSTRACT_TEXT)
        self.assertEqual(obj.metadata.license.id, TEST_COLLECTION_LICENSE_ID)
