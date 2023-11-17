# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"
    date_appointment = fields.Date(string='Date', required=False)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,

            'date_appointment': self.date_appointment
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        # return view form python code
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'target': 'new'
        }

    # RETURN ACTION AND VIEW FROM Python Code
    def action_view_appointment(self):
        # <<======1 method==========>>>
        action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action
        # <<======2 method==========>>>
        # action = self.env['ir.actions.actions']._for_xml_id("om_hospital.action_hospital_appointment")
        # action['domain'] = [('patient_id', '=', self.patient_id.id)]
        # <<======3 method==========>>>
        # return {
        # 'type': 'ir.actions.act_window',
        # 'name': 'Appointments',
        # 'res_model': 'hospital.appointment',
        # 'view_type': 'form',
        # 'domain': [('patient_id', '=', self.patient_id.id)],
        # 'view_mode': 'tree,form',
        # 'target': 'current',
        # }
