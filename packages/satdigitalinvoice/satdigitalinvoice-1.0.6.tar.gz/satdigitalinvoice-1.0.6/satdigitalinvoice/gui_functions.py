import logging
import uuid
from datetime import datetime
from uuid import UUID

from satcfdi.create.cfd import cfdi40
from satcfdi.create.cfd.cfdi40 import Comprobante

from . import SERIE, EMISOR, LUGAR_EXPEDICION
from .file_data_managers import FacturasManager
from .mycfdi import notifications, clients, get_all_cfdi

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def create_cfdi(factura_details, serie, folio):
    cliente = clients.get(factura_details['Rfc'])
    if not cliente:
        logger.error(f"{factura_details['Rfc']}: client not found")
        return None

    invoice = cfdi40.Comprobante(
        emisor=EMISOR,
        lugar_expedicion=LUGAR_EXPEDICION,
        receptor=cfdi40.Receptor(
            rfc=factura_details['Rfc'],
            nombre=cliente['RazonSocial'],
            uso_cfdi=factura_details['UsoCFDI'],
            domicilio_fiscal_receptor=cliente['CodigoPostal'],
            regimen_fiscal_receptor=cliente['RegimenFiscal']
        ),
        metodo_pago=factura_details['MetodoPago'],
        forma_pago=factura_details['FormaPago'],
        serie=serie,
        folio=folio,
        conceptos=factura_details["Conceptos"]
    ).process()

    if factura_details['Total'] != invoice['Total']:
        logger.error(f"{factura_details['Rfc']}: Total '{factura_details['Total']}' is invalid, expected '{invoice['Total']}'")
        return None

    if invoice["MetodoPago"] == "PPD" and invoice["FormaPago"] != "99":
        logger.error(f"{factura_details['Rfc']}: FormaPago '{invoice['FormaPago']}' is invalid, expected '99' for PPD")
        return None

    for c in factura_details["Conceptos"]:
        mes_ajuste = c.get("_MesAjusteAnual")
        if not isinstance(mes_ajuste, int) or not (12 >= mes_ajuste >= 1):
            logger.error(f"{factura_details['Rfc']}: No Tiene Mes de Ajuste Anual Valido")
            return None

    return invoice


def generate_ingresos(values):
    facturas_manager = FacturasManager(values)
    facturas = facturas_manager["Facturas"]

    inicio = int(values["inicio"])
    if inicio <= 0:
        logger.error("Inicio no Valido")

    final = int(values["final"])
    if final <= 0 or final < inicio:
        logger.error("Final no Valido")

    facturas = facturas[inicio - 1:final]
    cfdis = [create_cfdi(f, SERIE, str(notifications.folio(SERIE) + i)) for i, f in enumerate(facturas)]

    if None in cfdis:
        return

    return cfdis


def find_factura(factura):
    if not factura:
        logger.error("Factura No Especificada")
        return

    try:
        factura_uuid = uuid.UUID(factura)
    except:
        factura_uuid = None

    all_invoices = get_all_cfdi()
    for i in all_invoices.values():
        if (i.name == factura or i.uuid == factura_uuid) and i["Emisor"]["Rfc"] == EMISOR.rfc:
            logger.info(f"Factura Encontrada: {i['Receptor']['Rfc']}  {i.name}  {i.uuid}  {i['Fecha']}")
            return i

    logger.info(f"Factura No Encontrada {factura}")


def parse_fecha_pago(fecha_pago):
    if not fecha_pago:
        logger.error("Fecha de Pago esta vacia")
        return

    fecha_pago = datetime.fromisoformat(fecha_pago)
    if fecha_pago > datetime.now():
        logger.error("Fecha de Pago esta en el futuro")
        return

    if fecha_pago.replace(hour=12) > datetime.now():
        fecha_pago = datetime.now()
    else:
        fecha_pago = fecha_pago.replace(hour=12)

    dif = datetime.now() - fecha_pago
    if dif.days > 30:
        logger.error("!!! FECHA DE PAGO ES MAYOR A 30 DIAS !!!")

    return fecha_pago


def pago_factura(factura_pagar, fecha_pago, forma_pago):
    if not (fecha_pago := parse_fecha_pago(fecha_pago)):
        return

    if i := find_factura(factura_pagar):
        if i["TipoDeComprobante"] != "I":
            logger.error("Comprobante a pagar no es de Ingreso")
            return

        if i["MetodoPago"] != "PPD":
            logger.error("Comprobante a pagar no es de Metodo Pago PPD")
            return

        if i.saldo_pendiente != i["Total"]:
            logger.error("Comprobante ya tiene pago anterior")
            logger.error(f"Saldo Pendiente: {i.saldo_pendiente}")
            return

        if i.estatus != "1":
            logger.error("Comprobante ya esta cancelado")
            return

        return generar_pago(cfdi=i, fecha_pago=fecha_pago, forma_pago=forma_pago)


def generar_pago(cfdi, fecha_pago, forma_pago="03"):
    pago = Comprobante.pago_comprobantes(
        emisor=EMISOR,
        lugar_expedicion=LUGAR_EXPEDICION,
        comprobantes=cfdi,
        fecha_pago=fecha_pago,
        forma_pago=forma_pago,
        serie=SERIE,
        folio=str(notifications.folio(SERIE)),
    ).process()
    return pago

# Pago Parcial
# comprobantes = [PagoComprobante(
#     comprobante=c,
#     num_parcialidad=c.ultima_num_parcialidad + 1,
#     imp_saldo_ant=c.saldo_pendiente,
#     imp_pagado=Decimal(imp_pagado)
# ) for c, imp_pagado in cfdis],
