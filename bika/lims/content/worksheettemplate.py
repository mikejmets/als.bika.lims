from AccessControl import ClassSecurityInfo
from Acquisition import aq_base, aq_inner
from Products.ATExtensions.field.records import RecordsField
from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from bika.lims.browser.widgets import ServicesWidget
from bika.lims.browser.widgets import WorksheetTemplateLayoutWidget
from bika.lims.config import ANALYSIS_TYPES, I18N_DOMAIN, PROJECTNAME
from bika.lims.content.bikaschema import BikaSchema
from bika.lims import bikaMessageFactory as _

schema = BikaSchema.copy() + Schema((
    RecordsField('Row',
        required = 1,
        type = 'templateposition',
        subfields = ('pos', 'type', 'sub', 'dup'),
        required_subfields = ('pos', 'type'),
        subfield_labels = {'pos': 'Position',
                           'type': 'Type',
                           'sub': 'Subtype',
                           'dup': 'Duplicate Of'},
        widget = WorksheetTemplateLayoutWidget(
            label = _("Worksheet Layout"),
            description = _("Specify the size of the Worksheet, e.g. corresponding to a "
                            "specific instrument's tray size. Then select an Analysis 'type' "
                            "per Worksheet position. Where QC samples are selected, also select "
                            "which Reference Sample should be used. If a duplicate analysis is "
                            "selected, indicate which sample position it should be a duplicate of"),
        )
    ),
    ReferenceField('Service',
        required = 1,
        multiValued = 1,
        allowed_types = ('AnalysisService',),
        relationship = 'WorksheetTemplateAnalysisService',
        referenceClass = HoldingReference,
        widget = ServicesWidget(
            label = _("Analysis service"),
            description = _("Select which Analyses should be included on the Worksheet"),
        )
    ),
))

schema['description'].schemata = 'default'
schema['description'].widget.visible = True

class WorksheetTemplate(BaseContent):
    security = ClassSecurityInfo()
    schema = schema

    security.declarePublic('getAnalysisTypes')
    def getAnalysisTypes(self):
        """ return Analysis type displaylist """
        return ANALYSIS_TYPES

registerType(WorksheetTemplate, PROJECTNAME)
