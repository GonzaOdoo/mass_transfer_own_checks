from odoo import models, fields,api
from collections import defaultdict
import logging

_logger = logging.getLogger(__name__)
class InfoWizard(models.TransientModel):
    _name = 'account.check.deposit'

    check_id = fields.Many2one('account.payment',string='Cheque')
    amount = fields.Monetary('Monto',related='check_id.amount_company_currency_signed')
    currency_id = fields.Many2one(
        'res.currency',
        related='check_id.currency_id'
    )
    
    journal_id = fields.Many2one('account.journal','Diario destino',domain=[('type', '=', 'bank')])
    check_ids = fields.Many2many(
        'account.payment',
        string='Cheques a depositar',
        compute='_compute_check_ids',
        store=True,
        readonly=False
    )
    date = fields.Date('Fecha',default=fields.Date.context_today)
    
    @api.depends('check_id')
    def _compute_check_ids(self):
        for wizard in self:
            active_ids = wizard._context.get('active_ids', [])
            checks = self.env['account.payment'].browse(active_ids).filtered(
                lambda p: p.payment_method_line_id.code == 'check_printing'
                          and p.state == 'posted'
                          and p.partner_type == 'customer'
                          and not p.is_internal_transfer
                          and not p.is_move_sent
            )
            if checks:
                wizard.check_ids = [(6, 0, checks.ids)]
                # Si solo hay uno, también llenamos check_id para compatibilidad con la vista
                if len(checks) == 1:
                    wizard.check_id = checks.id
                    
    def action_deposit(self):

        if not self.journal_id:
            raise UserError("Debe seleccionar un diario de depósito.")

        for check in self.check_ids:
            # Crear la línea del extracto
            statement_line = self.env['account.bank.statement.line'].sudo().create({
                'ref': f"Depósito de cheque {check.check_number or ''} - {check.partner_id.name}",
                'date': self.date,
                'amount': check.amount_company_currency_signed,
                'payment_ref': f"Cheque {check.check_number}",
                'journal_id':self.journal_id.id,
                'partner_id': check.partner_id.id,
                'notes':'Deposito de cheque',
                'payment_ref':'Deposito de cheque',
                # Este campo es clave: enlaza con el pago (cheque)
            })
            # Marcar el cheque como depositado
            #self.check_id.write({'is_move_sent': True})
            _logger.info(statement_line.move_id.line_ids)
        
        # Retornar vista del extracto para revisión/conciliación
    


    
        