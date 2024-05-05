# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    nombre_jours = fields.Integer('Jours',  readonly=False)


#     def _set_price_and_tax_after_fpos(self):
#         self.ensure_one()
#         # Manage the fiscal position after that and adapt the price_unit.
#         # E.g. mapping a price-included-tax to a price-excluded-tax must
#         # remove the tax amount from the price_unit.
#         # However, mapping a price-included tax to another price-included tax must preserve the balance but
#         # adapt the price_unit to the new tax.
#         # E.g. mapping a 10% price-included tax to a 20% price-included tax for a price_unit of 110 should preserve
#         # 100 as balance but set 120 as price_unit.
#         if self.tax_ids and self.move_id.fiscal_position_id and self.move_id.fiscal_position_id.tax_ids:
#             price_subtotal = self._get_price_total_and_subtotal()['price_subtotal']
#             self.tax_ids = self.move_id.fiscal_position_id.map_tax(
#                 self.tax_ids._origin,
#                 partner=self.move_id.partner_id)
#             accounting_vals = self._get_fields_onchange_subtotal(
#                 price_subtotal=price_subtotal,
#                 currency=self.move_id.company_currency_id)
#             balance = accounting_vals['debit'] - accounting_vals['credit']
#             business_vals = self._get_fields_onchange_balance(balance=balance)
#             if 'price_unit' in business_vals:
#                 self.price_unit = business_vals['price_unit']

#             raise ValidationError(_(self.price_unit, self.nombre_jours, price_subtotal))



#     def _get_price_total_and_subtotal(self, price_unit=None,  quantity=None, discount=None, currency=None, product=None, partner=None, taxes=None, move_type=None):
#         self.ensure_one()
#         return self._get_price_total_and_subtotal_model(
#             price_unit=self.price_unit if price_unit is None else price_unit,
#             quantity=self.quantity if quantity is None else quantity,
#             discount=self.discount if discount is None else discount,
#             currency=self.currency_id if currency is None else currency,
#             product=self.product_id if product is None else product,
#             partner=self.partner_id if partner is None else partner,
#             taxes=self.tax_ids if taxes is None else taxes,
#             move_type=self.move_id.type if move_type is None else move_type,
#             # nombre_jours=self.nombre_jours if nombre_jours is None else nombre_jours,
#         )


#     @api.model
#     def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
#         ''' This method is used to compute 'price_total' & 'price_subtotal'.

#         :param price_unit:  The current price unit.
#         :param nombre_jours:The current quantity in days.
#         :param quantity:    The current quantity.
#         :param discount:    The current discount.
#         :param currency:    The line's currency.
#         :param product:     The line's product.
#         :param partner:     The line's partner.
#         :param taxes:       The applied taxes.
#         :param move_type:   The type of the move.
#         :return:            A dictionary containing 'price_subtotal' & 'price_total'.
#         '''
#         res = {}

#         # Compute 'price_subtotal'.
#         price_unit_wo_discount = (price_unit * (1 - (discount / 100.0))) 

#         #### Updated
#         subtotal = (quantity  * price_unit_wo_discount) 

#         # Compute 'price_total'.
#         if taxes:
#             taxes_res = taxes._origin.with_context(force_sign=1).compute_all(price_unit_wo_discount,
#                 quantity = quantity , currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            
#             # taxes_res['total_excluded'] = price_unit * self.nombre_jours * quantity
#             # taxes_res['total_included'] = ((price_unit * self.nombre_jours * quantity) * 0.16) +taxes_res['total_excluded']

#             res['price_subtotal'] = taxes_res['total_excluded']
#             res['price_total'] = taxes_res['total_included']

            
#         else:
#             res['price_total'] = res['price_subtotal'] = subtotal
#         #In case of multi currency, round before it's use for computing debit credit
#         if currency:
#             res = {k: currency.round(v) for k, v in res.items()}
#         return res
    
#     def _get_fields_onchange_balance(self, quantity=None, discount=None, balance=None, move_type=None, currency=None, taxes=None, price_subtotal=None, force_computation=False):
#         self.ensure_one()
#         return self._get_fields_onchange_balance_model(
#             quantity=self.quantity if quantity is None else quantity,
#             discount=self.discount if discount is None else discount,
#             balance=self.balance if balance is None else balance,
#             move_type=self.move_id.type if move_type is None else move_type,
#             currency=self.currency_id or self.move_id.currency_id if currency is None else currency,
#             taxes=self.tax_ids if taxes is None else taxes,
#             price_subtotal=self.price_subtotal if price_subtotal is None else price_subtotal,
#             force_computation=force_computation,
#         )

#     @api.model
#     def _get_fields_onchange_balance_model(self, quantity, discount, balance, move_type, currency, taxes, price_subtotal, force_computation=False):
#         ''' This method is used to recompute the values of 'quantity', 'discount', 'price_unit' due to a change made
#         in some accounting fields such as 'balance'.

#         This method is a bit complex as we need to handle some special cases.
#         For example, setting a positive balance with a 100% discount.

#         :param quantity:        The current quantity.
#         :param discount:        The current discount.
#         :param balance:         The new balance.
#         :param move_type:       The type of the move.
#         :param currency:        The currency.
#         :param taxes:           The applied taxes.
#         :param price_subtotal:  The price_subtotal.
#         :return:                A dictionary containing 'quantity', 'discount', 'price_unit'.
#         '''
#         if move_type in self.move_id.get_outbound_types():
#             sign = 1
#         elif move_type in self.move_id.get_inbound_types():
#             sign = -1
#         else:
#             sign = 1
#         balance *= sign

#         # Avoid rounding issue when dealing with price included taxes. For example, when the price_unit is 2300.0 and
#         # a 5.5% price included tax is applied on it, a balance of 2300.0 / 1.055 = 2180.094 ~ 2180.09 is computed.
#         # However, when triggering the inverse, 2180.09 + (2180.09 * 0.055) = 2180.09 + 119.90 = 2299.99 is computed.
#         # To avoid that, set the price_subtotal at the balance if the difference between them looks like a rounding
#         # issue.
#         if not force_computation and currency.is_zero(balance - price_subtotal):
#             return {}

#         taxes = taxes.flatten_taxes_hierarchy()
#         if taxes and any(tax.price_include for tax in taxes):
#             # Inverse taxes. E.g:
#             #
#             # Price Unit    | Taxes         | Originator Tax    |Price Subtotal     | Price Total
#             # -----------------------------------------------------------------------------------
#             # 110           | 10% incl, 5%  |                   | 100               | 115
#             # 10            |               | 10% incl          | 10                | 10
#             # 5             |               | 5%                | 5                 | 5
#             #
#             # When setting the balance to -200, the expected result is:
#             #
#             # Price Unit    | Taxes         | Originator Tax    |Price Subtotal     | Price Total
#             # -----------------------------------------------------------------------------------
#             # 220           | 10% incl, 5%  |                   | 200               | 230
#             # 20            |               | 10% incl          | 20                | 20
#             # 10            |               | 5%                | 10                | 10
#             force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
#             taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(balance, currency=currency, handle_price_include=False)
#             for tax_res in taxes_res['taxes']:
#                 tax = self.env['account.tax'].browse(tax_res['id'])
#                 if tax.price_include:
#                     balance += tax_res['amount']

#         discount_factor = 1 - (discount / 100.0)
#         if balance and discount_factor:
#             # discount != 100%
#             vals = {
#                 'quantity': quantity or 1.0,
#                 'price_unit': balance / discount_factor / (quantity or 1.0),
#             }
#         elif balance and not discount_factor:
#             # discount == 100%
#             vals = {
#                 'quantity': quantity or 1.0,
#                 'discount': 0.0,
#                 'price_unit': balance / (quantity or 1.0),
#             }
#         elif not discount_factor:
#             # balance of line is 0, but discount  == 100% so we display the normal unit_price
#             vals = {}
#         else:
#             # balance is 0, so unit price is 0 as well
#             vals = {'price_unit': 0.0}
#         return vals

        

#     @api.onchange('quantity', 'discount', 'price_unit', 'tax_ids','nombre_jours')
#     def _onchange_price_subtotal(self):
       
#         for line in self:
#             if not line.move_id.is_invoice(include_receipts=True):
#                 continue

#             line.update(line._get_price_total_and_subtotal())
#             line.update(line._get_fields_onchange_subtotal())



    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    nombre_jours = fields.Integer('Jours',  default=1)

    @api.depends('state', 'price_reduce', 'product_id', 'untaxed_amount_invoiced', 'qty_delivered', 'product_uom_qty','nombre_jours')
    def _compute_untaxed_amount_to_invoice(self):
        """ Total of remaining amount to invoice on the sale order line (taxes excl.) as
                total_sol - amount already invoiced
            where Total_sol depends on the invoice policy of the product.

            Note: Draft invoice are ignored on purpose, the 'to invoice' amount should
            come only from the SO lines.
        """
        for line in self:
            amount_to_invoice = 0.0
            if line.state in ['sale', 'done']:
                # Note: do not use price_subtotal field as it returns zero when the ordered quantity is
                # zero. It causes problem for expense line (e.i.: ordered qty = 0, deli qty = 4,
                # price_unit = 20 ; subtotal is zero), but when you can invoice the line, you see an
                # amount and not zero. Since we compute untaxed amount, we can use directly the price
                # reduce (to include discount) without using `compute_all()` method on taxes.
                price_subtotal = 0.0
                uom_qty_to_consider = line.qty_delivered if line.product_id.invoice_policy == 'delivery' else line.product_uom_qty
                
                ### Upadte
                price_reduce = line.price_unit * float(line.nombre_jours)  * (1 - (line.discount or 0.0) / 100.0)
                
                price_subtotal = price_reduce * uom_qty_to_consider 
                if len(line.tax_id.filtered(lambda tax: tax.price_include)) > 0:
                    # As included taxes are not excluded from the computed subtotal, `compute_all()` method
                    # has to be called to retrieve the subtotal without them.
                    # `price_reduce_taxexcl` cannot be used as it is computed from `price_subtotal` field. (see upper Note)
                    price_subtotal = line.tax_id.compute_all(
                        price_reduce = price_reduce,
                        currency=line.order_id.currency_id,
                        quantity=uom_qty_to_consider,
                        product=line.product_id,
                        partner=line.order_id.partner_shipping_id)['total_excluded']

                if any(line.invoice_lines.mapped(lambda l: l.discount != line.discount)):
                    # In case of re-invoicing with different discount we try to calculate manually the
                    # remaining amount to invoice
                    amount = 0
                    for l in line.invoice_lines:
                        if len(l.tax_ids.filtered(lambda tax: tax.price_include)) > 0:
                            amount += l.tax_ids.compute_all(l.currency_id._convert(l.price_unit* l.nombre_jours, line.currency_id, line.company_id, l.date or fields.Date.today(), round=False) * l.quantity)['total_excluded']
                        else:
                            amount += l.currency_id._convert(l.price_unit *l.nombre_jours, line.currency_id, line.company_id, l.date or fields.Date.today(), round=False) * l.quantity

                    amount_to_invoice = max(price_subtotal - amount, 0) * line.nombre_jours
                else:
                    amount_to_invoice = price_subtotal - line.untaxed_amount_invoiced * line.nombre_jours

            line.untaxed_amount_to_invoice = amount_to_invoice

    def _compute_amount_undiscounted(self):
        for order in self:
            total = 0.0
            for line in order.order_line:
                ### Updated
                total += (line.price_subtotal * 100)/(100-line.discount) if line.discount != 100 else (line.price_unit * line.product_uom_qty * line.nombre_jours)
            order.amount_undiscounted = total

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','nombre_jours')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            # compute amount total including (nombre_jours)
            price = line.price_unit  * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty * line.nombre_jours, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])


    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.
        This refers to (account.move.line)

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice * self.nombre_jours,
            'discount': self.discount,
            'price_unit': self.price_unit,
            # Add (nombre_jours)
            # 'nombre_jours':self.nombre_jours,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id if not self.display_type else False,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.display_type:
            res['account_id'] = False
        return res



