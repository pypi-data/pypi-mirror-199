"""Test cases for the __helpers__ module."""

import os
from pathlib import Path
from typing import List

import pytest
from lxml import etree, objectify

from lxmlh import (
    create_attribute,
    create_attribute_list,
    create_element_text,
    fill_in_defaults,
    get_element,
    get_element_list,
    get_inner_text_list,
)


@pytest.fixture(name="ship_order")
def __ship_order() -> etree.ElementTree:
    dataDir = os.path.join(Path(__file__).parent.parent.resolve(), "data")
    sampleFile = os.path.join(dataDir, "sample.xml")
    schemaFile = os.path.join(dataDir, "schema.xsd")

    class _ShipTo(etree.ElementBase):
        name = create_element_text("name", str, schemaFile)
        address = create_element_text("address", str, schemaFile)
        city = create_element_text("city", str, schemaFile)
        country = create_element_text("country", str, schemaFile)

    class _Item(etree.ElementBase):
        @property
        def notes(self) -> List[str]:
            """Notes."""
            return get_inner_text_list(self, "note")

    class _ShipOrder(etree.ElementBase):
        orderId = create_attribute("orderid", str, schemaFile, lambda orderId: orderId)
        orderStatus = create_attribute("orderstatus", str, schemaFile, None)
        orderTime = create_attribute("ordertime", str, schemaFile, None)
        orderPerson = create_element_text("orderperson", str, schemaFile)
        discounts = create_attribute_list("discount", int, schemaFile)

        @property
        def shipTo(self) -> "_ShipTo":
            """Inner shipto element"""
            return get_element(self, "shipto")

        @property
        def itemsList(self) -> List["_Item"]:
            "Items."
            return get_element_list(self, "item")

    class _Lookup(etree.CustomElementClassLookup):
        def lookup(self, unused_node_type, unused_document, unused_namespace, name):
            """Maps XML elements to custom classes."""
            lookupMap = {
                "item": _Item,
                "shiporder": _ShipOrder,
                "shipto": _ShipTo,
            }
            try:
                return lookupMap[name]
            except KeyError:
                return None

    parser = objectify.makeparser(schema=etree.XMLSchema(file=schemaFile))
    parser.set_element_class_lookup(_Lookup())
    shipOrder = objectify.parse(sampleFile, parser).getroot()

    return shipOrder


def test_create_attribute(ship_order: etree.ElementTree) -> None:
    """It creates an attribute that user can get and set properly."""
    assert ship_order.orderId == "889923"

    newOrderId = "1234"
    ship_order.orderId = newOrderId
    assert ship_order.orderId == newOrderId


def test_create_element_text(ship_order: etree.ElementTree) -> None:
    """It creates an element text that user can get and set properly."""
    assert ship_order.orderPerson == "John Smith"

    newOrderPerson = "John Doe"
    ship_order.orderPerson = newOrderPerson
    assert ship_order.orderPerson == newOrderPerson


def test_create_attribute_list(ship_order: etree.ElementTree) -> None:
    """It creates an attribute list that user can get and set properly."""
    assert ship_order.discounts == [1, 2]

    newDiscounts = [3]
    ship_order.discounts = newDiscounts
    assert ship_order.discounts == newDiscounts


def test_fill_in_defaults(ship_order: etree.ElementTree) -> None:
    "It fills defaults properly."
    staticDefaults = {"_ShipOrder": {"orderStatus": "wip"}}

    def _get_order_time(element: etree.ElementBase) -> str:
        return element.orderId

    dynamicDefaults = {"_ShipOrder": {"orderTime": _get_order_time}}

    fill_in_defaults(ship_order, staticDefaults, dynamicDefaults)
    assert ship_order.orderStatus == staticDefaults["_ShipOrder"]["orderStatus"]
    assert ship_order.orderTime == ship_order.orderId


def test_get_element(ship_order: etree.ElementTree) -> None:
    """It gets an element properly."""
    shipTo = ship_order.shipTo
    assert shipTo.name == "Ola Nordmann"


def test_get_element_list(ship_order: etree.ElementTree) -> None:
    """It gets an element list properly."""
    items = ship_order.itemsList
    assert len(items) == 2


def test_get_inner_text_list(ship_order: etree.ElementTree) -> None:
    """It gets an inner text list properly."""
    items = ship_order.itemsList
    assert items[0].notes == ["Item1", "Item1.1"]
