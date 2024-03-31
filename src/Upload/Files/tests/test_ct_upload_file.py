# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from Upload.Files.content.upload_file import IUploadFile  # NOQA E501
from Upload.Files.testing import UPLOAD_FILES_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class UploadFileIntegrationTest(unittest.TestCase):

    layer = UPLOAD_FILES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_upload_file_schema(self):
        fti = queryUtility(IDexterityFTI, name='Upload File')
        schema = fti.lookupSchema()
        self.assertEqual(IUploadFile, schema)

    def test_ct_upload_file_fti(self):
        fti = queryUtility(IDexterityFTI, name='Upload File')
        self.assertTrue(fti)

    def test_ct_upload_file_factory(self):
        fti = queryUtility(IDexterityFTI, name='Upload File')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IUploadFile.providedBy(obj),
            u'IUploadFile not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_upload_file_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Upload File',
            id='upload_file',
        )

        self.assertTrue(
            IUploadFile.providedBy(obj),
            u'IUploadFile not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('upload_file', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('upload_file', parent.objectIds())

    def test_ct_upload_file_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Upload File')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
