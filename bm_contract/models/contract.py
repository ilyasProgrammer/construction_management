# -*- coding: utf-8 -*-

import logging
from openerp import api, models, fields


_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = 'project.project'
    _description = 'Contract'

    bm_project_id = fields.Many2one('bm.project', string='Project')
    foremen_ids = fields.Many2many('hr.employee', string='Foremen', required=True)
    date = fields.Date(string='Date', required=True)
    start = fields.Date(string='Begin date')
    finish = fields.Date(string='End date')
    code = fields.Char(string='Номер', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contractor_id = fields.Many2one('res.partner', string='Contractor', required=True)
    estimate_ids = fields.One2many('bm.estimate', 'contract_id', string='Estimates')
    rate = fields.Float(string='Rate')
    amount = fields.Float(string='Amount')
    subject = fields.Char(string='Subject')
    type = fields.Selection([('revenue', 'Выручка'),
                             ('expense', 'Затраты'),
                             ], 'Статус', readonly=True, default='revenue')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([('draft', 'Черновик'),
                              ('signed', 'Подписан'),
                              ('canceled', 'Отменен'),
                              ], 'Статус', readonly=True, default='draft')
    # tasks_ids - in parent model


class Project(models.Model):
    _inherit = 'bm.project'

    contracts_ids = fields.One2many('project.project', 'bm_project_id', string='Contracts')


class Estimate(models.Model):
    _inherit = 'bm.estimate'

    type = fields.Selection(related='contract_id.type')


class Task(models.Model):
    _inherit = 'project.task'

    bm_project_id = fields.Many2one(related='project_id.bm_project_id')


class Report(models.Model):
    _inherit = 'bm.report'

    bm_project_id = fields.Many2one(related='task_id.bm_project_id', string='Project')