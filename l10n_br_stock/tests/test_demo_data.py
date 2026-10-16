# Copyright 2026 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDemoDataHooks(TransactionCase):
    """Test the warehouse and inventory data created by the module hooks."""

    warehouse_external_id_suffixes = (
        "",
        "_loc_stock_id",
        "_view_location",
        "_input_location",
        "_quality_control_location",
        "_pack_location",
        "_output_location",
        "_picking_type_in",
        "_picking_type_internal",
        "_pick_type_internal",
        "_pack_type_internal",
        "_picking_type_out",
    )

    def _warehouse(self, external_id):
        warehouse = self.env.ref(external_id, raise_if_not_found=False)
        self.assertTrue(warehouse, f"Warehouse {external_id} should exist")
        return warehouse

    def test_warehouse_external_ids(self):
        for company_external_id in (
            "l10n_br_base.empresa_simples_nacional",
            "l10n_br_base.empresa_lucro_presumido",
        ):
            warehouse_external_id = (
                "l10n_br_stock.wh_" + company_external_id.split(".")[1]
            )
            warehouse = self._warehouse(warehouse_external_id)
            self.assertTrue(warehouse.active)
            self.assertTrue(warehouse.lot_stock_id)
            for suffix in self.warehouse_external_id_suffixes:
                self.assertTrue(
                    self.env.ref(
                        warehouse_external_id + suffix,
                        raise_if_not_found=False,
                    ),
                    f"External ID {warehouse_external_id + suffix} should resolve",
                )

    def test_warehouse_external_id_mapping(self):
        warehouse = self._warehouse("l10n_br_stock.wh_empresa_simples_nacional")
        self.assertEqual(
            self.env.ref("l10n_br_stock.wh_empresa_simples_nacional_output_location"),
            warehouse.wh_output_stock_loc_id,
        )
        self.assertEqual(
            warehouse.company_id,
            self.env.ref("l10n_br_base.empresa_simples_nacional"),
        )

    def test_stock_quants_created(self):
        warehouse = self._warehouse("l10n_br_stock.wh_empresa_simples_nacional")
        quants = self.env["stock.quant"].search(
            [("location_id", "=", warehouse.lot_stock_id.id)]
        )
        self.assertTrue(quants)
        product = self.env.ref("product.product_product_24")
        self.assertTrue(quants.filtered(lambda quant: quant.product_id == product))

    def test_demo_shelf_locations(self):
        self.assertEqual(
            self.env.ref("l10n_br_stock.stock_location_sn_shelf_1").location_id,
            self.env.ref("l10n_br_stock.wh_empresa_simples_nacional_loc_stock_id"),
        )
        self.assertEqual(
            self.env.ref("l10n_br_stock.stock_location_lp_shelf_1").location_id,
            self.env.ref("l10n_br_stock.wh_empresa_lucro_presumido_loc_stock_id"),
        )

    def test_picking_partner_search_fields(self):
        picking = self.env["stock.picking"].new()
        self.assertIn("legal_name", picking._fields)
        self.assertIn("l10n_br_ie_code", picking._fields)

        partner = self.env.ref("l10n_br_base.res_partner_cliente1_sp")
        pickings = self.env["stock.picking"].search(
            [("legal_name", "ilike", partner.name or "")]
        )
        self.assertIsInstance(pickings, type(self.env["stock.picking"]))
