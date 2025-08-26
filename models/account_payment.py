from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)
class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_open_deposit_wizard(self):
        """Abre el wizard de depósito con los pagos (cheques) seleccionados."""
        payments = self.env['account.payment'].browse(self._context.get('active_ids'))

        _logger.info(payments)
        # Filtrar solo cheques válidos (no depositados, en estado 'posted', etc.)
        checks = payments.filtered(
            lambda p: p.is_matched == False
        )

        if not checks:
            raise UserError(_("No se encontraron cheques válidos para depositar."))

        # Abrir el wizard
        wizard = self.env['account.check.deposit'].create({'check_ids':checks.ids})

        # Pasar los IDs de los cheques seleccionados al contexto
        return {
            'name': _('Depositar Cheques'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.check.deposit',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
            'context': {
                'default_check_ids': checks.ids if len(checks) else False,
                'active_ids': checks.ids,
                'active_model': 'account.payment',
            },
            'views': [(False, 'form')],
        }