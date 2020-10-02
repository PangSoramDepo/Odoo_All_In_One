from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class Student(models.Model):

	_name							=	"student"
	_description					=	"Student"

	name_en							=	fields.Char		('Name En')
	name_kh							=	fields.Char		('Name Kh')
	nickname_en						=	fields.Char		('Nickname En')
	nickname_kh						=	fields.Char		('Nickname Kh')
	dob								=	fields.Date		('Dob')
	gender							=	fields.Char		('Gender')
	nationality_id					=	fields.Integer	('Nationality Id')
	language_id						=	fields.Integer	('Language Id')
	photo							=	fields.Text		('Photo')
	address_id						=	fields.Integer	('Address Id')
	father_id						=	fields.Char		('Father Id')
	mother_id						=	fields.Char		('Mother Id')
	emergency_contact_category_id	=	fields.Integer	('Emergency Contact Category Id')
	student_medicine_id				=	fields.Integer	('Student Medicine Id')
	bulletin						=	fields.Boolean	('Bulletin')
	newsletters						=	fields.Boolean	('Newsletters')
	ads_material					=	fields.Boolean	('Ads Material')
	more_info						=	fields.Text		('More Info')
	enroll_date						=	fields.Date		('Enroll Date')
	classtype_id					=	fields.Integer	('Classtype Id')
	class_name_id					=	fields.Integer	('Class Name Id')
	status_id						=	fields.Integer	('Status Id')
	school_branch_id				=	fields.Integer	('School Branch Id')
	academic_year_id				=	fields.Integer	('Academic Year Id')
	grade_id						=	fields.Integer	('Grade Id')

