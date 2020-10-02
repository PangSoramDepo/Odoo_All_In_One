from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class Student(models.Model):

	_name							=	"student"
	_description					=	"Student"

	name_en							=	fields.Char     ('Title', required=True)
	name_kh							=	fields.Char     ('Title', required=True)
	nickname_en						=	fields.Char     ('Title', required=True)
	nickname_kh						=	fields.Char     ('Title', required=True)
	dob								=	fields.Char     ('Title', required=True)
	gender							=	fields.Char     ('Title', required=True)
	nationality_id					=	fields.Char     ('Title', required=True)
	language_id						=	fields.Char     ('Title', required=True)
	photo							=	fields.Char     ('Title', required=True)
	address_id						=	fields.Char     ('Title', required=True)
	father_id						=	fields.Char     ('Title', required=True)
	mother_id						=	fields.Char     ('Title', required=True)
	emergency_contact_category_id	=	fields.Char     ('Title', required=True)
	student_medicine_id				=	fields.Char     ('Title', required=True)
	bulletin						=	fields.Char     ('Title', required=True)
	newsletters						=	fields.Char     ('Title', required=True)
	ads_material					=	fields.Char     ('Title', required=True)
	more_info						=	fields.Char     ('Title', required=True)
	enroll_date						=	fields.Char     ('Title', required=True)
	classtype_id					=	fields.Char     ('Title', required=True)
	class_name_id					=	fields.Char     ('Title', required=True)
	status_id						=	fields.Char     ('Title', required=True)
	school_branch_id				=	fields.Char     ('Title', required=True)
	academic_year_id				=	fields.Char     ('Title', required=True)
	grade_id						=	fields.Char     ('Title', required=True)
