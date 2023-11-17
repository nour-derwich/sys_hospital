# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
# Add the necessary import
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


# Define the model for HospitalPatient
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = "Hospital Patient"
    _order = "id desc"

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    # Define a unique constraint for the "name" field
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Name must be unique!')
    ]

    age = fields.Integer(string='Age', tracking=True, store=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)

    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft', string="Status",
                             tracking=True)
    image = fields.Binary(string="Patient Image")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    # Field for patient's appointments
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

    # Method to confirm a patient
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # Method to compute the number of appointments for a patient
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    # Create a new patient record with additional checks
    @api.model
    def create(self, vals):
        # Ensure the "name" field is unique
        if 'name' in vals:
            existing_record = self.search([('name', '=', vals['name'])])
            if existing_record:
                raise UserError('A patient with this name already exists!')
        # Set a default note if it's not provided
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        # Generate a unique reference for the patient
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        # Call the super method to create the patient
        res = super(HospitalPatient, self).create(vals)
        print("====>", res)
        return res

    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        res['note'] = 'NEW Patient Created'
        return res

    # @api.constrains('name')
    # def check_name(self):
    #     for rec in self:
    #         patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
    #         if patients:
    #             raise ValidationError(_("Name %s Already Exists" % rec.name))
    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Age Cannot Be Zero .. !"))

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name
            result.append((rec.id, name))
        return result

    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }
