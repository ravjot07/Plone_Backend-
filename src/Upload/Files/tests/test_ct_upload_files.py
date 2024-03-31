# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from Upload.Files.content.upload_files import IUploadFiles  # NOQA E501
from Upload.Files.testing import UPLOAD_FILES_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class UploadFilesIntegrationTest(unittest.TestCase):

    layer = UPLOAD_FILES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_upload_files_schema(self):
        fti = queryUtility(IDexterityFTI, name='Upload Files')
        schema = fti.lookupSchema()
        self.assertEqual(IUploadFiles, schema)

    def test_ct_upload_files_fti(self):
        fti = queryUtility(IDexterityFTI, name='Upload Files')
        self.assertTrue(fti)

    def test_ct_upload_files_factory(self):
        fti = queryUtility(IDexterityFTI, name='Upload Files')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IUploadFiles.providedBy(obj),
            u'IUploadFiles not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_upload_files_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Upload Files',
            id='upload_files',
        )

        self.assertTrue(
            IUploadFiles.providedBy(obj),
            u'IUploadFiles not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('upload_files', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('upload_files', parent.objectIds())

    def test_ct_upload_files_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Upload Files')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_upload_files_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Upload Files')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'upload_files_id',
            title='Upload Files container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
